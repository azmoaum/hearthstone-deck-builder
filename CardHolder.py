from Tkinter import LabelFrame, Label
class CardHolder(LabelFrame):
    def __init__(self, column, row, width, height, master=None, image=None):
        LabelFrame.__init__(self, master=master, width=width, height=height, image=image)
        self.grid_propagate(False)
        self.grid(column=column, row=row)
        
        self.card = Label(master=self, image=None)
        self.card.grid()