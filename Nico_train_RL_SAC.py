import os
import time

import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict
import numpy as np
from stable_baselines3 import PPO, SAC
import socket
import pickle

import csv
import precitecpyV2
import mircoepsilonpy
import d3rlpy
from d3rlpy.algos.qlearning import DDPGConfig, DQNConfig


# Dateipfad angeben
file_path = r"\\ifsw-cifs.tik.uni-stuttgart.de\DATA0\shared\Projekte\Laufend\2023 ICM IC CutAIye (85037125)\05_Experimente\00_Python\00_Python_Programme\00_Automatisierung\Reinforcement_learning_main\action\action.txt"
"""
        Defines the action space for the laser system.

        :param Laserleistung_low: Lowest laser power
        :param Laserleistung_high: Highest laser power
        :param Gasdruck_low: Lowest gas pressure
        :param Gasdruck_high: Highest gas pressure
        :param Vorschub_low: Lowest feed rate
        :param Vorschub_high: Highest feed rate
        :param Düsenabstand_low: Lowest nozzle distance
        :param Düsenabstand_high: Highest nozzle distance
        :param Fokusabstand_low: Lowest focus distance
        :param Fokusabstand_high: Highest focus distance
        :param action_space: Parameter space of the action
        :param self.id: Trial number
        
        :param number_of_trials: Anzahl der Versuche, die in der Umgebung durchgeführt werden sollen.
        :param signal_length: Länge des Signals in der Beobachtungsraumdefinition.
        :param observation_space: Der Beobachtungsraum der Umgebung, der als Box definiert ist. Er enthält die Beobachtungen, die der Agent während des Trainings erhält.
        :paramCuttingEnv_EP: Die Klasse, die die Umgebung für das Schneiden implementiert. Sie erbt von der Klasse Env.

        :param __init__: Der Konstruktor, der den Aktionsraum, den Beobachtungsraum und die Anzahl der Versuche initialisiert.
        :param obs: Eine Methode, die die Beobachtungen der Umgebung zurückgibt.
        :param reward: Eine Methode, die die Belohnung für eine Aktion berechnet.
        :param done: Eine Methode, die überprüft, ob der Versuch beendet ist oder nicht.
        :param step: Eine Methode, die einen Schritt in der Umgebung ausführt und die Beobachtungen, Belohnung, den Zustand der Umgebung und zusätzliche Informationen zurückgibt.
        :param reset: Eine Methode, die die Umgebung zurücksetzt und den initialen Zustand zurückgibt.
"""

Laserleistung_low, Laserleistung_high = 4000, 8000
Gasdruck_low, Gasdruck_high = 8000, 18000
Vorschub_low, Vorschub_high = 1000, 4000
Düsenabstand_low, Düsenabstand_high = 1,5
Fokusabstand_low, Fokusabstand_high = -8, -3
#Versuchslänge
number_of_trials = 10
signal_length =1000 #signal_length =498011

# Aktionsraum definieren
action_space = Box(
    low=np.array([Laserleistung_low,Gasdruck_low,Vorschub_low, Düsenabstand_low, Fokusabstand_low]),  # Untere Grenzen für jede Aktion
    high=np.array([Laserleistung_high,Gasdruck_high, Vorschub_high, Düsenabstand_high, Fokusabstand_high]),  # Obere Grenzen für jede Aktion
    dtype=np.float64  # Datentyp der Aktionen
)

# Beobachtungsraum definieren
observation_space = Box(
    low=np.expand_dims(np.array([0, 0, 0]),0).repeat(signal_length, axis=0) , # Untere Grenzen für t_raw, p_raw und r_raw
    high=np.expand_dims(np.array([10, 10, 10]),0).repeat(signal_length, axis=0), # Obere Grenzen für t_raw, p_raw und r_raw
    shape=(signal_length, 3),  # Form der Beobachtungen: (signal_length, 3)
    dtype=np.float64  # Datentyp der Beobachtungen
)


#class CuttingEnv_Con(Env):
class CuttingEnv_EP(Env):
    """":param action_space: Parameter space of the action
        :param self.id: Trial number
        :param number_of_trials: Anzahl der Versuche, die in der Umgebung durchgeführt werden sollen.
        :param signal_length: Länge des Signals in der Beobachtungsraumdefinition.
        :param observation_space: Der Beobachtungsraum der Umgebung, der als Box definiert ist. Er enthält die Beobachtungen, die der Agent während des Trainings erhält.
        :paramCuttingEnv_EP: Die Klasse, die die Umgebung für das Schneiden implementiert. Sie erbt von der Klasse Env.
        :param __init__: Der Konstruktor, der den Aktionsraum, den Beobachtungsraum und die Anzahl der Versuche initialisiert.
        :param obs: Eine Methode, die die Beobachtungen der Umgebung zurückgibt.
        :param reward: Eine Methode, die die Belohnung für eine Aktion berechnet.
        :param done: Eine Methode, die überprüft, ob der Versuch beendet ist oder nicht.
        :param step: Eine Methode, die einen Schritt in der Umgebung ausführt und die Beobachtungen, Belohnung, den Zustand der Umgebung und zusätzliche Informationen zurückgibt.
        :param reset: Eine Methode, die die Umgebung zurücksetzt und den initialen Zustand zurückgibt."""
    def __init__(self):
        # Aktionsraum und Beobachtungsraum setzen
        self.action_space = action_space
        self.observation_space = observation_space
        # Schneidzeit setzen (Zeitpunkte)
        self.sequence_length =number_of_trials #Anzahl der Schnitte
        self.id = 3627
        self.state = None
        self.last_action = None

    def is_done(self):
        while True:
            eingabe = input("Ist der Versuch durchlaufen worden? LWM gespeichert worden (ja/nein): ").lower()
            if eingabe == "ja":
                self.id = self.id + 1
                print("Der Versuch wurde beendet.")
                return True
            elif eingabe == "nein":
                print("Die Schleife wurde abgebrochen.")
                continue
            else:
                print("Ungültige Eingabe. Bitte antworte mit 'ja' oder 'nein'.")
        print("done durchlaufen")

    def update_obs(self):
        print("Code Obs")
        id=self.id
        #print("id:",id)
        obs = precitecpyV2.obs(id)
        print("Obs durchlaufen ")

        return obs
    def reward(self):
        "STEFAN REWARD"
        reward_array =mircoepsilonpy.reward(self.id)
        reward = reward_array[0]
        print("Reward durchlaufen ")

        return reward

    def check_id(self):
        print("Aktueller Wert von self.id ist:", self.id)
        antwort = input("Ist der Wert korrekt? (ja/nein): ")
        if antwort.lower() == "ja":
            print("Der Wert ist korrekt.")
        elif antwort.lower() == "nein":
            neue_id = input("Bitte geben Sie den neuen Wert für self.id ein: ")
            self.id = int(neue_id)
            print("Der Wert von self.id wurde erfolgreich geändert.")
        else:
            print("Ungültige Eingabe. Bitte geben Sie 'ja' oder 'nein' ein.")
            self.check_id()

    def step(self, action):
        # Convert the list to a NumPy array
        self.check_id()
        print("action",action)
        action_array = np.array(action)
        # Save the array to a text file
        np.savetxt('action_array.txt', action_array)
        self.is_done()
        print("ID", self.id)
        # Einzelne Beobachtung zurückgeben
        obs = self.update_obs()
        # reward
        reward = self.reward()
        print("Reward:", reward)
        info = {}
        # Schneidzeit verringern
        self.sequence_length -= 1
        print("sequence_length", self.sequence_length)
        done = self.sequence_length <= 0
        return obs, reward, done, info

   

    def reset(self):
        self.state = np.zeros((1000, 3))
        print("state = Zeros")
        self.sequence_length = number_of_trials
        print("sequence_length", self.sequence_length )
        self.last_action = None  # Setzen Sie die letzte Aktion auf None zurück
        model.save('SAC_16_04_2024_V2')
        print("Modell gespeichert")
        return np.array(self.state, dtype=np.float32)

# SAC-Modell initialisieren und trainieren
env = CuttingEnv_EP()
model = SAC("MlpPolicy", env, buffer_size=100, verbose=1)
# Trainieren des Modells
model.learn(total_timesteps=200, log_interval=number_of_trials)
model.save('SAC_16_04_2024_Final_V2')
print("Training beendet")

