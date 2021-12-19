file_paths = [
    # "./raw/minimax_ab_max_d4_new_eval_.out",
    # "./raw/minimax_ab_max_d4_new_eval__.out",
    # "./raw/minimax_ab_sum_d4_new_eval_.out",
    # "./raw/minimax_ab_sum_d4_new_eval__.out",
    # "./raw/mixed_d4.out",
    # "./raw/mixed_d5.out"
    "./raw/mixed_u4.out",
    "./raw/mixed_u5.out",
    "./raw/mixed_l4.out",
    "./raw/mixed_l5.out",
]

for file_path in file_paths:
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
    file_output = file_output.replace("raw", "result", 1)
    f = open(file_output, "w")

    print(file_output)
    for k, v in tiles.items():
        print(k, v)
        f.write(f"{k} {v}\n")
