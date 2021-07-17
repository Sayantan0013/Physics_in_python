import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint

fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-10, 10), ylim=(-10, 10))
ax.set_aspect('equal')
ax.grid()
xdata, ydata = 0, 0
ln, = plt.plot([], [], 'o-',lw=2)
line, = plt.plot([],[],'r',lw=1)

M = 1.0
g = 9.8
L = 5.0
k = 5
t_stop = 100

def derive(state,t):
    dydx = np.zeros_like(state)
    dydx[0] = state[1]
    dydx[1] = -k*((state[0])-L)-g*np.cos(state[2])
    dydx[3] = (g/(state[0]))*np.sin(state[2])
    dydx[2] = state[3]
    return dydx

dt = 0.02
t = np.arange(0, t_stop, dt)


state = [L,0.0,np.radians(170.0),np.radians(0.0)]

y = odeint(derive,state,t)

x1 = y[:,0]*np.sin(y[:, 2])
y1 = y[:,0]*np.cos(y[:, 2])
x2 = []
y2 = []

def update(i):
    xdata=[0,x1[i]]
    ydata=[0,y1[i]]
    x2.append(x1[i])
    y2.append(y1[i])
    line.set_data(x2,y2)
    ln.set_data(xdata, ydata)
    return ln,line

th = np.linspace(0, 2*np.pi, 400)


#ax.plot(np.sin(th),np.cos(th),'k')

ani = FuncAnimation(
    fig, update, len(y), interval=dt*1000, blit=True,repeat = False)




#ani.save('single_pendulum2.mp4')
plt.show()