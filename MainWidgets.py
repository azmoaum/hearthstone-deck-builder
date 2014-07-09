from Tkinter import LabelFrame, Label

class CardHolder(LabelFrame):
    def __init__(self, column, row, width, height, master=None, image=None):
        LabelFrame.__init__(self, master=master, width=width, height=height, image=image)
        self.grid_propagate(False)
        self.grid(column=column, row=row)
        self.card = Card(master=self, image=image)

class Card(Label):
    def __init__(self, master=None, image=None, id=None):
        Label.__init__(self, master=master, image=image)
        self.id = id
        self.grid()