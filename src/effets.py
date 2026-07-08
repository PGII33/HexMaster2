""" Fichier de gestion des effets """
from __future__ import annotations
from src.const import MOUILLE_DUREE
from src.auxiliaire import a_portee_hex
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
        Effet._effets_custom = dict(effets_definitions.items())

    @staticmethod
    def appliquer_nom(nom_effet, origine, toutes_entitees, cible=None, joueurs=None):
        """Applique un effet composé depuis JSON."""

        if nom_effet in Effet._effets_custom:
            definition = Effet._effets_custom[nom_effet]
            contexte = {}  # Contexte pour sauvegarder les résultats des effets
            for etape in definition.get("effets", []):
                base = etape.get("base")
                params = etape.get("params", {})
                condition = etape.get("condition")
                
                # Vérifier la condition si elle existe
                if condition and not Effet._evaluer_condition(condition, contexte):
                    continue
                
                resultat = Effet.appliquer_base(
                    base,
                    origine,
                    toutes_entitees,
                    cible=cible,
                    joueurs=joueurs,
                    params=params,
                )
                
                # Sauvegarder le résultat si demandé
                save_result = etape.get("save_result")
                if save_result:
                    contexte[save_result] = resultat
            return

        if hasattr(Effet, nom_effet):
            methode = getattr(Effet, nom_effet)
            return methode(origine, toutes_entitees, cible, joueurs)

        raise ValueError(f"Effet inconnu: {nom_effet}")

    @staticmethod
    def appliquer_base(base, origine, toutes_entitees, cible=None, **options):
        """Applique une étape élémentaire d'un effet composé."""
        joueurs = options.get("joueurs")
        params = options.get("params") or {}

        match base:
            case "degats_sur_meme_case":
                montant = int(params.get("montant", 0))
                cible_type = params.get("cible", "")
                Effet.degats_sur_meme_case(origine, toutes_entitees, montant, cible_type)
                return True

            case "ajouter_pi_origine":
                montant = int(params.get("montant", 0))
                ajouter_pi(joueurs, origine.get_equipe(), montant)
                return True

            case "transformer":
                cible_type = params.get("cible_type", "")
                entite1 = params.get("entite1", "")
                entite2 = params.get("entite2")
                resultat = Effet.transformer(
                    origine,
                    toutes_entitees,
                    cible=cible,
                    cible_type=cible_type,
                    entite1=entite1,
                    entite2=entite2,
                )
                return resultat

            case "donner_statut":
                statut = params.get("statut", "")
                rayon = params.get("rayon", 0)
                Effet.donner_statut(
                    origine,
                    toutes_entitees,
                    statut,
                    cible=cible,
                    rayon=rayon,
                    joueurs=joueurs,
                )
                return True

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

    @staticmethod
    def transformer(origine, toutes_entitees, cible=None, **options):
        """Transforme une entité cible en une autre. Retourne True si réussi."""
        cible_type = options.get("cible_type", "")
        entite1 = options.get("entite1", "")
        entite2 = options.get("entite2")

        if cible is None or not entite2:
            return False

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
                toutes_entitees.append(nouvelle_entite)
                entite.set_pv(0)
                return True
        return False

    @staticmethod
    def donner_statut(origine, toute_entitees, statut, cible=None, **options):
        """Donne un statut chargé dans un rayon autour de la cible."""
        if not statut:
            raise ValueError("Statut manquant pour l'effet donner_statut")

        rayon = options.get("rayon", 0)
        centre = cible if cible is not None else origine
        if centre is None:
            return False

        try:
            rayon = int(rayon)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Rayon invalide pour l'effet donner_statut: {rayon}") from exc

        positions_affectees = set(a_portee_hex(centre.get_pos(), rayon))

        for entite in toute_entitees:
            if entite.est_creature() and entite.get_pos() in positions_affectees:
                entite.ajouter_statut(Effet._creer_statut_depuis_id(statut))

        return True

    @staticmethod
    def _creer_statut_depuis_id(id_statut):
        """Crée un statut à partir du registre JSON, avec fallback minimal."""
        try:
            return StatutActif.depuis_id(id_statut)
        except ValueError as exc:
            raise ValueError(f"Erreur: le statut '{id_statut}' n'a pas été chargé") from exc

    @staticmethod
    def _evaluer_condition(condition, contexte):
        """Évalue une condition simple basée sur le contexte.
        
        Formats supportés:
        - "nom_var == true" ou "nom_var == false"
        - "nom_var" (équivalent à "nom_var == true")
        """
        if not condition or not isinstance(condition, str):
            return True
        
        condition = condition.strip()
        
        # Format "var == true/false"
        if "==" in condition:
            parts = condition.split("==")
            if len(parts) == 2:
                var_name = parts[0].strip()
                expected = parts[1].strip().lower()
                actual = contexte.get(var_name, False)
                
                if expected == "true":
                    return actual is True
                elif expected == "false":
                    return actual is False
        
        # Format "var" (assume true)
        else:
            var_name = condition.strip()
            return contexte.get(var_name, False) is True
        
        return False

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
