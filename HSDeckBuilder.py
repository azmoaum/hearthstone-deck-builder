#!/usr/bin/env python

from Tkinter import *
from requests import Session
from PIL import Image, ImageTk
from StringIO import StringIO
import json
import sys
import os
import Config
from CardHolder import CardHolder

class HSDeckBuilder(Frame):
    def __init__(self, session, master=None):
        Frame.__init__(self, master)
        self.master.title('HSDeckBuilder')
        self.pack_propagate(0)
        self.create_widgets(session)
        
    def create_widgets(self, session):
        self.card_holder_list = []
        #card_dict = Dictionary of hero classes with their associated card lists
        card_dict = load_cards(session)
        
        #Create Card Holders
        for x in range(1, Config.MAX_ROWS_PER_PAGE+1):
            for y in range(1, Config.MAX_CARDS_PER_ROW+1):
                card_holder = CardHolder(master=self.master, column=y, row=x, 
                    width=Config.CARD_WIDTH, height=Config.CARD_HEIGHT)
                def handler(event, card_holder=card_holder):
                   return self.set_card(event, card_holder)
                card_holder.card.bind('<Button-1>', handler)
                self.card_holder_list.append(card_holder)
        
        #Create Hero Buttons
        button_frame = LabelFrame(master=self.master)
        button_frame.grid(row=0, column=1, columnspan=Config.MAX_CARDS_PER_ROW)
        for x, hero in enumerate(Config.HERO_CLASSES):
            button = Button(button_frame, text=hero, image=None)
            button.grid(column=x+1, row=0)
            def handler(event, card_dict=card_dict, hero=hero):
                self.current_hero = hero
                self.current_page = 1
                return self.display_cards(event, card_dict)
            button.bind('<Button-1>', handler)

        #Create Next Button
        button = Button(master=self.master, text='Next', height=35)
        button.grid(column=9,row=1, rowspan=2)
        def handler(event, card_dict=card_dict):
            if self.current_page >= Config.MAX_PAGES:
                hero_index = Config.HERO_CLASSES.index(self.current_hero)
                if (hero_index < len(Config.HERO_CLASSES)-1):
                    self.current_hero = Config.HERO_CLASSES[hero_index+1]
                    self.current_page = 1
            else:
                self.current_page = self.current_page+1
            return self.display_cards(event, card_dict)
        button.bind('<Button-1>', handler)
        
        #Create Back Button
        button = Button(master=self.master, text='Back', height=35)
        button.grid(column=0,row=1, rowspan=2)
        def handler(event, card_dict=card_dict):
            if self.current_page <= 1:
                hero_index = Config.HERO_CLASSES.index(self.current_hero)
                if (hero_index > 0):
                    self.current_hero = Config.HERO_CLASSES[hero_index-1]
                    self.current_page = Config.MAX_PAGES
            else:
                self.current_page = self.current_page-1
            return self.display_cards(event, card_dict)
        button.bind('<Button-1>', handler)
        
    def display_cards(self, event, card_dict):
        #card_data = List of cards to display depending on the current hero and page
        card_list = card_dict[self.current_hero][Config.MAX_CARDS_PER_PAGE*(self.current_page-1):]
        num_cards_to_display = len(card_list)
        if num_cards_to_display > Config.MAX_CARDS_PER_PAGE:
            num_cards_to_display = Config.MAX_CARDS_PER_PAGE
        
        #For each card_holder, decide if a card should be displayed
        #If there are less cards to display then card holders, than
        #blank images will fill those card holders
        for holder_num in range(0, Config.MAX_CARDS_PER_PAGE):
            if holder_num < num_cards_to_display:
                self.card_holder_list[holder_num].card.id = card_list[holder_num]['name']
                self.display_card(card_list[holder_num]['image'], holder_num) 
            else:
                self.display_card('', holder_num)
        
    def display_card(self, card_image, holder_num):
        self.card_holder_list[holder_num].card.config(image = card_image)
        self.card_holder_list[holder_num].card.image = card_image
    
    def set_card(self, event, card_holder):
        print card_holder.card.id
        
def load_cards(session):
    card_dict = {}
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
        card_dict[hero] = card_list[:]
        #for card in cards[hero]:
        #    print card['name'], ' ', card['id']
        card_list[:] = []
    print 'Finished loading cards'   
    return card_dict
    
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