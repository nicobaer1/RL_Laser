import os
import time

import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict
import numpy as np
from stable_baselines3 import PPO, SAC
import socket
import pickle
import pickle
import csv
import precitecpyV2

import mircoepsilonpy
import d3rlpy
from d3rlpy.algos.qlearning import DDPGConfig, DQNConfig

id = 3706
obs = precitecpyV2.obs(id)

# Pfadeinstellungen
model_filename = "SAC_16_04_2024_V1.zip"  # Name der Modelldatei
# Laden des Modells aus dem angegebenen Pfad
loaded_model = SAC.load(model_filename )


action, _ = loaded_model.predict(obs, deterministic=True)

print("Vorhergesagte Aktion:", action)