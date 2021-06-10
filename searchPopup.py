# -*- coding: utf-8 -*-
from tkinter import *

# 기능: 문자열 검색 기능
class SearchPopup():
    '''검색어 입력 팝업'''

    def __init__(self, parent, x=0, y=0):
        self.parent = parent
        self.frame = Toplevel()
        self.frame.resizable(width=False, height=False)

        TITLE = "검색, P.Y Editor 1.0"
        self.frame.geometry('{}x{}+{}+{}'.format(400, 150, x-420, y + 20))
        self.frame.title(TITLE)
        
        self.createGUI(self.frame)
    
    def createGUI(self, frame):
        lbKeyword = Label(frame, text='검색할 단어 입력')
        
        inKeyword = Entry(frame)

        btnSearch = Button(frame, text="검색")

        lbKeyword.grid(row=0, column=0)
        inKeyword.grid(row=0, column=1)
        btnSearch.grid(row=0, column=2)
        

    def onCancel(self):
        self.parent.on_child_popup_closed(self)
        self.frame.destroy()

    def onApply(self):
        options = dir()
        self.parent.on_child_popup_closed(self, options)
        self.frame.destroy()
