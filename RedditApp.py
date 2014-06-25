#!/usr/bin/env python

import tkinter as tk

class RedditApp(tk.Frame): #RedditApp inherits from tk.Frame
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=1)
        
        self.label1 = tk.Label(self, text='Label')
        self.label1.grid(column=0, row=0)
        self.label2 = tk.Label(self, text='Label')
        self.label2.grid(column=0, row=1)
        self.label3 = tk.Label(self, text='Label')
        self.label3.grid(column=0, row=2)
        self.label4 = tk.Label(self, text='Label')
        self.label4.grid(column=0, row=3)


if __name__ == '__main__':
    app = RedditApp()
    app.master.title('RedditApp')
    app.mainloop()