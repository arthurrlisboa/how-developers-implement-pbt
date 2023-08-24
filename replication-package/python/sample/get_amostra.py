import numpy as np
from obtem_distribuicao import calcular_distribuicao

def has_duplicates(lst):
    return len(lst) != len(set(lst))


def obter_amostra_rand():
    sample = np.random.choice(np.arange(1, 764), size=86, replace=False)
    print(sorted(sample))
    print(has_duplicates(sample))
    calcular_distribuicao(sample)

obter_amostra_rand()