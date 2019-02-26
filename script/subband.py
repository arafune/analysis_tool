#!/usr/bin/env python3
'''
Created on 2017/07/24

@author: Emi Minamitani
Harper-Hofstdater Hamiltonian
For simplicity, I set lattice constant a=1.0 & p=1
therefore \alpha=p/q is just set to 1/q
'''
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from numpy import meshgrid


#
#
def Hamiltonian(q, kx, ky, J):
    ham = np.zeros((q, q), dtype=np.complex)
    ham[range(q), range(q)] = -J * 2.0 * np.cos(
        [kx - float(i) * 2.0 * np.pi / float(q) for i in range(q)])
    ham[range(1, q - 1), range(2, q)] = -J * np.exp(ky * 1.0j)
    ham[range(1, q - 1), range(0, q - 2)] = -J * np.exp(-ky * 1.0j)
    #
    ham[0][q - 1] = -J * np.exp(-ky * 1.0j)
    ham[q - 1][0] = -J * np.exp(ky * 1.0j)
    ham[0][1] = -J * np.exp(ky * 1.0j)
    ham[q - 1][q - 2] = -J * np.exp(-ky * 1.0j)
    return ham


q = 6

#check the band degeneracy corresponds to Landau level
ky = np.pi / float(q)
#ky=0.0
#eigenvalue should be degenerate for kx=kx+2pi*n/q

eigen = []
hams = np.array([
    Hamiltonian(q, -2.0 / float(q) * float(i) * np.pi + np.pi / float(q), ky,
                0.1) for i in range(q + 1)
])
ls = np.linalg.eigvalsh(hams, UPLO='L')
print(hams.shape)
for i in range(q + 1):
    kx = -2.0 / float(q) * float(i) * np.pi + np.pi / float(q)
    ham = Hamiltonian(q, kx, ky, 0.1)
    l = np.linalg.eigvalsh(ham, UPLO='L')
    print('kx=' + str(kx) + '  ky=' + str(ky))
    print(l)
    eigreal = []
    for j in range(q):
        eigreal.append(l[j].real)

    eigen.append(sorted(eigreal))
#degeneracy condition seems to be satisfied
ksample = 50
kxmesh = np.linspace(-np.pi, np.pi, ksample)
kymesh = np.linspace(-np.pi / float(q), np.pi / float(q), ksample)

X, Y = np.meshgrid(kxmesh, kymesh)

eigen = []

for kx in kxmesh:
    for ky in kymesh:
        ham = Hamiltonian(q, kx, ky, -0.2)
        #print(ham)
        l = np.linalg.eigvalsh(ham, UPLO='L')
        tmp = []
        for i in l:
            tmp.append(i.real)
        sortedval = sorted(tmp)
        #print(sortedval)
        eigen.append(sortedval)

Ztot = []
for i in range(q):
    Z = []
    counter = 0
    for ikx in range(len(kxmesh)):
        eigentmp = []
        for iky in range(len(kymesh)):
            eigentmp.append(eigen[counter][i])
            counter = counter + 1

        Z.append(eigentmp)
    Ztot.append(Z)

fig = plt.figure()
ax = fig.gca(projection='3d')
for i in range(q):
    surf = ax.plot_surface(
        X,
        Y,
        np.transpose(Ztot[i]),
        rstride=1,
        cstride=1,
        cmap='coolwarm',
        linewidth=0,
        alpha=0.4,
        antialiased=False)

title = "energy spectrum"
plt.title(title)
plt.show()
plt.close()
