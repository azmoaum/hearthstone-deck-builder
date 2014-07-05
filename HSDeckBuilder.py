#!/usr/bin/env python

from Tkinter import *
from requests import Session
from PIL import Image, ImageTk
from StringIO import StringIO
import json
import sys
import os
import Config
class HSDeckBuilder(Frame):
    def __init__(self, session, master=None):
        Frame.__init__(self, master)
        self.master.title('HSDeckBuilder')
        self.pack_propagate(0)
        self.create_widgets(session)
        
    def create_widgets(self, session):
        self.card_holder_list = []
        cards = load_cards(session)
        
        #Create Card Holders
        for x in range(1, Config.MAX_ROWS_PER_PAGE+1):
            for y in range(0, Config.MAX_CARDS_PER_ROW):
                frame = LabelFrame(width=Config.CARD_WIDTH, height=Config.CARD_HEIGHT)
                frame.grid_propagate(False)
                frame.grid(column=y, row=x)
                card_holder = Label(frame, image=None)
                card_holder.grid()
                self.card_holder_list.append(card_holder)
        
        #Create Hero Buttons
        for x, hero in enumerate(Config.HERO_CLASSES):
            button = Button(text=hero, image=None)
            button.grid(column=x, row=0)
            def handler(event, session=session, cards=cards, hero=hero):
                self.current_hero = hero
                self.current_page = 0
                return self.display_cards(event, session, cards)
            button.bind('<Button-1>', handler)
        
        #Create Next Button
        button = Button(text='Next')
        button.grid(column=9,row=2)
        def handler(event, session=session, cards=cards):
            if self.current_page >= Config.MAX_PAGES-1:
                return
            self.current_page = self.current_page+1
            return self.display_cards(event, session, cards)
        button.bind('<Button-1>', handler)
        
        #Create Back Button
        button = Button(text='Back')
        button.grid(column=8,row=2)
        def handler(event, session=session, cards=cards):
            if self.current_page <= 0:
                return
            self.current_page = self.current_page-1
            return self.display_cards(event, session, cards)
        button.bind('<Button-1>', handler)
        
    def display_cards(self, event, session, cards):
        cards = cards[self.current_hero][Config.MAX_CARDS_PER_PAGE*self.current_page:]
        num_cards = len(cards)
        if num_cards > Config.MAX_CARDS_PER_PAGE:
            cards_to_display = Config.MAX_CARDS_PER_PAGE
        else:
            cards_to_display = num_cards
            
        for holder_num in range(0, Config.MAX_CARDS_PER_PAGE):
            if holder_num < cards_to_display:
                self.display_card(cards[holder_num]['image'], holder_num) 
            else:
                self.display_card('', holder_num)
        
    def display_card(self, card_image, holder_num):
        self.card_holder_list[holder_num].config(image = card_image)
        self.card_holder_list[holder_num].image = card_image
    
def load_cards(session):
    cards = {}
    card_list = []
    
    #Read in the card data from json file
    card_data = open("AllSets.enUS.json").read()
    card_data = json.loads(card_data)

    for hero in Config.HERO_CLASSES:
        print 'Loading cards for %s...' % hero
        for set in Config.CARD_SETS:
            for card in card_data[set]:
                if 'playerClass' in card and 'cost' in card:
                    if card['playerClass'] == hero:
                    #
                    #
                    #
                    #
                    #
                    # if card does not have a playerclass than it is a netural card!
                    #
                    #
                    #
                    #
                    #
                        if card['id'] in Config.CARDS_TO_IGNORE:
                            continue
                        url = r'http://wow.zamimg.com/images/hearthstone/cards/enus/original/%s.png' % card['id']
                        response = session.get(url)
                        if response.status_code != 200:
                            continue
                        img = Image.open(StringIO(response.content)).resize((Config.CARD_WIDTH, Config.CARD_HEIGHT),Image.ANTIALIAS)
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
    
#Main application entry point
def main():
    print 'Starting HSDeckBuilder'
    session = Session()
    session.headers = {'user-agent': 'HearthStone Deck Builder v0.1'}
    app = HSDeckBuilder(session)
    app.mainloop()
#Standard main function
if __name__ == '__main__':
       main()