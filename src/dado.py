import random
def dev_dado_A():
    return random.randint(1,6)

def dev_dado_B():
    return random.randint(1,6)

print('El valor del dado A: {0:1}'.format(str(dev_dado_A())))
print('El valor del dado B: {0:1}'.format(str(dev_dado_B())))