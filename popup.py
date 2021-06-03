# -*- coding: utf-8 -*-
from tkinter import *

# 사용자 편의 기능 2. 폰트 설정 팝업 표시
class StylePopup():
    
    def __init__(self, root):
        self.root = root
        self.win = Tk()
        self.TITLE = '스타일 설정 팝업'
        self.win.title(self.TITLE)
        self.win.geometry('400x300')
    
    def createGUI(self):
    # create child window
        # display message
        message = "This is the child window"
        Label(self.win, text=message).pack()
        # quit child window and return to root window
        # the button is optional here, simply use the corner x of the child window
        Button(self.win, text='OK', command=self.destroy).pack()

    def destroy(self):
        # root의 onChildDestory(인자로 설정 값을)
        
        self.root.removeChildWindow(self)
        self.win.destroy()