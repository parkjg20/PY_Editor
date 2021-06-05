# -*- coding: utf-8 -*-
from tkinter import *

# 사용자 편의 기능 2. 폰트 설정 팝업 표시
class StylePopup():
    '''스타일 설정 팝업'''

    def __init__(self, parent):
        self.parent = parent
        self.frame = Toplevel()
        
        TITLE = "스타일 설정, P.Y Editor 1.0"
        self.frame.geometry('400x300')
        
        self.frame.title(TITLE)
        
        self.createGUI()
    
    def createGUI(self):
    # create child window
        # display message
        message = "This is the child window"
        Label(self.frame, text=message).pack()
        # quit child window and return to root window
        # the button is optional here, simply use the corner x of the child window
        Button(self.frame, text='OK', command=self.onDestroy).pack()

    def onDestroy(self):
        print("Destroy", self)
        self.parent.on_child_popup_closed(self)
        self.frame.destroy()
        