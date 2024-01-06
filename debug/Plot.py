import matplotlib.pylab as plt
import numpy as np
import CurveFunction as cf

c1,c2,c3,c4 = "blue","green","red","black"      # 各プロットの色
segment = 16
# x = np.linspace(-np.pi, np.pi, 201)
t = np.linspace(0, 1.0, segment)
param = [t, 10, 15, segment] 
p1,q1 = cf.cos2_curve(param)
#p2,q2 = cf.gaussian_curve(param)
#p3,q3 = cf.cos3_curve(param)
plt.plot(p1, q1, c1)
#plt.plot(p2, q2, c2)
#plt.plot(p3, q3, c3)
plt.xlabel('p')
plt.ylabel('q')
plt.axis('tight')
plt.show()