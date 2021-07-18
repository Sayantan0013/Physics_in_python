import numpy as np
import random
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy.core.fromnumeric import shape
from scipy.integrate import odeint

s = 2
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-s, s), ylim=(-s,s))
ax.set_aspect('equal')
ax.grid()

class Point():
    dt = 0.01
    t = 0.1
    def __init__(self,x,y,dx=0,dy=0,m=1) -> None:
        self.m = m              # Mass of particle
        self.x,self.y = x,y     # Position of the paritcle
        self.dx,self.dy = dx,dy # Velocity of the particle
    def derive(self,state,t):
        dydx = np.zeros(6)
        dydx[:4] =state[2:]
        return dydx
    def update(self,F):
        state = np.array([self.x,self.y,self.dx,self.dy,*F])
        y = odeint(self.derive,state,np.arange(0,self.t,self.dt))
        #print(y.shape)
        self.x,self.y,self.dx,self.dy = y[-1,:4]

        

class space():
    def __init__(self, p = None) -> None:   # Initiating the particles 
        if p ==None:
            self.particle = []
            self.forces = []
            self.plots = []
        else:
            self.particle = p   # Creating a world containing all the given points
            self.forces = np.zeros((len(p),2))
            self.plots = []
            for i in p:
                self.plots.append(plt.plot([],[],'.'))
    def gravity(self,G):                      # function for gravitaion 
        for i,p in enumerate(self.particle):
            for j,q in enumerate(self.particle):
                if(i!=j):
                    d = np.sqrt((q.x-p.x)**2 + (q.y-p.y)**2)
                    self.forces[i] += G*q.m*np.array([q.x-p.x,q.y-p.y])/d**3
    def central(self,mag,cx=0,cy=0):        # function for central forces 
        for i,p in enumerate(self.particle):
            self.forces[i] = mag*(cx-p.x),mag*(cy-p.y)
    def __call__(self):                     # This function apply forces on the perticle
        #time.sleep(0.01)
        self.central(1)
        self.gravity(0.01)
        for i,p in enumerate(self.particle):
            p.update(self.forces[i])
        self.forces.fill(0)
        return self.particle
    def animate(self,args):
        for i,p in enumerate(args):
            self.plots[i][0].set_data([p.x],[p.y])
        return self.plots


p1 = Point(0,0)
p2 = Point(1,0)
p3 = Point(1,1)
p4 = Point(0,1)
p5 = Point(1/2,1/2)
uni = space([p2])


def frames():
    while True:
        yield uni()
anim = FuncAnimation(fig, uni.animate, frames=frames, interval=10)
plt.show()
