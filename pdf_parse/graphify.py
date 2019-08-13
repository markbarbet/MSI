import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import graph_parser as gp
import tkinter as tk
import pandas as pd
import pandas as pd
import numpy as np
import skimage
import math
import sys

from tkinter import ttk
from skimage import io

if(len(sys.argv)==1):
    fname = '../data/pdf_data/Hong_2013_ppm.png'
else:
    fname = sys.argv[1].rstrip()
imgCV = io.imread(fname);
    


class Graphify(ttk.Frame):
    def __init__(self):
        super().__init__()
        self.savename = 'test.csv'
        self.initUI()

    def click(self, event):
        self.px = imgCV[event.y, event.x]
        #print(self.px)
        self.pos = [event.y, event.x]
        #print(self.pos)
        self.pname.set("Color %d %d %d" % (self.px[0], self.px[1], self.px[2]))
        self.lname.set("Location %d %d" % (self.pos[0], self.pos[1]))         


    def calc_graph(self):
        #if(not self.x[0].get().replace('.','',1).isdigit() or not self.x[1].get().replace('.','',1).isdigit()):
         #   print("X Range needs to be number")
         #   return
        #if(not self.y[0].get().replace('.','',1).isdigit() or not self.y[1].get().replace('.','',1).isdigit()):
         #   print("Y Range needs to be number")
          #  return
    
        if(self.spath.get().replace(' ','')):
            self.savename = self.spath.get().rstrip()

        xval = (float(self.x[0].get()), float(self.x[1].get()))
        yval = (float(self.y[0].get()), float(self.y[1].get()))
        graph = gp.Graph_Parser((self.ypos[1][0],self.ypos[1][1]),
                                (self.ypos[0][0],self.ypos[0][1]),
                                (self.xpos[0][0],self.xpos[0][1]),
                                (self.xpos[1][0],self.xpos[1][1]),
                                yval, xval,
                                (self.pos[0], self.pos[1]), fname)
        print((self.ypos[1][0],self.ypos[1][1]),
                                (self.ypos[0][0],self.ypos[0][0]),
                                (self.xpos[0][0],self.xpos[0][1]),
                                (self.xpos[1][0],self.xpos[1][1]),
                                xval, yval,
                                (self.pos[0], self.pos[1]), fname)

        if(self.opt == 0):
            pt = graph.get_pts()
        else:
            pt = graph.get_pts(mode='color-all')

        x, y = zip(*pt)
        plt.scatter(x,y)
        plt.show(block=False)

        df = pd.DataFrame(pt)
        df.to_csv(self.savename)

    
    def set_xlow(self):
        self.xpos[0] = self.pos
        print(self.xpos)

    def set_xhigh(self):
        self.xpos[1] = self.pos
        print(self.xpos)

    def set_ylow(self):
        self.ypos[0] = self.pos
        print(self.ypos)

    def set_yhigh(self):
        self.ypos[1] = self.pos
        print(self.ypos)

    def set_color(self):
        self.color = self.pos
        print(self.color)

    def initUI(self):
        self.master.title("Graphify")
        mf = ttk.Frame(self, padding="3 3 12 12")
        self.pack()
        self.x = [0, 0]
        self.y = [0, 0]
        self.xpos = [[0,0], [0,0]]
        self.ypos = [[0,0], [0,0]]
        self.pos= [0,0]
        self.px = [0,0,0,0]

        tk.Label(self, text='X_Low', 
                    borderwidth=1).grid(row=1,column=1)
        self.x[0] = tk.Entry(self, borderwidth=1, width=4)
        self.x[0].grid(row=1,column=2)

        tk.Label(self, text='X_High', 
                    borderwidth=1).grid(row=2,column=1)
        self.x[1] = tk.Entry(self, borderwidth=1, width=4)
        self.x[1].grid(row=2,column=2)

        tk.Label(self, text='Y_Low', 
                    borderwidth=1).grid(row=1,column=3)
        self.y[0] = tk.Entry(self, borderwidth=1, width=4)
        self.y[0].grid(row=1,column=4)

        tk.Label(self, text='Y_High', 
                    borderwidth=1).grid(row=2,column=3)
        self.y[1] = tk.Entry(self, borderwidth=1, width=4)
        self.y[1].grid(row=2,column=4)

        self.pname = tk.StringVar()        # this creates a Tkinter object
        self.pname.set("Color  0 0 0");
        self.lname = tk.StringVar()        # this creates a Tkinter object
        self.lname.set("Location 0 0");

        
        tk.Label(self, textvariable=self.pname,
                    borderwidth=1).grid(row=3, column=2)

        tk.Label(self, textvariable=self.lname,
                    borderwidth=1).grid(row=4, column=2)

        # Set radiobuttons
        self.opt = tk.IntVar() # 0=one line 1=all
        self.opt.set(0)
        self.rb = []
        self.rb.append(tk.Radiobutton(self, text="Single Line",
            variable=self.opt, value=0))
        self.rb[0].grid(row=1, column=7)

        self.rb.append(tk.Radiobutton(self, text="All Points",
            variable=self.opt, value=1))
        self.rb[1].grid(row=2, column=7)

        # Buttons for submission
        coordButton = tk.Button(self, text='Approximate Data', command=self.calc_graph)
        coordButton.grid(row=1, column=5, rowspan=2)
        
        pos_but = [];
        pos_but.append(tk.Button(self, text = 'Set X-Low  Loc',
            command=self.set_xlow).grid(row = 3, column=3))
        pos_but.append(tk.Button(self, text = 'Set X-High Loc',
            command=self.set_xhigh).grid(row=3, column=4))
        pos_but.append(tk.Button(self, text = 'Set Y-Low  Loc',
            command=self.set_ylow).grid(row=4, column=3))
        pos_but.append(tk.Button(self, text = 'Set Y-High Loc',
            command=self.set_yhigh).grid(row=4, column=4))

        pos_but.append(tk.Button(self, text = 'Color',
            command=self.set_color).grid(row=3, column=5, rowspan=2))

        # Savepath and filename options
        tk.Label(self, text='Savepath', 
                    borderwidth=1).grid(row=6,column=1)
        self.spath = tk.Entry(self, borderwidth=1, width=15)
        self.spath.grid(row=6,column=2)

        # Image Handler
        self.canvas = tk.Canvas(width=800, height=800, bg='white')
        self.canvas.pack()
        self.img = tk.PhotoImage(file=fname)        
        self.canvas.create_image(0,0,image=self.img, anchor=tk.NW)
        self.canvas.bind("<Button-1>", self.click)
        #self.canvas.bind()
        

        
def main():
    w = tk.Tk()
    w.geometry("800x800")
    app = Graphify()
    w.mainloop()

if __name__=='__main__':
    main()