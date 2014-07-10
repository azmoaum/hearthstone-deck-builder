from Tkinter import LabelFrame, Label

class CardsFrame(LabelFrame):
    def __init__(self, width, height, master=None):
        LabelFrame.__init__(self, master=master, width=width, height=height)
        self.hero = ''
        self.page = 1    

class CardLabel(Label):
    def __init__(self, master=None, image=None, id=None):
        Label.__init__(self, master=master, image=image)
        self.id = id
        
class HeroButtonsFrame(LabelFrame):
    def __init__(self, master=None):
        LabelFrame.__init__(self, master=master)
