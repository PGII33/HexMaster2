""" Fichier de gestion des effets """

from src.const import DGTS_PIQUANT, DGTS_INSTABLE, ABATTAGE_PI, CONFORT_PI, MOUILLE_DUREE
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

        for entite in toutes_entitees:
            if entite.get_pos() == origine.get_pos() and entite.est_creature():
                damage(entite, DGTS_PIQUANT)

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
    def pluie_de_fleches(origine, toutes_entitees, cible, joueurs=None):
        """ Effet pluie de flèches : inflige les dégats de toutes les archères alliées à une cible

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
            if (
                entite.est_creature()
                and entite.get_equipe() == equipe_origine
                and entite.get_nom().lower() in ["archere", "archer"]
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
