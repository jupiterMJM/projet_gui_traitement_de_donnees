"""
auteur: Maxence BARRE
date: 2024
projet: affichage graphique de comparaison des bouteilles magnétiques
fichier : annexe pour la conversion des données
"""
import numpy as np

def tof2eV(t,V0,alpha,t0):
    """
    Convert a time of flight to an energy
    :param t: float
    :param V0: float
    :param alpha: float
    :param t0: float
    :return: float
    """
    return V0+alpha/((t-t0)**2)

def eV2TOF_Jac(E,alpha,V0):
    """
    Convert an energy to a time of flight
    :param E: float
    :param alpha: float
    :param V0: float
    :return: float
    """
    return 0.5*(np.sqrt(np.abs((E - V0)/alpha)))