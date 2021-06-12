from popup import Popup
from tkinter import *
from tkinter import ttk

class AutocompPopup(Popup):
    '''자동완성 팝업'''

    def __init__(self, parent, x=0, y=0, auto_completes=dict()):
        Popup.__init__(self, parent, 270, 180, x, y)
        self.__auto_completes = auto_completes
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

        addBtn = Button(frame, text="추가", command=self.onAppend)
        addBtn.grid(row=1, column=3, rowspan=2, padx=5)

        currentSet = 0
        self.comboList = [ f + ":" + self.__auto_completes[f] for f in self.__auto_completes]

        lbSet = Label(frame, text="설정된 키워드")
        cbSet = ttk.Combobox(frame, values=self.comboList, width=22)
        cbSet.bind('<<ComboboxSelected>>', self.onSelect)

        lbSet.grid(row=3, column=0)
        cbSet.grid(row=3, column=1, columnspan=3, pady=10)

        btnFrame = Frame(frame)
        closeBtn = Button(btnFrame, text="닫기", padx=30, command=self.onCancel)
        closeBtn.grid(row=0, column=0, columnspan=2)
        btnFrame.grid(row=4, column=0, columnspan=4, pady=10)

        self.originKeyword = originKeyword
        self.transitionKeyword = transitionKeyword
        self.cbSet = cbSet

    def onDestroy(self, event=None):
        options = self.self.__auto_completes
        self.parent.on_child_popup_closed(self, options)
        self.frame.destroy()

    def onSelect(self, event=None):
        print(self.cbSet.current())
        self.originKeyword.delete(0, "end")
        self.transitionKeyword.delete(0, "end")
        selected = self.cbSet.get().split(':')
        key = selected[0].strip()
        value = selected[1].strip()
        self.originKeyword.insert(0, key)
        self.transitionKeyword.insert(0, value)

    # 항목 추가
    def onAppend(self, event=None):
        originEntry=self.originKeyword.get().strip()
        transitionEntry=self.transitionKeyword.get().strip()
        self.__auto_completes[originEntry]=transitionEntry

        self.comboList.append(originEntry+":"+transitionEntry)
        self.cbSet['values'] = self.comboList