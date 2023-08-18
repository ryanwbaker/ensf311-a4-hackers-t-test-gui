# GUI Implementation of Hacker's T-Test
# Author: Ryan Baker

import re
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import seaborn as sns

sns.set_style('whitegrid')
sns.set_palette('deep')

# Create a couple of colors to use throughout the notebook
red = sns.xkcd_rgb['vermillion']
blue = sns.xkcd_rgb['dark sky blue']

class TtestFrame(ttk.Frame):
    def __init__(self, parent=None):
        """ Parent object in which entire GUI is kept

        returns: None
        """
        # call parent constructor
        super().__init__(parent)

        # add self to frame with geometry manager
        #  make top level window fill entire frame
        self.grid(sticky='NEWS')
    
        # Frames are nested: tk.frame -> ttk.frame
        # Make ttk.frame fill entire window by making tk.frame fill entire window
        top = self.winfo_toplevel()
        top.grid_rowconfigure(0,weight=1)
        top.grid_columnconfigure(0, weight=1)
        
        # matplotlib related variables: Figure and axes
        self.fig = Figure()
        self.ax = self.fig.add_subplot()

        # create attributes
        self.p_val = tk.StringVar()


        # call make_widgets()
        self.make_widgets()


    
    def make_widgets(self):
        """Creates ttk widgets in the BitFrame object

        self (BitFrame): A BitFrame object

        returns: None
        """
        ttk.Label(self, text="Group A").grid(column=0, row=0)
        ttk.Label(self, text="Group B").grid(column=1, row=0)
        self.grp_a = tk.Text(self, width=35, highlightthickness=2)
        self.grp_a.grid(column=0, row=1, padx=5, pady=5, sticky='NEWS')
        self.grp_b = tk.Text(self, width=35, highlightthickness=2)
        self.grp_b.grid(column=1, row=1, padx=5, pady=5, sticky='NEWS')
        ttk.Button(self, text="Run t-test", command=self.plot_results).grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky='NEWS')
        ttk.Label(self, text="p-value").grid(column=0, row=3, padx=5, pady=5, sticky='E')
        ttk.Entry(self, textvariable=self.p_val).grid(column=1, row=3, padx=5, pady=5, sticky='EW')
        # tk.DrawingArea for matplotlib Figure
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().grid(column=2, row=1, rowspan=3, padx=5, pady=5, sticky='NEWS')
        self.canvas.draw()
        # Navigation Toolbar must be in its own Frame because it uses pack
        toolbar_frame = ttk.Frame(self)
        toolbar_frame.grid(column=2, row=0, padx=5, pady=5, sticky='WE')
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        # grid configuration
        self.grid_columnconfigure(0, weight = 1, minsize=50)
        self.grid_columnconfigure(1, weight = 1, minsize=50)
        self.grid_columnconfigure(2, weight = 4, minsize=250)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1, minsize=50)



    def plot_results(self):
        """ plots results onto matplotlib canvas in GUI
        
        returns: None
        """
        self.ax.clear()
        self.canvas.draw()
        # get and parse data from first Text widget
        vals = [(0,float(i)) for i in re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?',self.grp_a.get("1.0", tk.END+"-1c"))]
        # get, parse, and append data from second Text widget
        vals = vals +[(1,float(i)) for i in re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?',self.grp_b.get("1.0", tk.END))]
        df=pd.DataFrame(vals,columns=['group', 'measurement'])
        label = df['group'].values.copy()
        diff_measured = df[label == 1]['measurement'].mean() - df[label == 0]['measurement'].mean()
        differences = []
        num_simulations = 10000
        for i in range(num_simulations):
            np.random.shuffle(label)
            group_1_mean = df[label == 1]['measurement'].mean()
            group_0_mean = df[label == 0]['measurement'].mean()
            differences.append(group_1_mean - group_0_mean)
        
        p_value = sum(diff >= diff_measured for diff in differences) / num_simulations
        self.p_val.set(p_value)
        self.ax.hist(differences, bins=50, color=blue)
        # self.self.ax.set_xlim([-20, 20])
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        # xmin, xmax, ymin, ymax = plt.axis()

        self.ax.plot((diff_measured, diff_measured), (0, ymax), color=red)
        self.ax.annotate('{:3.1f}%'.format(p_value * 100), 
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
        self.ax.set(xlabel='score difference', ylabel='number')
        self.ax.grid(b=True)
        plt.show()
        self.canvas.draw()
        # warn user if text found
        txt_err = re.findall(r'[a-z]|[A-Z]',self.grp_a.get("1.0", tk.END+"-1c") + self.grp_b.get("1.0", tk.END))
        if (len(txt_err) > 0):
            messagebox.showwarning("Warning", "Warning: Found text in input.")

root = tk.Tk()
TtestFrame(parent=root)
root.title("Hacker's T-test")
root.mainloop()
