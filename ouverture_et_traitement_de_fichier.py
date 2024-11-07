import h5py as h
import numpy as np
import	matplotlib.pyplot as plt
from annexe_gui import *
from configuration import *


with h.File('data.h5', "r") as f:
    Tof1 = np.squeeze(np.array(f['RawData']['Scan000']['Detector000']['Data1D']['CH00']['Data00']))
    Tof2 = np.squeeze(np.array(f['RawData']['Scan000']['Detector000']['Data1D']['CH00']['Data01']))
    tof_axis = 10**6*np.squeeze(np.array(f['RawData']['Scan000']['Detector000']['Data1D']['CH00']['Axis00']))
    shutter_axis = np.squeeze(np.array(f['RawData']['Scan000']['NavAxes']['Axis01']))

Tof1_on = Tof1[:,np.squeeze(np.where(shutter_axis%2==1)),:]
Tof1_off= Tof1[:,np.squeeze(np.where(shutter_axis%2==0)),:]
Tof2_on = Tof2[:,np.squeeze(np.where(shutter_axis%2==1)),:]
Tof2_off= Tof2[:,np.squeeze(np.where(shutter_axis%2==0)),:]

Tof1_on_avg=np.mean(Tof1_on,axis=0)
Tof1_off_avg=np.mean(Tof1_off,axis=0)

Tof2_on_avg=np.mean(Tof2_on,axis=0)
Tof2_off_avg=np.mean(Tof2_off,axis=0)

Tof_considere = Tof1_on_avg[0]

alpha, t0, V0 = tof1_config

energy_axis = [tof2eV(t,V0,alpha,t0) for t in tof_axis]
signal_E = np.flip(Tof_considere)
for i in range (len(signal_E)):
    signal_E[i] *= np.abs(eV2TOF_Jac(energy_axis[i],alpha,V0))


plt.plot(energy_axis, Tof_considere,label='Tof1_on')
plt.show()