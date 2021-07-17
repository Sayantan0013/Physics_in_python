import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

s = 20
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-s, s), ylim=(-s,s))
ax.set_aspect('equal')
ax.grid()
xdata, ydata = 0, 0
p1, = plt.plot([], [], 'o-',lw=2)
p2, = plt.plot([], [], 'o-',lw=2)
p3, = plt.plot([], [], 'o-',lw=2)
line1, = plt.plot([],[],'r',lw=1)
line2, = plt.plot([],[],'r',lw=1)
line3, = plt.plot([],[],'r',lw=1)

G = 30
t_stop = 120

M = [2,1,5]

def derive(state,t):
    dydx = np.zeros_like(state)
    d1 = np.sqrt((state[0]-state[2])**2 + (state[1]-state[3])**2)
    d2 = np.sqrt((state[0]-state[4])**2 + (state[1]-state[5])**2)
    d3 = np.sqrt((state[4]-state[2])**2 + (state[5]-state[3])**2)
    #print(d)
    dydx[:6] = state[-6:]
    dydx[6:8] = G*(M[1]*np.array([state[2]-state[0],state[3]-state[1]])/(d1**3)+
                M[2]*np.array([state[4]-state[0],state[5]-state[1]])/(d2**3)
                )
    dydx[8:10] = G*(M[0]*np.array([state[0]-state[2],state[1]-state[3]])/(d1**3)+
                M[2]*np.array([state[4]-state[2],state[5]-state[3]])/(d3**3)
                )
    dydx[10:] = G*(M[0]*np.array([state[0]-state[4],state[1]-state[5]])/(d2**3)-
                M[1]*np.array([state[4]-state[2],state[5]-state[3]])/(d3**3)
                )
    return dydx

dt = 0.01
t = np.arange(0, t_stop, dt)

r3 = np.sqrt(3)
v = 6/8
state = [-4,0,4,0,0,0,0,-1-v,0,3-v,0,1-v]

state =np.array(state)
state[-6:] = 2*state[-6:]

y = odeint(derive,state,t)

x1 = y[:,0]
y1 = y[:,1]
x2 = []
y2 = []
x3 = y[:,2]
y3 = y[:,3]
x4 = []
y4 = []
x5 = y[:,4]
y5 = y[:,5]
x6 = []
y6 = []

def update(i):
    x2.append(x1[i])
    y2.append(y1[i])
    x4.append(x3[i])
    y4.append(y3[i])
    x6.append(x5[i])
    y6.append(y5[i])
    l = 200
    line1.set_data(x2[-l:],y2[-l:])
    line2.set_data(x4[-l:],y4[-l:])
    line3.set_data(x6[-l:],y6[-l:])
    p1.set_data(x1[i],y1[i])
    p2.set_data(x3[i],y3[i])
    p3.set_data(x5[i],y5[i])
    return p1,p2,p3,line1,line2,line3

th = np.linspace(0, 2*np.pi, 400)


#ax.plot(np.sin(th),np.cos(th),'k')

ani = FuncAnimation(
    fig, update, len(y), interval=dt*1000, blit=True,repeat = False)




#ani.save('planet_rozha.mp4')
plt.show()