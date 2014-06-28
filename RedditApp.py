#!/usr/bin/env python

import Tkinter as tk
import requests
import json
import sys


def create_widgets(s):
    quit_button = tk.Button(text='Quit',command=quit)
    quit_button.grid(column=3,row=2)
    
    username_input = tk.Entry();
    username_input.insert(0,'Username');
    username_input.grid(column=1,row=1)
    
    password_input = tk.Entry()
    password_input.insert(0,'password');
    password_input.grid(column=1,row=2)
    
    button = tk.Button(text='Login')
    button.bind('<Button-1>', 
            lambda event: launch(event,s,username_input.get(),password_input.get()))
    button.grid(column=2,row=2)

def launch(event,s,username,password):
    login(s,username,password)
    load_comment_history(s)
    
def login(s,username,password):
    login_dict = {'api_type': 'json',
                    'user': username, 
                    'passwd': password}
    #Request for a login, and convert the response to a json object                    
    data = s.post(r'http://www.reddit.com/api/login',data=login_dict).json()
    
    #Check for a successful login, and if so, save the user credentials to the session
    if data['json']['errors']:
        print 'There was an error processing your request'
        print data['json']['errors']
        sys.exit()
    else:
        print 'Login successful'
        s.user_cred = {'user': username,'passwd': password}
 
def load_comment_history(s):
    url = r'http://www.reddit.com/user/%s/comments.json' % (s.user_cred['user'])
    data = s.get(url).json()
    for child in data['data']['children']:
        print child['data']['author'],"\r\n",child['data']['body']
    
#Main application entry point
def main():
    s = requests.session()
    s.headers = {'user-agent': 'Aodhs Reddit App used for learning purposes'}
    app = tk.Frame()
    app.master.title('RedditApp')
    app.grid()
    create_widgets(s) 
    app.mainloop()
    
#Standard main function
if __name__ == '__main__':
       main()