import random
from collections import Counter

z = [2,1,0]
T= [0.5,1,2,100000]


def softmax(z, T):
    import math
    exp_z = [math.exp(zi / T) for zi in z]
    sum_exp_z = sum(exp_z)
    return [e / sum_exp_z for e in exp_z]

for t in T:
    print(f"Softmax with T={t}: {softmax(z, t)}")


def sample(p):
    u =random.random()
    cumulative = 0
    for i, pi in enumerate(p):
        cumulative += pi
        if u < cumulative:
            return i
    return len(p) - 1
# Example usage of sample function
counts = Counter(sample([0.6,0.3,0.1]) for _ in range(10000))
print(f"Sample counts: {counts}")