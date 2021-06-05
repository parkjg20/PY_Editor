# -*- coding: utf-8 -*-
from tkinter import *

# 사용자 편의 기능 2. 폰트 설정 팝업 표시
class StylePopup():
    '''스타일 설정 팝업'''

    def __init__(self, parent, x=0, y=0):
        self.parent = parent
        self.frame = Toplevel()

        TITLE = "스타일 설정, P.Y Editor 1.0"
        self.frame.geometry('{}x{}+{}+{}'.format(400, 300, x, y))
        
        self.frame.title(TITLE)
        
        self.createGUI(self.frame)
    
    def createGUI(self, frame):
    # create child framedow
        lbFont = Label(frame, text='글꼴', width=10)
        lbFontStyle = Label(frame, text='글꼴 스타일')
        lbFontSize = Label(frame, text='크기')
        
        lbFont.grid(row=0, column=0)
        lbFontStyle.grid(row=1, column=0)
        lbFontSize.grid(row=2, column=0)

        inFont = Entry(frame, width=20)
        inFontStyle = Entry(frame)
        inFontSize = Entry(frame)
        
        inFont.grid(row=0, column=1)
        inFontStyle.grid(row=1, column=1)
        inFontSize.grid(row=2, column=1)

        self.inFont = inFont
        self.inFontStyle = inFontStyle
        self.inFontSize = inFontSize

        trueBtn = Button(frame, text='확인', command=self.onApply)
        falseBtn = Button(frame, text='취소', command=self.onCancel)
        trueBtn.grid(row=3, column=0)
        falseBtn.grid(row=3, column=1)
        

    def onCancel(self):
        self.parent.on_child_popup_closed(self)
        self.frame.destroy()

    def onApply(self):
        print("Destroy", self)
        options = dict({
            "font": self.inFont.get().strip(),
            "fontStyle": self.inFontStyle.get().strip(),
            "fontSize": self.inFontSize.get().strip()
        })

        self.parent.on_child_popup_closed(self, options)
        self.frame.destroy()
