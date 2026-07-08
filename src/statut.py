""" Fichier de gestion des statuts actifs """

from __future__ import annotations

from src.phase import PhaseTour


class StatutActif:
    """Représente un statut appliqué à une entité."""

    _statuts_custom: dict[str, dict] = {}

    def __init__(self, nom: str, duree: int, phase: PhaseTour = PhaseTour.FIN_TOUR,
                 modificateurs: dict[str, int] | None = None, nom_effet: str | None = None,
                 est_buff: bool = False, id_statut: str | None = None):
        """Initialise un statut actif."""
        self.id_statut = (id_statut or nom).lower().replace(" ", "_")
        self.nom = nom
        self.duree_restante = duree
        self.phase = phase
        self.modificateurs = dict(modificateurs) if modificateurs is not None else {}
        self._est_buff = est_buff
        self.nom_effet = nom_effet.lower() if isinstance(nom_effet, str) and nom_effet else None

    def get_nom(self):
        """ Retourne le nom du statut """
        return self.nom

    def get_id(self):
        """Retourne l'identifiant du statut."""
        return self.id_statut

    def get_duree_restante(self):
        """ Retourne le nombre de tours restants """
        return self.duree_restante

    def est_buff(self):
        """ Retourne vrai si le statut est un buff, faux si c'est un debuff """
        return self._est_buff

    def est_debuff(self):
        """ Retourne vrai si le statut est un debuff, faux si c'est un buff """
        return not self._est_buff

    def set_duree_restante(self, duree: int):
        """ Modifie la durée restante du statut """
        self.duree_restante = duree

    def rafraichir(self, duree: int|None = None, modificateurs: dict[str, int]|None = None,
                   phase: PhaseTour|None = None, nom_effet: str|None = None):
        """ Rafraîchit les données du statut lors d'une réapplication """
        if duree is not None:
            self.duree_restante = duree
        if modificateurs is not None:
            self.modificateurs = dict(modificateurs)
        if phase is not None:
            self.phase = phase
        if nom_effet is not None:
            self.nom_effet = nom_effet

    def decrementer(self):
        """ Décrémente la durée d'un tour si elle est positive """
        if self.duree_restante > 0:
            self.duree_restante -= 1

    def est_expire(self):
        """ Retourne vrai si le statut est expiré """
        return self.duree_restante == 0

    def get_phase(self):
        """ Retourne la phase d'activation du statut """
        return self.phase

    def get_nom_effet(self):
        """ Retourne le nom de l'effet à résoudre pour ce statut """
        if self.nom_effet is not None:
            return self.nom_effet
        return self.nom.lower().replace(" ", "_")

    def get_modificateur(self, statistique: str):
        """ Retourne le modificateur d'une statistique donnée """
        return self.modificateurs.get(statistique, 0)

    def get_modificateurs(self):
        """ Retourne tous les modificateurs du statut """
        return dict(self.modificateurs)

    @staticmethod
    def _nom_depuis_id(identifiant: str):
        return " ".join(mot.capitalize() for mot in identifiant.replace("_", " ").split())

    @staticmethod
    def _normaliser_phase(phase):
        if phase is None:
            return PhaseTour.FIN_TOUR
        if isinstance(phase, PhaseTour):
            return phase
        if isinstance(phase, str):
            phase_normalisee = phase.strip().upper()
            if hasattr(PhaseTour, phase_normalisee):
                return getattr(PhaseTour, phase_normalisee)
        raise ValueError(f"Phase invalide pour un statut: {phase}")

    @classmethod
    def normaliser_definition(cls, definition: dict, source: str | None = None):
        """Valide et normalise une définition JSON de statut."""
        if not isinstance(definition, dict):
            origine = f" dans {source}" if source else ""
            raise ValueError(f"Statut invalide{origine}: format JSON attendu")

        id_statut = definition.get("id")
        if not id_statut:
            origine = f" dans {source}" if source else ""
            raise ValueError(f"Statut invalide{origine}: champ 'id' manquant")

        duree = definition.get("duree")
        if duree is None:
            origine = f" dans {source}" if source else ""
            raise ValueError(f"Statut '{id_statut}' invalide{origine}: champ 'duree' manquant")

        modificateurs = definition.get("modificateurs", {})
        if modificateurs is None:
            modificateurs = {}
        if not isinstance(modificateurs, dict):
            origine = f" dans {source}" if source else ""
            raise ValueError(f"Statut '{id_statut}' invalide{origine}: champ 'modificateurs' invalide")

        valeur_nom_effet = definition.get("nom_effet", definition.get("effet"))

        return {
            "id": str(id_statut).lower(),
            "nom": definition.get("nom", cls._nom_depuis_id(str(id_statut).lower())),
            "duree": int(duree),
            "phase": cls._normaliser_phase(definition.get("phase")),
            "modificateurs": dict(modificateurs),
            "est_buff": bool(definition.get("est_buff", False)),
            "nom_effet": str(valeur_nom_effet).lower() if valeur_nom_effet else None,
        }

    @classmethod
    def depuis_definition(cls, definition: dict, source: str | None = None):
        """Construit une instance depuis une définition JSON normalisée."""
        definition_normalisee = cls.normaliser_definition(definition, source=source)
        return cls(
            nom=definition_normalisee["nom"],
            duree=definition_normalisee["duree"],
            phase=definition_normalisee["phase"],
            modificateurs=definition_normalisee["modificateurs"],
            nom_effet=definition_normalisee["nom_effet"],
            est_buff=definition_normalisee["est_buff"],
            id_statut=definition_normalisee["id"],
        )

    @staticmethod
    def enregistrer_statuts_custom(statuts_definitions: dict):
        """Enregistre les définitions de statuts JSON."""
        StatutActif._statuts_custom = dict(statuts_definitions.items())

    @classmethod
    def depuis_id(cls, id_statut: str):
        """Construit un statut à partir de son identifiant chargé."""
        if not id_statut:
            raise ValueError("Statut invalide sans identifiant")

        definition = cls._statuts_custom.get(id_statut.lower())
        if definition is None:
            raise ValueError(f"Statut inconnu: {id_statut}")

        return cls.depuis_definition(definition)
