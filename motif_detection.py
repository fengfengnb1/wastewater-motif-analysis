import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import stumpy
from matplotlib.patches import Rectangle
from defperiod import calculate_period

df = pd.read_csv(r"D:\Vertiefung\close loop data\reac5_cl.csv")
start_time = 245
end_time = 609
length = df.shape[0]
times = np.linspace(start_time, end_time, length)
df['time'] = times
df = df.set_index('time')

for column in df.columns:
    m1, m2 = calculate_period(df[column])
    signal_without_mean = df[column] - df[column].mean()

    # 计算矩阵 mp
    mp1 = stumpy.stump(signal_without_mean, m=m1)
    mp2 = stumpy.stump(signal_without_mean, m=m2)

    # 确定主题的索引位置，找到具有最小值的索引位置
    motif_idx1_temp = np.argsort(mp1[:, 0])[0]
    motif_idx1 = motif_idx1_temp / (4 * 24)
    motif_idx2_temp = np.argsort(mp2[:, 0])[0]
    motif_idx2 = motif_idx2_temp / (4 * 24)

    print(f"The motif for {column} with m1={m1} is located at index {motif_idx1}")
    print(f"The motif for {column} with m2={m2} is located at index {motif_idx2}")

    max_value_1 = df[column].max()
    max_value = max_value_1

    fig, axs = plt.subplots(2, figsize=(15, 10))
    plt.suptitle(column)
    axs[0].plot(df.index, df[column].values, color='blue')
    axs[0].set_xlim(start_time, end_time)
    axs[0].set_ylabel('Steam Flow', fontsize=20)
    rect1 = Rectangle((df.index[motif_idx1_temp], 0), m1 / (4 * 24), max_value, facecolor='lightgrey',
                      label=f'm1={m1}h')
    rect2 = Rectangle((df.index[motif_idx2_temp], 0), m2 / (4 * 24), max_value, facecolor='lightblue',
                      label=f'm2={m2}h')
    axs[0].add_patch(rect1)
    axs[0].add_patch(rect2)
    axs[0].legend()
    axs[1].set_xlim(start_time, end_time)
    axs[1].set_xlabel('Time', fontsize=20)
    axs[1].set_ylabel('Matrix Profile', fontsize=20)
    axs[1].plot(df.index[:len(mp1)], mp1[:, 0], color='green', label=f'm1={m1}h')
    axs[1].plot(df.index[:len(mp2)], mp2[:, 0], color='orange', label=f'm2={m2}h')

    axs[1].axvline(x=df.index[motif_idx1_temp], linestyle="--", color="yellow", label='Motif 1')
    axs[1].axvline(x=df.index[motif_idx2_temp], linestyle="--", color="red", label='Motif 2')
    axs[1].legend()

    plt.tight_layout()
    plt.show()
    fig.savefig(column)
