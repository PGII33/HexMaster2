""" Fichier de gestion des effets """

from src.const import ABATTAGE_PI, CONFORT_PI, MOUILLE_DUREE
from src.auxiliaire import adjacents_hex
from src.statut import StatutActif
#pylint: disable=unused-argument

def damage(cible, montant):
    """ Inflige des dégâts à une cible

    Args:
        cible: L'entité cible
        montant: Montant des dégâts à infliger
    """
    nouveaux_pv = cible.get_pv() - montant
    cible.set_pv(nouveaux_pv)


def ajouter_pi(joueurs, joueur, montant):
    """ Ajoute des points d'invocation à un joueur

    Args:
        joueurs: Dictionnaire {numero_equipe: objet_joueur} pour donner les PI
        joueur: L'objet joueur à qui ajouter les PI
        montant: Montant des PI à ajouter
    """
    if joueurs is not None and joueur in joueurs:
        j = joueurs[joueur]
        j.set_pi(j.get_pi() + montant)

class Effet:
    """ Les effets - Méthodes statiques uniquement """

    _effets_custom = {}

    @staticmethod
    def enregistrer_effets_custom(effets_definitions: dict):
        """Enregistre les définitions d'effets JSON composés."""
        Effet._effets_custom = {
            nom: definition for nom, definition in effets_definitions.items()
        }

    @staticmethod
    def appliquer_nom(nom_effet, origine, toutes_entitees, cible=None, joueurs=None):
        """Applique un effet, natif ou composé depuis JSON."""

        if nom_effet in Effet._effets_custom:
            definition = Effet._effets_custom[nom_effet]
            for etape in definition.get("effets", []):
                base = etape.get("base")
                params = etape.get("params", {})
                Effet.appliquer_base(base, origine, toutes_entitees, cible, joueurs, params)
            return
        else:
            raise ValueError(f"Effet inconnu: {nom_effet}")

    @staticmethod
    def appliquer_base(base, origine, toutes_entitees, cible=None, joueurs=None, params=None):
        """Applique une étape élémentaire d'un effet composé."""
        params = params if params is not None else {}

        match base:
            case "degats_sur_meme_case":
                montant = int(params.get("montant", 0))
                cible_type = params.get("cible", "")
                Effet.degats_sur_meme_case(origine, toutes_entitees, montant, cible_type)
                return

            case "ajouter_pi_origine":
                montant = int(params.get("montant", 0))
                ajouter_pi(joueurs, origine.get_equipe(), montant)
                return

            case "transformer":
                cible_type = params.get("cible_type", "")
                entite1 = params.get("entite1", "")
                entite2 = params.get("entite2")
                Effet.transformer(origine, toutes_entitees, cible_type, cible, entite1, entite2)
                return

            case _:
                raise ValueError(f"Effet de base inconnu: {base}")

    @staticmethod
    def degats_sur_meme_case(origine, toutes_entitees, montant, cible_type="creature"):
        """Inflige des dégâts à une catégorie d'entités présentes sur la case d'origine."""
        for entite in toutes_entitees:
            if entite.get_pos() != origine.get_pos():
                continue

            if cible_type == "creature" and not entite.est_creature():
                continue
            if cible_type == "batiment" and not entite.est_batiment():
                continue
            if cible_type == "case" and not entite.est_case():
                continue

            if entite == origine:
                continue
            damage(entite, montant)

    def transformer(origine, toutes_entitees, cible_type, cible, entite1, entite2):
        "Transforme les cibles_type ou entite1 en entite2"
        for entite in toutes_entitees:
            if entite.get_pos() != cible.get_pos():
                continue
            if cible_type == "creature" and not entite.est_creature():
                continue
            if cible_type == "batiment" and not entite.est_batiment():
                continue
            if cible_type == "case" and not entite.est_case():
                continue

            if entite == origine:
                continue

            if entite1 != "" and entite.get_nom().lower() != entite1.lower():
                continue

            # Import local pour éviter la dépendance circulaire
            from src.chargeur.entite_chargeur import EntiteChargeur #pylint: disable=import-outside-toplevel
            chargeur = EntiteChargeur()
            chargeur.charger_toutes_les_entites()
            nouvelle_entite = chargeur.creer_instance(entite2.lower(), cible.get_pos(), origine.get_equipe())
            if nouvelle_entite is not None:
                print("Transformer", entite.get_nom(), "en", nouvelle_entite.get_nom())
                toutes_entitees.append(nouvelle_entite)
                entite.set_pv(0)
                return

    @staticmethod
    def creer_statut_mouille():
        """ Crée une instance du statut Mouille """
        return StatutActif(
            nom="Mouille",
            duree=MOUILLE_DUREE,
            modificateurs={"mouv_max": -1}
        )

    @staticmethod
    def piquant(origine, toutes_entitees, cible=None, joueurs=None):
        """ Effet piquant : inflige des dégâts aux créatures sur la même case

        Args:
            origine: L'entité (case) qui a la compétence piquant
            toutes_entitees: Liste de toutes les entités du terrain
            cible: Non utilisé pour cette compétence
            joueurs: Non utilisé pour cette compétence
        """
        Effet.degats_sur_meme_case(origine, toutes_entitees, DGTS_PIQUANT, "creature")

    @staticmethod
    def instable(origine, toutes_entitees, cible=None, joueurs=None):
        """ Effet instable : à la fin du tour, les bâtiments sur la même case perdent des PV

        Args:
            origine: L'entité qui possède la compétence
            toutes_entitees: Liste de toutes les entités du terrain
            cible: Non utilisé pour cette compétence
            joueurs: Dictionnaire {numero_equipe: objet_joueur} pour retirer les PI
        """
        for entite in toutes_entitees:
            if entite.get_pos() == origine.get_pos() and entite.est_batiment():
                damage(entite, DGTS_INSTABLE)

    @staticmethod
    def abattage(origine, toutes_entitees, cible, joueurs=None):
        """ Effet abattage : si la cible est une case forêt, la transforme en case plaine, l'utilisateur gagne des PI

        Args:
            origine: L'entité qui possède la compétence
            toutes_entitees: Liste de toutes les entités du terrain
            cible: L'entité ciblée par l'attaque
            joueurs: Dictionnaire {numero_equipe: objet_joueur} pour donner les PI
        """
        # Import local pour éviter la dépendance circulaire
        from src.chargeur.entite_chargeur import EntiteChargeur #pylint: disable=import-outside-toplevel

        if cible is not None and cible.est_case() and cible.get_nom() == "Foret":
            # Transformer la case forêt en case plaine
            pos = cible.get_pos()
            equipe = cible.get_equipe()

            # Retirer la case forêt
            cible.set_pv(0)

            # Créer une nouvelle case plaine à la même position
            chargeur = EntiteChargeur()
            chargeur.charger_toutes_les_entites()
            plaine = chargeur.creer_instance("plaine", pos, equipe)
            if plaine is not None:
                toutes_entitees.append(plaine)

            ajouter_pi(joueurs, origine.get_equipe(), ABATTAGE_PI)

    @staticmethod
    def confort(origine, toutes_entitees, cible=None, joueurs=None):
        """ Effet confort : à la fin du tour, le joueur gagne des PI

        Args:
            origine: L'entité qui possède la compétence
            toutes_entitees: Liste de toutes les entités du terrain
            cible: Non utilisé pour cette compétence
            joueurs: Dictionnaire {numero_equipe: objet_joueur} pour donner les PI
        """
        ajouter_pi(joueurs, origine.get_equipe(), CONFORT_PI)


    @staticmethod
    def pluie_de_fleches(origine, toutes_entitees, cible, joueurs=None):
        """ Effet pluie de flèches : inflige les dégats de toutes les "archer" alliées à une cible

        Args:
            origine: L'entité qui possède la compétence
            toutes_entitees: Liste de toutes les entités du terrain
            cible: L'entité ciblée par l'attaque
            joueurs: Dictionnaire {numero_equipe: objet_joueur} pour retirer les PI
        """
        if cible is None:
            return

        equipe_origine = origine.get_equipe()
        total_dgts = 0
        for entite in toutes_entitees:
            if (entite.get_equipe() == equipe_origine
                and "archer" in entite.get_tags()
            ):
                if cible.est_creature():
                    total_dgts += entite.get_combat()
                elif cible.est_batiment():
                    total_dgts += entite.get_demolition()
                elif cible.est_case():
                    total_dgts += entite.get_degradation()
        damage(cible, total_dgts)

    @staticmethod
    def pluie(origine, toutes_entitees, cible, joueurs=None):
        """ Applique le statut Mouille sur la case ciblée et les hexagones adjacents """
        if cible is None:
            return

        positions_affectees = set(adjacents_hex(cible.get_pos()))
        positions_affectees.add(cible.get_pos())

        for entite in toutes_entitees:
            if entite.est_creature() and entite.get_pos() in positions_affectees:
                entite.ajouter_statut(Effet.creer_statut_mouille())
