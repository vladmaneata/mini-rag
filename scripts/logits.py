z = [2,1,0]
T= [0.5,1,2,100000]

def softmax(z, T):
    import math
    exp_z = [math.exp(zi / T) for zi in z]
    sum_exp_z = sum(exp_z)
    return [e / sum_exp_z for e in exp_z]

for t in T:
    print(f"Softmax with T={t}: {softmax(z, t)}")
