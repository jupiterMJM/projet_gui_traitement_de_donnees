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
from scipy.signal import convolve


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

    # Tof1_on = Tof1[:,np.squeeze(np.where(shutter_axis%2==1)),:]
    Tof1_off= Tof1[:,np.squeeze(np.where(shutter_axis%2==0)),:]
    # Tof2_on = Tof2[:,np.squeeze(np.where(shutter_axis%2==1)),:]
    Tof2_off= Tof2[:,np.squeeze(np.where(shutter_axis%2==0)),:]

    # Tof1_on_avg=np.mean(Tof1_on,axis=0)
    Tof1_off_avg=np.mean(Tof1_off,axis=0)
    # Tof2_on_avg=np.mean(Tof2_on,axis=0)
    Tof2_off_avg=np.mean(Tof2_off,axis=0)
    return (tof_axis, Tof1_off_avg[0]), (tof_axis, Tof2_off_avg[0])


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



def apply_theory_on_bottle1(path_to_theory, data_tof_1, return_data_interpolate = False):
    """
    Applique la théorie sur les données de la bouteille 1 pour comparaison avec les données de la bouteille 2
    :param path_to_theory: str
    :param data_tof_1: tuple
    :return: tuple
    """
    # extraction des données de la théorie
    theory=np.loadtxt(path_to_theory)
    energies, value = theory[0], theory[1]

    # on enleve l'offset des valeurs
    value = value - np.min(value)
    # print(energies)

    # juste un test (il faut l'enlever après)
    # energies = np.linspace(-max(np.min(data_tof_1[0]), np.max(data_tof_1[0])), max(np.min(data_tof_1[0]), np.max(data_tof_1[0])), 10000)
    # energies = np.linspace(-1, 1, 10)
    # from scipy import signal
    # dirac = np.zeros_like(energies)
    # zero_crossings = np.where(np.diff(np.sign(energies)))[0]
    # dirac[zero_crossings] = 1
    # value = dirac

    # # interpolation des données de la théorie
    x_min = -max(abs(data_tof_1[0][-1]), abs(data_tof_1[0][-1]), abs(energies[0]), abs (energies[1]))    #min(data_tof_1[0][0], np.min(energies))
    x_max = max(abs(data_tof_1[0][-1]), abs(data_tof_1[0][-1]), abs(energies[0]), abs (energies[1]))
    # print(x_min, x_max)
    x_common = np.arange(x_min, x_max, step=min(data_tof_1[0][1]-data_tof_1[0][0], abs(energies[1]-energies[0])))
    print("x_common", x_common)
    # print(np.where(np.diff(np.sign(x_common)) != 0)[0])
    # Interpoler les deux ensembles de données sur l'ensemble commun d'abscisses
    y1_interpolated = np.interp(x_common, data_tof_1[0], data_tof_1[1], left=0, right=0)
    y2_interpolated = np.interp(x_common, energies, value, left = 0, right=0)
    print("y1_interpolated", y1_interpolated)
    print("value", value)
    print("y2_interpolated", y2_interpolated)
    # application de l'opération de convolution entre la théorie et la bouteille 1
    convol = convolve(y1_interpolated, y2_interpolated, mode='same')
    if return_data_interpolate: return (x_common, convol), (x_common, y1_interpolated, y2_interpolated)
    return (x_common, convol)


if __name__ == "__main__":
    tof1_data, tof2_data = ouverture_data_tof("data.h5")
    tof1_config, tof2_config = extract_config_file("configuration.json", "liquid")
    tof1_data = calibration_tof(tof1_data, tof1_config["alpha"], tof1_config["t0"], tof1_config["V0"])
    plt.plot(*apply_theory_on_bottle1("WaterLiquidValence_smooth.txt", tof1_data))
    plt.show()