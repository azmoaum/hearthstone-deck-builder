#!/usr/bin/env python

import Tkinter as tk
import requests
import json

def create_widgets(s):
    quit_button = tk.Button(text='Quit', command=quit)
    quit_button.grid(column=3,row=2)
    
    username_input = tk.Entry();
    username_input.insert(0, 'Username');
    username_input.grid(column=1,row=1)
    
    password_input = tk.Entry()
    password_input.insert(0, 'Password');
    password_input.grid(column=1,row=2)
    
    button = tk.Button(text='Login')
    button.bind('<Button-1>', 
            lambda event: login(event,s,username_input.get(),password_input.get()))
    button.grid(column=2,row=2)

def login(event,s,username,password):
    login_dict = {'api_type': 'json',
                        'user': username,
                        'passwd': password,
                        'rem': False}
    r = s.post(r'http://www.reddit.com/api/login', data=login_dict)
    j = json.loads(r.content)
    print j
    r = s.get(r'http://www.reddit.com/api/me.json')
    j = json.loads(r.content)
    print j
   
# Main application entry point
def main():
    s = requests.session()
    s.headers = {'user-agent': 'Aodhs Reddit App used for learning purposes'}
    app = tk.Frame()
    app.master.title('RedditApp')
    app.grid()
    create_widgets(s) 
    app.mainloop()
    
# Standard main function
if __name__ == '__main__':
       main()