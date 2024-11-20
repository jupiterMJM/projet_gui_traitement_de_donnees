"""
auteur : Maxence BARRE
date : 2024
projet : affichage graphique de comparaison des bouteilles magnétiques
fichier : annexes pour l'ouverture et le traitement des fichiers de données
"""

import h5py as h
import numpy as np
import	matplotlib.pyplot as plt
from annexe_gui import *
import json


def ouverture_data_tof(path_to_data):
    """
    Ouvre un fichier de données et extrait les données de temps de vol
    :param path_to_data: str
    :return: tuple
    """
    with h.File(path_to_data, "r") as f:
        Tof1 = np.squeeze(np.array(f['RawData']['Scan000']['Detector000']['Data1D']['CH00']['Data00']))
        Tof2 = np.squeeze(np.array(f['RawData']['Scan000']['Detector000']['Data1D']['CH00']['Data01']))
        tof_axis = 10**6*np.squeeze(np.array(f['RawData']['Scan000']['Detector000']['Data1D']['CH00']['Axis00']))
        shutter_axis = np.squeeze(np.array(f['RawData']['Scan000']['NavAxes']['Axis01']))

    Tof1_on = Tof1[:,np.squeeze(np.where(shutter_axis%2==1)),:]
    # Tof1_off= Tof1[:,np.squeeze(np.where(shutter_axis%2==0)),:]
    Tof2_on = Tof2[:,np.squeeze(np.where(shutter_axis%2==1)),:]
    # Tof2_off= Tof2[:,np.squeeze(np.where(shutter_axis%2==0)),:]

    Tof1_on_avg=np.mean(Tof1_on,axis=0)
    # Tof1_off_avg=np.mean(Tof1_off,axis=0)
    Tof2_on_avg=np.mean(Tof2_on,axis=0)
    # Tof2_off_avg=np.mean(Tof2_off,axis=0)
    return (tof_axis, Tof1_on_avg[0]), (tof_axis, Tof2_on_avg[0])


def calibration_tof(data_tof, alpha, t0, V0):
    """
    Calibre les données de temps de vol en énergie
    :param data_tof: tuple
    :param alpha: float
    :param t0: float
    :param V0: float
    :return: tuple
    """
    tof_axis, tof = data_tof
    tof_considere = tof - np.mean(tof[:600])
    energy_axis = np.flip([tof2eV(t,V0,alpha,t0) for t in tof_axis])
    signal_E = np.flip(tof_considere)
    for i in range (len(signal_E)):
        signal_E[i] *= np.abs(eV2TOF_Jac(energy_axis[i],alpha,V0))
    return (energy_axis, signal_E)


def extract_config_file(path_to_config, what_s_in_bottle2):
    """
    Extrait les données de configuration du fichier json
    :param path_to_config: str
    :param what_s_in_bottle2: str
    :return: tuple
    """
    with open(path_to_config, 'r') as f:
        data = json.load(f)
    return data["bottle1"], data["bottle2"][what_s_in_bottle2]



def apply_theory_on_bottle1(path_to_theory, data_tof_1):
    """
    Applique la théorie sur les données de la bouteille 1 pour comparaison avec les données de la bouteille 2
    :param path_to_theory: str
    :param data_tof_1: tuple
    :return: tuple
    """
    # extraction des données de la théorie
    theory=np.loadtxt(path_to_theory)
    energies, value = np.flip(np.abs(theory[0])), theory[1]

    # interpolation des données de la théorie
    theory_interpolate = np.interp(data_tof_1[0], energies, value)

    # application de l'opération de convolution entre la théorie et la bouteille 1
    convol = np.convolve(theory_interpolate, data_tof_1[1], mode='same')
    return (data_tof_1[0], convol)


if __name__ == "__main__":
    tof1_data, tof2_data = ouverture_data_tof("data.h5")
    tof1_config, tof2_config = extract_config_file("configuration.json", "liquid")
    tof1_data = calibration_tof(tof1_data, tof1_config["alpha"], tof1_config["t0"], tof1_config["V0"])
    plt.plot(*apply_theory_on_bottle1("WaterLiquidValence_smooth.txt", tof1_data))
    plt.show()