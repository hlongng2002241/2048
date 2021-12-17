file_path = "./minimax_ab_max_d5_new_eval.out"
f = open(file_path, "r")


lines = f.readlines()
f.close()

tiles = dict()

for line in lines:
    if line.startswith("max_tile"):
        tile = int(line[10:-1])
        tiles[tile] = tiles.get(tile, 0) + 1
    elif line.startswith("score"):
        score = int(line[7:-1])

file_output = file_path[0: file_path.rfind('.')] + ".result"
f = open(file_output, "w")

for k, v in tiles.items():
    print(k, v)
    f.write(f"{k} {v}\n")
