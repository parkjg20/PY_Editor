from tkinter import *

class Popup():
    '''팝업의 슈퍼클래스 팝업 기본 기능 정의'''
    def __init__(self, parent, width, height, x, y, style=None):
        self.parent = parent
        self.frame = Toplevel()
        self.frame.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.frame.minsize(width, height)

        self.frame.protocol("WM_DELETE_WINDOW", self.onCancel)
        self.frame.bind('<Escape>', self.onCancel)

    def createGUI(self, frame, style):
        pass

    def onCancel(self, event=None):
        self.parent.on_child_popup_closed(self)
        self.frame.destroy()

    def onApply(self, event=None):
        pass

    def lift(self):
        self.frame.lift()
        self.frame.focus()

