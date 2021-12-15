f = open("./minimax_ab_sum_d5.out", "r")

lines = f.readlines()
scores = dict()

for line in lines:
    if line.startswith("max_tile"):
        score = int(line[10:-1])
        scores[score] = scores.get(score, 0) + 1

for k, v in scores.items():
    print(k, v)
