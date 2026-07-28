import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
#B=pd.read_excel("data.xlsx")
#B为所接收数据 下为示例
B = np.array([
[0.1,0.2,0.3,0.5,0.8,0.5,0.3,0.2,0.1],
[0.2,0.4,0.7,1.0,1.4,1.0,0.7,0.4,0.2],
[0.3,0.7,1.3,2.0,2.8,2.0,1.3,0.7,0.3],
[0.5,1.0,2.0,3.5,4.8,3.5,2.0,1.0,0.5],
[0.8,1.4,2.8,4.8,6.5,4.8,2.8,1.4,0.8],
[0.5,1.0,2.0,3.5,4.8,3.5,2.0,1.0,0.5],
[0.3,0.7,1.3,2.0,2.8,2.0,1.3,0.7,0.3],
[0.2,0.4,0.7,1.0,1.4,1.0,0.7,0.4,0.2],
[0.1,0.2,0.3,0.5,0.8,0.5,0.3,0.2,0.1]
])

plt.figure(figsize=(6,5))
plt.imshow(B,
           cmap='jet',
           origin='lower')
plt.colorbar(label='Magnetic Flux Density (mT)')
plt.title("2D Leakage Magnetic Field")
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.show()

x=np.arange(9)
y=B[4,:]
def gaussian(x,a,x0,sigma,c):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))+c
popt,_=curve_fit(
    gaussian,
    x,
    y,
    p0=[6,4,1,0]
)

plt.scatter(x,y,label='Measure')

plt.plot(
    x,
    gaussian(x,*popt),
    'r',
    label='Gaussian Fit'
)

plt.legend()

plt.xlabel("Position")

plt.ylabel("Magnetic Field(mT)")

plt.show()

print("拟合参数：[{:.8f} {:.8f} {:.8f} {:.8f}]".format(
    popt[0], popt[1], popt[2], popt[3]
))

max_B=np.max(B)
print("最大漏磁值：",max_B)

index=np.unravel_index(
    np.argmax(B),
    B.shape
)
row, col = np.unravel_index(np.argmax(B), B.shape)
print("缺陷位置：({}, {})".format(int(row), int(col)))
#漏磁面积
threshold=2
area=np.sum(B>threshold)
print("漏磁面积:",area)

#梯度分析
gx,gy=np.gradient(B)
plt.imshow(
    np.sqrt(gx**2+gy**2),
    cmap='jet'
)
plt.colorbar()
plt.title("Gradient")
plt.show()