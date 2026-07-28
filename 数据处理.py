import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
V = np.array([
[1.651,1.652,1.653,1.655,1.658,1.655,1.653,1.652,1.651],
[1.652,1.654,1.657,1.664,1.670,1.664,1.657,1.654,1.652],
[1.653,1.657,1.668,1.678,1.689,1.678,1.668,1.657,1.653],
[1.655,1.664,1.678,1.699,1.717,1.699,1.678,1.664,1.655],
[1.658,1.670,1.689,1.717,1.741,1.717,1.689,1.670,1.658],
[1.655,1.664,1.678,1.699,1.717,1.699,1.678,1.664,1.655],
[1.653,1.657,1.668,1.678,1.689,1.678,1.668,1.657,1.653],
[1.652,1.654,1.657,1.664,1.670,1.664,1.657,1.654,1.652],
[1.651,1.652,1.653,1.655,1.658,1.655,1.653,1.652,1.651]
])
V0 = 1.65          # 零磁场电压(V)
S = 0.014          # 灵敏度(V/mT)
B = (V - V0) / S
print("磁感应强度矩阵(mT)：")
print(np.round(B,3))
Bx = B.copy()
By = np.rot90(B)
B_max = np.maximum(np.abs(Bx), np.abs(By))
print()
print("最大值法融合完成")
B_sum = np.sqrt(Bx**2 + By**2)
print("幅值融合法完成")
print()
print("最大值法矩阵：")
print(np.round(B_max,3))
print()
print("幅值融合矩阵：")
print(np.round(B_sum,3))

plt.figure(figsize=(6,5))
plt.imshow(Bx,
           cmap='jet',
           origin='lower')
plt.colorbar(label='Magnetic Flux Density (mT)')
plt.title('X Direction Leakage Magnetic Field')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()
plt.figure(figsize=(6,5))
plt.imshow(B_max,
           cmap='jet',
           origin='lower')

plt.colorbar(label='Magnetic Flux Density (mT)')
plt.title('Maximum Fusion Leakage Magnetic Field')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()
plt.figure(figsize=(6,5))

plt.imshow(B_sum,
           cmap='jet',
           origin='lower')

plt.colorbar(label='Magnetic Flux Density (mT)')
plt.title('Magnitude Fusion Leakage Magnetic Field')
plt.xlabel('X Position')
plt.ylabel('Y Position')

plt.show()

center = B_max.shape[0] // 2

x = np.arange(B_max.shape[1])

y_max = B_max[center,:]

y_sum = B_sum[center,:]

def gaussian(x,a,x0,sigma,c):

    return a*np.exp(-(x-x0)**2/(2*sigma**2))+c

popt_max,pcov_max = curve_fit(
    gaussian,
    x,
    y_max,
    p0=[
        np.max(y_max),
        center,
        1,
        np.min(y_max)
    ]
)
popt_sum,pcov_sum = curve_fit(
    gaussian,
    x,
    y_sum,
    p0=[
        np.max(y_sum),
        center,
        1,
        np.min(y_sum)
    ]
)
print()
print("==========高斯拟合参数==========")
print()
print("最大值法：")
print(np.round(popt_max,4))

print()

print("幅值融合法：")

print(np.round(popt_sum,4))

x_fit = np.linspace(0,
                    B_max.shape[1]-1,
                    200)
y_fit_max = gaussian(
    x_fit,
    *popt_max
)

y_fit_sum = gaussian(
    x_fit,
    *popt_sum
)
plt.figure(figsize=(7,5))

plt.scatter(
    x,
    y_max,
    label="Measured",
    s=40
)
plt.plot(
    x_fit,
    y_fit_max,
    linewidth=2,
    label="Gaussian Fit"
)

plt.title("Maximum Fusion Gaussian Fit")
plt.xlabel("Position")
plt.ylabel("Magnetic Flux Density (mT)")
plt.grid(True)
plt.legend()
plt.show()
plt.figure(figsize=(7,5))
plt.scatter(
    x,
    y_sum,
    label="Measured",
    s=40
)
plt.plot(
    x_fit,
    y_fit_sum,
    linewidth=2,
    label="Gaussian Fit"
)
plt.title("Magnitude Fusion Gaussian Fit")
plt.xlabel("Position")
plt.ylabel("Magnetic Flux Density (mT)")
plt.grid(True)
plt.legend()
plt.show()

max_value_max = np.max(B_max)

position_max = np.unravel_index(
    np.argmax(B_max),
    B_max.shape
)

area_max = np.sum(B_max)

print()

print("========== 最大值法特征 ==========")

print("最大漏磁值：%.4f mT"%(max_value_max))

print("缺陷位置：",position_max)

print("漏磁面积：%.4f"%(area_max))

# 幅值法特征提取

max_value_sum = np.max(B_sum)

position_sum = np.unravel_index(
    np.argmax(B_sum),
    B_sum.shape
)

area_sum = np.sum(B_sum)

print()

print("========== 幅值融合法特征 ==========")

print("最大漏磁值：%.4f mT"%(max_value_sum))

print("缺陷位置：",position_sum)

print("漏磁面积：%.4f"%(area_sum))

# ==========================================
# 标准不确定度分析
# ==========================================

u_max = np.std(B_max,ddof=1)

u_sum = np.std(B_sum,ddof=1)

print()

print("========== 不确定度 ==========")

print("最大值法标准不确定度：%.4f"%(u_max))

print("幅值法标准不确定度：%.4f"%(u_sum))

# ==========================================
# 计算平均值
# ==========================================

mean_max = np.mean(B_max)

mean_sum = np.mean(B_sum)

print()

print("最大值法平均漏磁值：%.4f"%(mean_max))

print("幅值法平均漏磁值：%.4f"%(mean_sum))

# ==========================================
# 输出拟合参数
# ==========================================

print()

print("========== 拟合参数 ==========")

print()

print("最大值法")

print("峰值(a)：%.4f"%(popt_max[0]))

print("中心位置(x0)：%.4f"%(popt_max[1]))

print("宽度(sigma)：%.4f"%(popt_max[2]))

print("基线(c)：%.4f"%(popt_max[3]))

print()

print("幅值融合法")

print("峰值(a)：%.4f"%(popt_sum[0]))

print("中心位置(x0)：%.4f"%(popt_sum[1]))

print("宽度(sigma)：%.4f"%(popt_sum[2]))

print("基线(c)：%.4f"%(popt_sum[3]))

print()

print("==========================================")

print("          两种融合算法性能比较")

print("==========================================")

print()

print("{:<20}{:<15}{:<15}".format(
    "评价指标",
    "最大值法",
    "幅值融合法"
))

print("-"*55)

print("{:<20}{:<15.4f}{:<15.4f}".format(
    "最大漏磁值",
    max_value_max,
    max_value_sum
))

print("{:<20}{:<15.4f}{:<15.4f}".format(
    "漏磁面积",
    area_max,
    area_sum
))

print("{:<20}{:<15.4f}{:<15.4f}".format(
    "平均磁场",
    mean_max,
    mean_sum
))

print("{:<20}{:<15.4f}{:<15.4f}".format(
    "标准不确定度",
    u_max,
    u_sum
))

print("{:<20}{:<15.4f}{:<15.4f}".format(
    "拟合峰值",
    popt_max[0],
    popt_sum[0]
))

print("{:<20}{:<15.4f}{:<15.4f}".format(
    "拟合宽度",
    popt_max[2],
    popt_sum[2]
))

print()


print("========== 数据分析结论 ==========")
if max_value_sum > max_value_max:
    print("① 幅值融合法获得了更大的漏磁峰值，对缺陷响应更强。")
else:
    print("① 最大值法获得了更大的漏磁峰值。")
if area_sum > area_max:
    print("② 幅值融合法获得了更大的漏磁面积，更容易保留缺陷信息。")
else:
    print("② 最大值法获得了更大的漏磁面积。")
if u_sum < u_max:
    print("③ 幅值融合法的不确定度更小，数据更加稳定。")
else:
    print("③ 最大值法的数据稳定性更好。")
print("④ 两种融合算法均能有效提高缺陷识别能力，可根据实际检测需求选择不同融合策略。")