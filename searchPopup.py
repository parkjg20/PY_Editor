# -*- coding: utf-8 -*-
from popup import Popup
from tkinter import *

# 기능: 문자열 검색 기능
class SearchPopup(Popup):
    '''검색어 입력 팝업'''

    def __init__(self, parent, x=0, y=0):
        Popup.__init__(self, parent, 330, 40, x-420, y+20)

        self.frame.resizable(width=False, height=False)

        TITLE = "검색, P.Y Editor 1.0"
        
        self.frame.title(TITLE)
        
        self.createGUI(self.frame)
    
    def createGUI(self, frame):
        self.lbKeyword = Label(frame, text='검색할 단어 입력')
        
        self.inKeyword = Entry(frame)

        self.btnSearch = Button(frame, text="검색", command=self.onApply)

        self.lbKeyword.grid(row=0, column=0, padx=5, pady=5)
        self.inKeyword.grid(row=0, column=1, padx=5, pady=5)
        self.btnSearch.grid(row=0, column=2, padx=5, pady=5)

        self.inKeyword.focus()
        
    def onCancel(self, event=None):
        self.parent.editor.tag_remove('search_keyword', 1.0, "end")
        
        Popup.onCancel(self, event)
        

    def onApply(self, event=None):
        countVar = IntVar()
        keyword = self.inKeyword.get().strip()
        editor = self.parent.editor
        editor.tag_remove('search_keyword', 1.0, "end")

        start = editor.index('1.0')
        end = editor.index('end')

        editor.mark_set("matchStart", start)
        editor.mark_set("matchEnd", start)
        editor.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            # index = editor.search('r/*'+keyword+'*/gi', "matchEnd","searchLimit", count=count, regexp=True)
            index = editor.search(keyword, "matchEnd","searchLimit", count=count, regexp=False)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            editor.mark_set("matchStart", index)
            editor.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            editor.tag_add('search_keyword', "matchStart", "matchEnd")

