from Tkinter import LabelFrame, Label

class CardsFrame(LabelFrame):
    def __init__(self, width, height, master=None):
        LabelFrame.__init__(self, master=master, width=width, height=height)
        self.hero = 'Druid'
        self.page = 1    

class CardLabel(Label):
    def __init__(self, master=None, image=None, name=None):
        Label.__init__(self, master=master, image=image)
        self.name = name
        
class DeckFrame(LabelFrame):
    def __init__(self, width, height, master=None):
        LabelFrame.__init__(self, master=master, width=width, height=height)
        self.deck_list = []
        
class DeckLabel(Label):
    def __init__(self, master=None, image=None, text=None):
        Label.__init__(self, master=master, image=image, text=text)
        self.text = text
        #labels_text = [label.text for label in master.winfo_children()]
        
        """self.deck_list = '0/30'
        self.count = 0
    
    def add_to_deck(self, card_name):
        if self.count < 30:
            index = self.deck_list.find(card_name)
            if (self.deck_list.find(card_name + ' x2') > 0):
                return
            if index > 0:
                self.deck_list = self.deck_list[:index+len(card_name)] + ' x2' + self.deck_list[len(card_name)+index:]
            else:
                self.deck_list = self.deck_list + '\n' + card_name
                
            self.count = self.count + 1
            str1 = str(self.count-1)+'/30'
            str2 = str(self.count)+'/30'
            
            print str1, str2
            self.deck_list = self.deck_list.replace(str1, str2)
            self.config(text=self.deck_list)   """    

class HeroButtonsFrame(LabelFrame):
    def __init__(self, master=None):
        LabelFrame.__init__(self, master=master)
