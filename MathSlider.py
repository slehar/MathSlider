# -*- coding: utf-8 -*-
"""
MathSlider.py

Created on Wed Dec 28 07:45:24 2016

@author: slehar
"""

import matplotlib.pyplot as plt
from   matplotlib.widgets import Slider
from matplotlib.widgets import RadioButtons
from   matplotlib import animation
import numpy as np
import sys
from collections import deque

x = 0.001
t = 0.
lastX = 0.
lastT = 0.
dt = .5
dArrayPos = deque([0.])
dArrayVel = deque([0.])
dArrayAcc = deque([0.])
tArray    = deque([0.])
plotHeight = 30

# Open figure window
winXSize = 10
winYSize = 6
winAspect = winXSize/winYSize
plt.close('all')
fig = plt.figure(figsize=(winXSize, winYSize))
fig.canvas.set_window_title('MathSlider')

# Keypress 'q' to quit callback function
def press(event):
    global ptList, data
    sys.stdout.flush()
    if event.key == 'q':
        plt.close()

# Connect keypress event to callback function
fig.canvas.mpl_connect('key_press_event', press)

ySpace = np.linspace(.05, .24, 3) # Vertical spacing sliders

# sliders
axSlider1 = fig.add_axes([0.2, ySpace[0], 0.7, 0.05])
axSlider1.set_xticks([])
axSlider1.set_yticks([])

axSlider2 = fig.add_axes([0.2, ySpace[1], 0.7, 0.05])
axSlider2.set_xticks([])
axSlider2.set_yticks([])

axSlider3 = fig.add_axes([0.2, ySpace[2], 0.7, 0.05])
axSlider3.set_xticks([])
axSlider3.set_yticks([])

posSlider = Slider(axSlider1, 'position',     -1., 1., valinit=0.)
velSlider = Slider(axSlider2, 'velocity',     -1., 1., valinit=0.)
accSlider = Slider(axSlider3, 'accel',        -1., 1., valinit=0.)

#posSlider.poly.fill = False
#velSlider.poly.fill = False
#accSlider.poly.fill = False

#posSlider.poly.set_edgecolor('red')
#velSlider.poly.set_edgecolor('green')
#accSlider.poly.set_edgecolor('blue')

posSlider.poly.set_facecolor('red')
velSlider.poly.set_facecolor('green')
accSlider.poly.set_facecolor('blue')

#posSlider.poly.set_linewidth(3)
#velSlider.poly.set_linewidth(3)
#accSlider.poly.set_linewidth(3)

(pos, vel, acc) = (posSlider.val, velSlider.val, accSlider.val)

lastUpdated = None

def updatePos(val):
    global  lastUpdated
    lastUpdated = posSlider

def updateVel(val):
    global lastUpdated
    lastUpdated = velSlider

def updateAcc(val):
    global lastUpdated
    lastUpdated = accSlider

posSlider.on_changed(updatePos)
velSlider.on_changed(updateVel)
accSlider.on_changed(updateAcc)

# Radio buttons to select Pos Vel Acc
rax = plt.axes([0.01, .05, 0.1, 0.25])
radio = RadioButtons(rax, ('Acc', 'Vel', 'Pos'), active=2)
#radio.value_selected = 'Pos'

def radioFunc(label):
    print 'Radio button = %s'%radio.value_selected
radio.on_clicked(radioFunc)

# Global
time = 0.
delT = 0.1
lastPos, lastVel, lastAcc = 0, 0, 0
lastTime = time

# Add axes 2 for plot trace
axTime = fig.add_axes([.1,.4,.8,.5])
axTime.set_ylim(0, 1)
axTime.set_xlim(-1, 1)

t = 0.
dt = .1
x = .1

# Set up plot lines in axes 2
linePos, = axTime.plot(t, pos, color='red',   linewidth=1, 
                 linestyle='-', alpha=1.0)  
lineVel, = axTime.plot(t, vel, color='green', linewidth=1, 
                 linestyle='-', alpha=1.0)  
lineAcc, = axTime.plot(t, acc, color='blue',  linewidth=1, 
                 linestyle='-', alpha=1.0)  

def animate(i):
    global time, t, pos, vel, acc, lastPos, lastVel, lastAcc, lastUpdated

#    time += delT
    if radio.value_selected == 'Pos':
        pos = posSlider.val
        vel = pos - lastPos
        velSlider.set_val(vel)
        acc = vel - lastVel
        accSlider.set_val(acc)
        lastPos, lastVel, lastAcc = pos, vel, acc
        lastUpdated = None
    elif radio.value_selected == 'Vel':
        vel = velSlider.val
        pos += vel * delT
        posSlider.set_val(pos)
        acc = vel - lastVel
        accSlider.set_val(acc)
        lastPos, lastVel, lastAcc = pos, vel, acc
        lastUpdated = None
    elif radio.value_selected == 'Acc':
        acc = accSlider.val
        vel += acc
        velSlider.set_val(vel)
        pos += vel * dt
        posSlider.set_val(pos)
        lastPos, lastVel, lastAcc = pos, vel, acc
    t += dt
    dArrayPos.appendleft(pos)
    if len(dArrayPos) >= plotHeight/dt:
        dArrayPos.pop()
    
    dArrayVel.appendleft(vel)
    if len(dArrayVel) >= plotHeight/dt:
        dArrayVel.pop()

    dArrayAcc.appendleft(acc)
    if len(dArrayAcc) >= plotHeight/dt:
        dArrayAcc.pop()
        
    tArray.appendleft(t)
    if len(tArray) >= plotHeight/dt:
        tArray.pop()
        
    lineAcc.set_data(dArrayAcc, tArray)
    lineVel.set_data(dArrayVel, tArray)
    linePos.set_data(dArrayPos, tArray)
    axTime.axis((-1, 1., t, t-plotHeight))
    plt.pause(.001)
    
anim = animation.FuncAnimation(fig, animate)


# Pop fig window to top]]
figmgr=plt.get_current_fig_manager()
figmgr.canvas.manager.window.raise_()
geom=figmgr.window.geometry()
(xLoc,yLoc,dxWidth,dyHeight)=geom.getRect()
figmgr.window.setGeometry(10,10,dxWidth,dyHeight)




