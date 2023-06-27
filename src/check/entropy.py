import math

from collections import Counter
from src import colors


def entropy(filename):
    entropy = 0
    counts = Counter()
    
    with open(filename, 'r') as f:
        file = f.read()

    for d in file:
        counts[d]+=1

    probs = [float(c) / len(file) for c in counts.values()]
    probs = [p for p in probs if p > 0.]

    for p in probs:
        entropy -= p * math.log(p, 2)
    
    print(colors.BPurple + "Entropy in file is: {}".format(entropy) + colors.RESET)

