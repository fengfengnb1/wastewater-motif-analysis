import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import stumpy
from matplotlib.patches import Rectangle
from defperiod import calculate_period

df = pd.read_csv(r"D:\Vertiefung\close loop data\reac5_cl.csv")

start_time = 0
end_time = 7
length = df.shape[0]
times = np.linspace(start_time, length / (24 * 4), length)
df['time'] = times
df = df.set_index('time')

days = 7
time_per_day = 24 * 4  # 每天的时间步长（假设每小时有4个数据点）
end_index = days * time_per_day
new_columns = ['FR', 'SNH', 'SO']
#New_data = df([new_columns], [:end_index])
New_data = df[new_columns]
New_data = New_data.head(end_index)
for column in New_data.columns:
    m1, _ = calculate_period(New_data[column])
    signal_without_mean = New_data[column] - New_data[column].mean()

    # 计算矩阵 mp1
    mp1 = stumpy.stump(signal_without_mean, m=m1)

    # min_value_idx = mp1.idxmin()
    #max_value_idx = mp1.idxmax()
    # 确定最小值的索引位置
    motif_idx_temp1 = np.argmin(mp1[:, 0])
    motif_idx1 = motif_idx_temp1 / (4 * 24)

    # 确定最大值的索引位置
    motif_idx_temp2 = np.argmax(mp1[:, 0])
    motif_idx2 = motif_idx_temp2 / (4 * 24)

    print(f"The motif for {column} with m1={m1} is located at index {motif_idx1}")
    print(f"The maximum value in the matrix profile for {column} with m1={m1} is located at index {motif_idx2}")

    max_value = New_data[column].max()

    fig, axs = plt.subplots(2, figsize=(15, 10))
    plt.suptitle(column)
    axs[0].plot(New_data.index, New_data[column].values, color='blue')
    axs[0].set_xlim(start_time, end_time)
    axs[0].set_ylim(New_data[column].min(), New_data[column].max())
    axs[0].set_ylabel('Steam Flow', fontsize=20)

    rect1 = Rectangle((motif_idx1, 0), m1 / (4 * 24), max_value, facecolor='lightgrey', label=f'm1={m1}h')
    axs[0].add_patch(rect1)
    axs[0].legend()

    axs[1].set_xlim(start_time, end_time)
    axs[1].set_xlabel('Time', fontsize=20)
    axs[1].set_ylabel('Matrix Profile', fontsize=20)
    axs[1].plot(New_data.index[:len(mp1)], mp1[:, 0], color='green', label=f'm1={m1}h')
    axs[1].axvline(x=motif_idx1, linestyle="--", color="y", label='Min Value')
    axs[1].axvline(x=motif_idx2, linestyle="--", color="r", label='Max Value')

    axs[1].legend()

    plt.tight_layout()
    plt.show()
