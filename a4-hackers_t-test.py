import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

sns.set_style('whitegrid')
sns.set_palette('deep')

# Create a couple of colors to use throughout the notebook
red = sns.xkcd_rgb['vermillion']
blue = sns.xkcd_rgb['dark sky blue']

def plot_results(differences, diff_measured, p_value):

    fig, ax = plt.subplots()

    ax.hist(differences, bins=50, color=blue)
    # self.ax.set_xlim([-20, 20])
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    # xmin, xmax, ymin, ymax = plt.axis()

    ax.plot((diff_measured, diff_measured), (0, ymax), color=red)
    ax.annotate('{:3.1f}%'.format(p_value * 100), 
                    xytext=(diff_measured + (xmax-diff_measured)*0.5, ymax//2), 
                    xy=(diff_measured, ymax//2), 
                    multialignment='right',
                    va='center',
                    color=red,
                    size='large',
                    arrowprops={'arrowstyle': '<|-', 
                                'lw': 2, 
                                'color': red, 
                                'shrinkA': 10})
    ax.set(xlabel='score difference', ylabel='number')
    ax.grid(b=True)
    plt.show()

df = pd.read_csv('sneetches.txt')

label = df['star'].values.copy()
diff_measured =df[label == 1]['measurement'].mean() - df[label == 0]['measurement'].mean() 

differences = []
num_simulations = 10000
for i in range(num_simulations):
    np.random.shuffle(label)
    group_1_mean = df[label == 1]['measurement'].mean()
    group_0_mean = df[label == 0]['measurement'].mean()
    differences.append(group_1_mean - group_0_mean)

p_value = sum(diff >= diff_measured for diff in differences) / num_simulations
plot_results(differences, diff_measured, p_value)