from Tkinter import LabelFrame, Label

class CardsFrame(LabelFrame):
    def __init__(self, width, height, master=None):
        LabelFrame.__init__(self, master=master, width=width, height=height)
        self.hero = 'Druid'
        self.page = 1    

class CardLabel(Label):
    def __init__(self, master=None, image=None, text=None):
        Label.__init__(self, master=master, image=image)
        self.card = None
        
class DeckFrame(LabelFrame):
    def __init__(self, width, height, master=None):
        LabelFrame.__init__(self, master=master, width=width, height=height)
        self.deck_list = []
        
class DeckLabel(Label):
    def __init__(self, master=None, image=None, text=None, bg=None):
        Label.__init__(self, master=master, image=image, text=text, bg=bg)
        self.card_name = text

class HeroButtonsFrame(LabelFrame):
    def __init__(self, master=None):
        LabelFrame.__init__(self, master=master)
