""" Fichier de gestion des tags. """

class Tag:
    def __init__(self, nom:str):
        """ Initialise un tag """
        self.nom = nom
    
    def get_nom(self):
        """ Retourne le nom du tag """
        return self.nom