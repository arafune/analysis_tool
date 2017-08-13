
#!/usr/bin/env python3
# modified script
import numpy as np
import matplotlib.pyplot as plt
def H(kx,ky,delta):
    return np.array([[delta/2.0, kx-ky*1.0j],[kx+ky*1.0j, -delta/2.0]])
numk = 500
deltak=0.001
gap=0.5
path=np.linspace(-np.pi, np.pi, numk)
hams = np.array([H(kpt, 0.0, gap) for kpt in path])
eigens= np.linalg.eig(hams)
eigenc = np.real(eigens[0][:, 0])
eigenv = np.real(eigens[0][:, 1])  
hamdeltax = np.array([H(kpt+deltak, 0.0, gap) for kpt in path])
hamdeltay = np.array([H(kpt, deltak, gap) for kpt in path])
eigens_x = np.linalg.eig(hamdeltax)
eigens_y = np.linalg.eig(hamdeltay)
dux = (eigens_x[1] - eigens[1])/deltak
duy = (eigens_y[1] - eigens[1])/deltak
dux_c = dux[:, 0]
dux_v = dux[:, 1]
duy_c = duy[:, 0]
duy_v = duy[:, 1]
#cur_c = np.imag(np.diag(-2.0 * np.dot(np.conjugate(dux_c), duy_c.T)))
#cur_v = np.imag(np.diag(-2.0 * np.dot(np.conjugate(dux_v), duy_v.T)))
cur_c = np.imag(-2.0 * np.einsum('ij, ij -> i', np.conjugate(dux_c), duy_c))
cur_v = np.imag(-2.0 * np.einsum('ij, ij -> i', np.conjugate(dux_v), duy_v))
plt.plot(path,eigenc,label="conduction")
plt.plot(path,eigenv,label="valence")
plt.plot(path,cur_v,label="Berry conduction")
plt.plot(path,cur_c, label="Berry valence")
plt.legend()
plt.show()
