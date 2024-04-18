import os
import time

import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict
import numpy as np
from stable_baselines3 import PPO
import socket
import pickle
import pickle
import csv
import precitecpy
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
Laserleistung_low, Laserleistung_high = 3000, 8000
Gasdruck_low, Gasdruck_high = 8000, 18000
Vorschub_low, Vorschub_high = 1000, 5000
Düsenabstand_low, Düsenabstand_high = 1,5
Fokusabstand_low, Fokusabstand_high = -16, -3
#Versuchslänge
number_of_trials = 20
signal_length =498011 #signal_length =498011

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
        self.id = 3050
        self.state = None
    def is_done(self):
        while True:
            eingabe = input("Möchtest du fortfahren? (ja/nein): ").lower()
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
        #print("Code Obs")
        id=self.id
        #print("id:",id)
        obs = precitecpy.obs(id)
        print("Obs durchlaufen ")

        return obs
    def reward(self):
        "STEFAN REWARD"

        reward =mircoepsilonpy.reward(self.id)

        print("Reward durchlaufen ")

        return reward



    def step(self, action):
        # Convert the list to a NumPy array


        print("action",action)
        action_array = np.array(action)

        # Save the array to a text file
        np.savetxt('action_array.txt', action_array)

        # Versuch und Auswertung fertig
        done = self.is_done()
        # Einzelne Beobachtung zurückgeben
        obs = self.update_obs()
        # reward
        reward = self.reward()
        print("Reward:", reward)

        info = {}
        print("step")
        print("Laserleistung", action[0],"W "," Gasdruck:",action[1],"mbar ","Vorschub:",action[2]," mm/min ","Düsenabstand:",action[3],"mm ","Fokusabstand:",action[4],"mm" )
        #print("obs:", obs, "reward:", reward, "done:", done, "info", info)

        # Truncated auf False setzen, da in diesem Fall keine Truncation stattfindet
        truncated = False
        return obs, reward, done, info

    def render(self):
        # Implementierung der Visualisierung
        pass

    def initial_obs(self):
        # Implementieren Sie eine Funktion, die einen Standardzustand zurückgibt
        return np.zeros((signal_length, 3), dtype=np.float64)

    def reset(self):
        self.state = self.initial_obs()
        self.sequence_length = number_of_trials
        return np.array(self.state, dtype=np.float32)




# Umgebungsinitialisierung
# Creating an instance of your custom environment
# Umgebungsinitialisierung
env = CuttingEnv_EP()

# Testen der Umgebung
episodes = 0
for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0
    while not done:
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))

# A2C-Modell initialisieren und trainieren
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=20000)
model.save('PPO')
print("Training beendet")