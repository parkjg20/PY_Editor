from popup import Popup
from tkinter import *
from tkinter import ttk

class AutocompPopup(Popup):
    '''자동완성 팝업'''

    def __init__(self, parent, x=0, y=0):
        Popup.__init__(self, parent, 270, 180, x, y)

        TITLE = "자동완성 팝업, P.Y Editor 1.0"

        self.frame.title(TITLE)

        self.createGUI(self.frame)

    def createGUI(self, frame):
        lbTitle = Label(frame, text="자동완성 키워드 등록")
        lbTitle.grid(row=0, column=0, columnspan=4)

        lbOriginkeyword = Label(frame, text="기본 키워드")
        lbOriginkeyword.grid(row=1, column=0, pady=5)
        lbTransitionkeyword = Label(frame, text="바꿔질 키워드")
        lbTransitionkeyword.grid(row=2, column=0, pady=5)

        originKeyword = Entry(frame)
        originKeyword.grid(row=1, column=1, columnspan=2, pady=5)
        transitionKeyword = Entry(frame)
        transitionKeyword.grid(row=2, column=1, columnspan=2, pady=5)

        addBtn = Button(frame, text="추가" )
        addBtn.grid(row=1, column=3, rowspan=2, padx=5)

        # settings.json 연동
        setDict = {
            "박진국": "바보", 
            "유승완": "병신"
        }

        currentSet = 0
        comboList = [ f + ": " + setDict[f] for f in setDict]

        cbSet = ttk.Combobox(frame, values=comboList)
        cbSet.bind('<<ComboboxSelected>>', self.onSelect)

        cbSet.grid(row=3, column=0, columnspan=4, pady=10)

        btnFrame = Frame(frame)
        trueBtn = Button(btnFrame, text="확인", padx=30)
        falseBtn = Button(btnFrame, text="취소", padx=30)
        trueBtn.grid(row=0, column=0)
        falseBtn.grid(row=0, column=1)
        btnFrame.grid(row=4, column=0, columnspan=4, pady=10)

        self.originKeyword = originKeyword
        self.transitionKeyword = transitionKeyword
        self.cbSet = cbSet

    def onSelect(self, event=None):
        print(self.cbSet.current())
        self.originKeyword.delete(0, "end")
        self.transitionKeyword.delete(0, "end")
        selected = self.cbSet.get().split(':')
        key = selected[0].strip()
        value = selected[1].strip()
        self.originKeyword.insert(0, key)
        self.transitionKeyword.insert(0, value)