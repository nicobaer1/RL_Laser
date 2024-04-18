import numpy as np

# Load the array from the text file
loaded_action_array = np.loadtxt('action_array.txt')

print(loaded_action_array)
print(type(loaded_action_array))