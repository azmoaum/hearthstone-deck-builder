from Tkinter import Label
class Card(Label):
    def __init__(self, master=None, image=None):
        Label.__init__(self, master=master, image=image)