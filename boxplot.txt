import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df =pd.read_csv(r"D:\Vertiefung\open loop data\ASinput_ol.csv")
print(df.head())

steps_part1 = 244
steps_part2 = 365

df_part1 = df[df.index <= steps_part1]
df_part2 = df[(df.index > steps_part1) & (df.index <= steps_part1 + steps_part2)]

for column in df.columns:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(x='step', y=column, data=pd.concat([df_part1.assign(step='Steps 0-{0}'.format(steps_part1)),
                                                    df_part2.assign(step='Steps {0}-{1}'. format(steps_part1 + 1,
                                                                                                 steps_part1 + steps_part2))]),
                ax=ax, width=0.4)
    ax.set_title(column)
    plt.show()
