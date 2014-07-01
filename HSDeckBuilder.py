#!/usr/bin/env python

from Tkinter import *
from requests import Session
import json
import sys
from PIL import Image, ImageTk
from StringIO import StringIO
import os

HERO_CLASSES = ['Druid', 'Mage', 'Warlock', 'Hunter', 'Priest', 'Paladin', 'Rogue']
CARD_SETS = ['Basic', 'Expert']

CARDS_TO_IGNORE = ['CS2_013t', 'EX1_573t', 'EX1_158t', 'EX1_160t', 'CS2_017', 'EX1_165t2', 'EX1_165t1',
                    'EX1_173', 'CS2_034', 'tt_010a', 'CS2_mirror', 'EX1_323h', 'EX1_317t', 'EX1-tk33', 'CS2_056', 'EX1_323w',
                    'EX1_554t', 'EX1_538t', 'EX1_534t', 'DS1h_292', 'NEW1_034', 'NEW1_033', 'NEW1_032', 
                    'EX1_345t', 'CS1h_001', 'EX1_625t2', 'EX1_625t', 'EX1_130a', 'CS2_101t', 'CS2_101',
                    'EX1_383t', 'NEW1_006', 'EX1_131t', 'CS2_082', 'CS2_083b']

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
            
        cards = load_cards(session)
        for x, hero in enumerate(HERO_CLASSES):
            button = Button(text=hero, image=None)
            button.grid(column=x, row=0)
            def handler(event, session=session, hero=hero, card_spot_list=self.card_spot_list):
                return display_cards(event, session, cards, hero, self.card_spot_list)
            button.bind('<Button-1>', handler)
  
def load_cards(session):
    cards = {}
    card_list = []
    
    #Read in the card data from json file
    card_data = open("AllSets.enUS.json").read()
    card_data = json.loads(card_data)

    for hero in HERO_CLASSES:
        print 'Loading cards for %s' % hero
        for set in CARD_SETS:
            for card in card_data[set]:
                if 'playerClass' in card and 'cost' in card:
                    if card['playerClass'] == hero:
                        if card['id'] in CARDS_TO_IGNORE:
                            continue
                        url = r'http://wow.zamimg.com/images/hearthstone/cards/enus/original/%s.png' % card['id']
                        response = session.get(url)
                        if response.status_code != 200:
                            continue
                        img = Image.open(StringIO(response.content)).resize((200, 304),Image.ANTIALIAS)
                        photo_img = ImageTk.PhotoImage(img)
                        card['image'] = photo_img
                        card_list.append(card)
                        
        card_list.sort(key=lambda x:(x['cost'], x['name']))
        cards[hero] = card_list[:]
        #for card in cards[hero]:
        #    print card['name'], ' ', card['id']
        card_list[:] = []
    print 'Finished loading cards'   
    return cards
def display_cards(event, session, cards, hero, card_spot_list):
    count = 0
    #print 'Displaying cards for %s' % hero
    for card in cards[hero]:
        display_card(card, card_spot_list, count)
        count = count + 1
        if count == len(card_spot_list):
            return
    
def display_card(card, card_spot_list, count):
    card_spot_list[count].config(image = card['image'])
    card_spot_list[count].image = card['image']
    
#Main application entry point
def main():
    session = Session()
    session.headers = {'user-agent': 'HearthStone Deck Builder v0.1'}
    app = HSDeckBuilder(session)
    app.mainloop()
#Standard main function
if __name__ == '__main__':
       main()