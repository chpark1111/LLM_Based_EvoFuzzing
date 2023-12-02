import random

input_data_dir = "./data/input.txt"
initial_inputs = []
with open(input_data_dir, "r") as f:
    nw = f.readline().strip("\n").strip()
    while nw:
        initial_inputs.append(nw)
        nw = f.readline().strip("\n").strip()
        
random.shuffle(initial_inputs)
initial_inputs = initial_inputs[:20]