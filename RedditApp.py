#!/usr/bin/env python

import Tkinter as tk
import requests
import json

def createWidgets():
    quitButton = tk.Button(text='Quit', command=quit)
    quitButton.grid(column=3,row=2)
    
    usernameInput = tk.Entry();
    usernameInput.insert(0, 'Type Username Here');
    usernameInput.grid(column=1,row=1)
    
    passwordInput = tk.Entry()
    passwordInput.insert(0, 'Type Password Here');
    passwordInput.grid(column=1,row=2)
    
    button = tk.Button(text='Login')
    button.bind('<Button-1>', 
            lambda event: login(event, usernameInput.get(), passwordInput.get()))
    button.grid(column=2,row=2)

def login(event, username, password):
    print username

# Main application entry point
def main():
    app = tk.Frame()
    app.master.title('RedditApp')
    app.grid()
    createWidgets() 
    app.mainloop()
    
# Standard main function
if __name__ == '__main__':
       main()