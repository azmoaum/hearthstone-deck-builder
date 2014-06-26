#!/usr/bin/env python

import Tkinter as tk
import praw
import xml.etree.cElementTree as ET

class RedditApp(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
        # Make a connection to reddit and get the user
        self.r = praw.Reddit(user_agent='Reddit App made by Aodh')
        self.user = self.r.get_redditor('Unidan')         

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=1)
        
        self.label1 = tk.Label(self, text='Label')
        self.label1.bind('<Button-1>', self.setupUserData)
        self.label1.grid()

    def setupUserData(self, event):  
        gen = self.user.get_submitted(limit=5)
        for x in gen:
            print x

# Main application entry point
def main():
    app = RedditApp()
    app.master.title('RedditApp')
    app.mainloop()
    
# Standard main function
if __name__ == '__main__':
       main()