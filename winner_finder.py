import sys
import re

prob = sys.argv[1]
pset = sys.argv[2]

with open("leaderboard.txt") as f:
    lines = f.readlines()

leaderboard = []
for line in lines:
    parts = [x.strip() for x in re.split(r" +", line.strip())]
    # print(prob, set, parts[0], parts[1])
    if parts[0] == prob and parts[1] == pset:
        leaderboard.append(parts[2:])

# leaderboard.sort()
# print(leaderboard)

leaderboard.sort(key=lambda x: (-int(x[0]), x[1]))


# teams = set()
# filtered = []
# for l in leaderboard:
#     print(repr(l[3]), teams)
#     if l[3] not in teams:
#         teams.add(l[3])
#         filtered.append(l)

print("\n".join(["   ".join(l) for l in leaderboard]))