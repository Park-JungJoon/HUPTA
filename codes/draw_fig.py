import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class GenePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def create_kde_plot(self, data, label):
        self.kde_plot = sns.kdeplot(data, shade=True, label=label, ax=self.ax)

    def add_vertical_line(self, position, color='red', linestyle='--', label='Vertical Line'):
        self.ax.axvline(x=position, color=color, linestyle=linestyle, label=label)

path = os.getcwd() + "/media/cv_ts_con_table.tsv"
df = pd.read_csv(path, sep ='\t')

gene_plot = GenePlot()
threshold = np.percentile(df["CV"], 25)
vertical_line_position = float(threshold)
gene_plot.add_vertical_line(vertical_line_position)

gene_plot.fig.savefig("your_file_name.png")

