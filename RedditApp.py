#!/usr/bin/env python

import Tkinter as tk
import praw
import xml.etree.cElementTree as ET

class RedditApp(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        
        # Make a connection to reddit
        self.r = praw.Reddit(user_agent='Reddit App made by Aodh')    

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(column=1)
        
        self.usernameInput = tk.Entry(self);
        self.usernameInput.insert(0, 'Type Username Here');
        self.usernameInput.grid(column=2)
        
        self.button = tk.Button(self, text='Login')
        self.button.bind('<Button-1>', self.setupUserData)
        self.button.grid(column=3)

    def setupUserData(self, event): 
        username = self.usernameInput.get()
        self.user = self.r.get_redditor(username)
        
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