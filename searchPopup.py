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
        self.frame.protocol("WM_DELETE_WINDOW", self.onCancel)
        
        self.createGUI(self.frame)
    
    def createGUI(self, frame):
        self.lbKeyword = Label(frame, text='검색할 단어 입력')
        
        self.inKeyword = Entry(frame)

        self.btnSearch = Button(frame, text="검색", command=self.onApply)

        self.lbKeyword.grid(row=0, column=0)
        self.inKeyword.grid(row=0, column=1)
        self.btnSearch.grid(row=0, column=2)

        self.inKeyword.focus()
        

    def onCancel(self):
        self.parent.on_child_popup_closed(self)
        self.frame.destroy()

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

