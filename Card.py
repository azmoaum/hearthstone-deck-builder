from Tkinter import Label

class Card(Label):
    def __init__(self, master=None, image=None, id=None):
        Label.__init__(self, master=master, image=image)
        self.id = id
        self.grid()