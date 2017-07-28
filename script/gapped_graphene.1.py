
import math
import numpy as np
#import matplotlib.pyplot as plt

def H(kx,ky,delta):
    return np.array([[delta/2.0, kx-ky*1.0j],[kx+ky*1.0j, -delta/2.0]])

eigenv=[]
eigenc=[]
curv_v=[]
curv_c=[]

numk = 500
deltak=0.001
gap=0.5
path=np.linspace(-math.pi, math.pi, numk);

for kpt in path:

    ham=H(kpt,0.0,gap)
    eig, l=np.linalg.eig(ham)

    eigenc.append(eig[0].real)
    eigenv.append(eig[1].real)

    #try to evaluate Berry curv by differential

    dkx=kpt+deltak
    dky=deltak
    hamdeltax=H(dkx,0.0,gap)

    eigdeltax,ldeltax=np.linalg.eig(hamdeltax)
    hamdeltay=H(kpt,dky,gap)

    eigdeltay,ldeltay=np.linalg.eig(hamdeltay)

    dux_c=(ldeltax[:,0]-l[:,0])/deltak
    duy_c=(ldeltay[:,0]-l[:,0])/deltak

    dux_v=(ldeltax[:,1]-l[:,1])/deltak
    duy_v=(ldeltay[:,1]-l[:,1])/deltak




    curv_v.append(-2.0*np.dot(np.conjugate(dux_c),duy_c).imag)
    curv_c.append(-2.0*np.dot(np.conjugate(dux_v),duy_v).imag)
