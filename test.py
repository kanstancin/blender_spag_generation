

lines = []
with open("gcodes/707.gcode") as f:
    lines = f.readlines()
    print(len(f.readlines()))
