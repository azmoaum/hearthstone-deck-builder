#!/usr/bin/env python

from Tkinter import *
from requests import Session
import json
import sys
from PIL import Image, ImageTk
from StringIO import StringIO
import os

class HSDeckBuilder(Frame):
    def __init__(self, session, master=None):
        Frame.__init__(self, master)
        self.master.title('HSDeckBuilder')
        self.create_widgets(session)
        
    def create_widgets(self, session):
        self.card_spot_list = []
        for x in range(0, 4):
            card = Label(text="Card_Spot", image=None)
            card.grid(column=x, row=1)
            self.card_spot_list.append(card)
        for x in range(0, 4):
            card = Label(text="Card_Spot", image=None)
            card.grid(column=x, row=2)
            self.card_spot_list.append(card)
        
        self.druid_button = Button(text="Druid", image=None)
        self.druid_button.grid(column=0, row=0)
        self.druid_button.bind('<Button-1>', 
                lambda event: load_cards(session, 'Mage', self.card_spot_list))

    
def load_cards(session, playerClass, card_spot_list):
    card_data = open("AllSets.enUS.json").read()
    card_data = json.loads(card_data)
    count = 0
    for item in card_data['Expert']:
        if 'playerClass' in item:
            if item['playerClass'] == playerClass:
                print item['name'], ' ', item['id']
                url = r'http://wow.zamimg.com/images/hearthstone/cards/enus/original/%s.png' % item['id']
                display_image(session, url, card_spot_list, count)
                count = count + 1
                if count == len(card_spot_list):
                    return
    
def display_image(session, url, card_spot_list, count):
    print 'click'
    response = session.get(url)
    img = Image.open(StringIO(response.content))
    img2 = ImageTk.PhotoImage(img)
    card_spot_list[count].config(image = img2)
    card_spot_list[count].image = img2
    
#Main application entry point
def main():
    session = Session()
    session.headers = {'user-agent': 'HearthStone Deck Builder v0.1'}
    app = HSDeckBuilder(session)
    app.mainloop()
#Standard main function
if __name__ == '__main__':
       main()