import glob
import re
import collections

team_correct = collections.Counter()

for results in glob.glob("results/*/*.txt"):
    with open(results) as f:
        lines = f.readlines()

    # print(lines)
    this_round = set()
    # print(results)
    for line in lines:
        parts = [x.strip() for x in re.split(r" +", line.strip())]

        if parts[3] not in this_round:
            # print(parts)
            if parts[2] == "[CORRECT]":
                team_correct[parts[3]] += 1
                print(line)
                this_round.add(parts[3])
    # print(results, len(this_round))

for k, v in team_correct.items():
    print(f"{k}: {v}")