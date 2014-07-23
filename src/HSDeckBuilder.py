#!/usr/bin/env python

import json
import os.path
import Config
from MainWidgets import HeroButtonsFrame, CardsFrame, DeckMakerFrame, DeckLabel, CardLabel
from Tkinter import Frame, Button, Entry
from requests import Session
from PIL import Image, ImageTk
from StringIO import StringIO

class HSDeckBuilder(Frame):

    def __init__(self, session, master=None):
        Frame.__init__(self, master=master)
        self.master.title('HSDeckBuilder')
        self.pack_propagate(0)   
        
        #card_dict = Dictionary of hero classes with their associated card lists
        card_dict = load_cards(session)
        self.create_widgets(card_dict)
        self.populate_card_labels(card_dict)
        
    def create_widgets(self, card_dict):
        #Create CardsFrame
        self.cards_frame = CardsFrame(master=self.master, 
                                      width=Config.CARD_LABEL_WIDTH*Config.MAX_CARD_LABELS_PER_ROW,
                                      height=Config.CARD_LABEL_HEIGHT*Config.MAX_ROWS_PER_PAGE)
        self.cards_frame.grid_propagate(False)
        self.cards_frame.grid(column=1, row=1)
        
        #Add Cards to CardsFrame
        for x in range(1, Config.MAX_ROWS_PER_PAGE+1):
            for y in range(1, Config.MAX_CARD_LABELS_PER_ROW+1):
                card_label = CardLabel(master=self.cards_frame, image=None)
                def handler(event, card_label=card_label):
                    if (card_label.card['rarity'] == 'Legendary' and
                        self.deck_maker_frame.deck_list.count(card_label.card['name']) == 1):
                            return;
                    return self.add_to_deck(event, card_label.card['name'])
                card_label.bind('<Button-1>', handler)
                card_label.grid(column=y, row=x)
        self.card_labels = self.cards_frame.winfo_children()    
                
        #Create HeroButtonsFrame
        self.hero_buttons = HeroButtonsFrame(master=self.master)
        self.hero_buttons.grid(column=1, row=0, columnspan=Config.MAX_CARD_LABELS_PER_ROW)
        
        #Add buttons to HeroButtonsFrame
        for x, hero in enumerate(Config.HERO_CLASSES):
            button = Button(master=self.hero_buttons, text=hero, image=None)
            def handler(event, card_dict=card_dict, hero=hero):
                self.cards_frame.hero = hero
                self.cards_frame.page = 1
                return self.populate_card_labels(card_dict, event)
            button.bind('<Button-1>', handler)
            button.grid(column=x+1, row=0)
        self.hero_buttons = self.hero_buttons.winfo_children()

        #Create Next Button
        self.next_button = Button(master=self.master, text='Next', height=35)
        def handler(event, card_dict=card_dict):
            if self.cards_frame.page >= Config.MAX_PAGES:
                hero_index = Config.HERO_CLASSES.index(self.cards_frame.hero)
                if (hero_index < len(Config.HERO_CLASSES)-1):
                    self.cards_frame.hero = Config.HERO_CLASSES[hero_index+1]
                    self.cards_frame.page = 1                
            else:
                self.cards_frame.page = self.cards_frame.page+1
            return self.populate_card_labels(card_dict, event)
        self.next_button.bind('<Button-1>', handler)
        self.next_button.grid(column=2,row=1, rowspan=2)
        
        #Create Back Button
        self.back_button = Button(master=self.master, text='Back', height=35)
        def handler(event, card_dict=card_dict):
            if self.cards_frame.page <= 1:
                hero_index = Config.HERO_CLASSES.index(self.cards_frame.hero)
                if (hero_index > 0):
                    self.cards_frame.hero = Config.HERO_CLASSES[hero_index-1]
                    self.cards_frame.page = Config.MAX_PAGES
            else:
                self.cards_frame.page = self.cards_frame.page-1
            return self.populate_card_labels(card_dict, event)
        self.back_button.bind('<Button-1>', handler)
        self.back_button.grid(column=0,row=1, rowspan=2)
        
        #Create Save Button
        self.save_button = Button(master=self.master, text='Save Deck')
        self.save_button.bind('<Button-1>', self.save_deck)
        self.save_button.grid(column=3,row=4)
   
        #Create DeckMakerFrame
        self.deck_maker_frame = DeckMakerFrame(master=self.master, 
                                    width=150,
                                    height=Config.CARD_LABEL_HEIGHT*2)
        self.deck_maker_frame.grid_propagate(False)
        self.deck_maker_frame.grid(column=3, row=1, rowspan=2)
        
        #Create DeckName Entry
        self.deck_name_entry = Entry(master=self.master, text='Deck name')
        self.deck_name_entry.grid(column=3,row=0)
        
        #Create DeckLoaderFrame
        self.deck_loader_frame = DeckMakerFrame(master=self.master, 
                                    width=150,
                                    height=Config.CARD_LABEL_HEIGHT*2)
        self.deck_loader_frame.grid_propagate(False)
        self.deck_loader_frame.grid(column=4, row=1, rowspan=2)
        
        #Create LoadDecks Entry
        self.load_decks_button = Button(master=self.master, text='Load Decks')
        self.load_decks_button.bind('<Button-1>', self.load_decks)
        self.load_decks_button.grid(column=4,row=0)
        
    def populate_card_labels(self, card_dict, event=None):
        #List of cards to assign to card labels, depending on the hero and page
        card_list = card_dict[self.cards_frame.hero][Config.MAX_CARD_LABELS_PER_PAGE*(self.cards_frame.page-1):]
        
        labels_to_populate = len(card_list)
        if labels_to_populate > Config.MAX_CARD_LABELS_PER_PAGE:
            labels_to_populate = Config.MAX_CARD_LABELS_PER_PAGE
        
        #For each card label, assign it a card and set its image
        for x in range(0, Config.MAX_CARD_LABELS_PER_PAGE):
            if x < labels_to_populate:
                self.card_labels[x].card = card_list[x]
                self.card_labels[x].config(image = card_list[x]['image'])
                self.card_labels[x].image = card_list[x]['image']
            else:
                self.card_labels[x].config(image = '')
                self.card_labels[x].image = ''
    
    def add_to_deck(self, event, card_name):
        deck_labels = self.deck_maker_frame.winfo_children()
        if len(self.deck_maker_frame.deck_list) == Config.MAX_CARDS_IN_DECK:
            return
        if self.deck_maker_frame.deck_list.count(card_name) == 2:
            return
           
        #Check if card is already in the deck. If so, loop through
        #all the deck labels and add 'x2' to the label. Else
        #create a deck label for the new card
        if card_name in self.deck_maker_frame.deck_list:
           for label in deck_labels:
                if label.card_name == card_name:
                    label.config(text=label.card_name+' x2')
        else:
            if len(set(self.deck_maker_frame.deck_list)) % 2 == 0:
                bg = 'grey'
            else:
                bg = None
            deck_label = DeckLabel(master=self.deck_maker_frame, image=None, text=card_name, bg=bg)
            def handler(event, deck_label=deck_label):
                return self.remove_from_deck(event, deck_label)
            deck_label.bind('<Button-1>', handler)
            deck_label.grid()
        self.deck_maker_frame.deck_list.append(card_name)
    
    def remove_from_deck(self, event, deck_label):
        if ' x2' in deck_label.config()['text'][-1]:
            new_text = deck_label.config()['text'][-1].replace(' x2', '')
            deck_label.config(text=new_text)
        else:
            deck_label.destroy()
        self.deck_maker_frame.deck_list.remove(deck_label.card_name)
        
    def save_deck(self, event):
        #Check if deck is complete
        if self.deck_maker_frame.deck_list < Config.MAX_CARDS_IN_DECK:
            return
        deck_name = self.deck_name_entry.get()
        
        #Create a path for the deck. If the path exists, rename it.
        path = '%s\%s.txt' % (Config.DECK_PATH, deck_name)
        count = 1
        while os.path.isfile(path):
            path = '%s\%s-%03d.txt' % (Config.DECK_PATH, deck_name, count)
            count = count + 1
        
        #Create content of deck file and write it
        content_name = 'Deck: %s\n\n' % (deck_name)
        content_deck = ['    -'+s for s in self.deck_maker_frame.deck_list]
        content_deck = '\n'.join(content_deck)
        print 'Saving deck to %s' % os.path.abspath(path)
        with open(path, 'w') as myFile:
            myFile.write(content_name)
            myFile.write(content_deck)
    
    def load_decks(self, event):
        deck_files = [file for file in os.listdir(Config.DECK_PATH)]
        
        for file in deck_files:
            deck_loader_label = DeckLabel(master=self.deck_loader_frame, image=None, text=file)
            def handler(event, deck_loader_label=deck_loader_label):
                return self.load_deck(event, deck_loader_label)
            deck_loader_label.bind('<Button-1>', handler)
            deck_loader_label.grid()
        print deck_files
    
    def load_deck(self, event, deck_loader_label):
        path = '%s\%s' % (Config.DECK_PATH, deck_loader_label.config()['text'][-1])
        
        with open(path) as f:
            content = [l.strip().replace('-','') for l in f.readlines()]
            content = content[2:]

        del self.deck_maker_frame.deck_list[:]
        for label in self.deck_maker_frame.winfo_children():
            label.destroy()

        for x in content:
            self.add_to_deck(event, x)
        
def load_cards(session):
    card_dict = {}
    card_list = []
    
    #Read in the card data from json file
    path = '%s\AllSets.enUS.json' % (Config.JSON_PATH)
    card_data = open(path).read()
    card_data = json.loads(card_data)

    for hero in Config.HERO_CLASSES:
        print 'Loading cards for %s...' % hero
        for set in Config.CARD_SETS:
            for card in card_data[set]:
                if ('playerClass' in card and 'cost' in card and
                    card['playerClass'] == hero and
                    card['id'] not in Config.CARDS_TO_IGNORE):
                    #
                    # if card does not have a playerclass than it is a netural card!
                    #
                        url = '%s/%s.png' % (Config.IMAGES_URL, card['id'])
                        response = session.get(url)
                        if response.status_code == 200:
                            img = Image.open(StringIO(response.content)).resize((Config.CARD_LABEL_WIDTH, 
                                                                                 Config.CARD_LABEL_HEIGHT), 
                                                                                 Image.ANTIALIAS)
                            photo_img = ImageTk.PhotoImage(img)
                            card['image'] = photo_img
                            card_list.append(card)
        card_list.sort(key=lambda x:(x['cost'], x['name']))
        card_dict[hero] = card_list[:]
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