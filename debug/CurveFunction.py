#This source code is able to freely use for Blender and users.

import numpy as np
#
# Ellipse_Curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def ellipse_curve(param):
    t = param[0] 
    p = np.sin(t * 0.5 * np.pi)
    q = np.cos(t * 0.5 * np.pi)
    return p,q
#
# parabola_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def parabola_curve(param):
    x = param[0]
      
    p = x
    q = 1.0 - x*x
    return p,q
#
# circle_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def circle_curve(param):
    t0 = param[0]
    P  = param[1]
    Q  = param[2]

    if abs(Q) > 0.0001:
        R = P/Q
    else:
        R = 1.0
    
    Qr = 0.5*(R*R+1.0)
    Pr = 0.5*(R*R+1.0) / R
    y  = 0.5*(R*R-1.0)

    T = np.arccos((R*R - 1.0)/(R*R + 1.0))
    
    t = t0 * T 
    p = Pr * np.sin(t)
    q = Qr * np.cos(t) - y

    return p,q
#
# cos_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def cos_curve(param):
    t = param[0]
    p = t
    q = np.float(np.cos(0.5*t*np.pi))
    return p, q
#
# cos2_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def cos2_curve(param):
    t = param[0]
    p = t
    q = np.cos(0.5*t*np.pi)

    type(p)
    return p, q**2
#
# cos3_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def cos3_curve(param):
    t = param[0]
    p = t
    q = np.cos(0.5*t*np.pi)
    return p, q**3
#
# asteroid_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def asteroid_curve(param):
    t = param[0]
    p = (np.sin(t * np.pi*0.5))**3.0
    q = (np.cos(t * np.pi*0.5))**3.0
    return p,q
#
# gaussian_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Top direction
def gaussian_curve(param):
    t = param[0]
    d = param[3]

    p = t
    r = 0
    if d > 0:
        r = np.log(1.0/(1.0+d))*t*t
    q = np.exp(r)
    return p,q
