f = open("log.txt", "r")
fout = open("log_.txt", "w")

lines = f.readlines()

for i, line in enumerate(lines):
    if i % 6 == 0:
        idx = int(line.split()[0]) + 4236
        fout.write(f"{idx}\n")
    else:
        fout.write(line)

f.close()
fout.close()