# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
from tkinter import colorchooser


# 사용자 편의 기능 2. 폰트 설정 팝업 표시
class StylePopup():
    '''스타일 설정 팝업'''

    def __init__(self, parent, style,  x=0, y=0):
        self.parent = parent
        self.frame = Toplevel()

        TITLE = "스타일 설정, P.Y Editor 1.0"
        self.frame.geometry('{}x{}+{}+{}'.format(400, 300, x, y))
        
        self.frame.title(TITLE)
        
        print(style)
        self.createGUI(self.frame, style)
    
    def createGUI(self, frame, style):
    # create child framedow
        lbFont = Label(frame, text='글꼴', width=10)
        lbFontStyle = Label(frame, text='글꼴 스타일')
        lbFontWeight = Label(frame, text='글꼴 굵게')
        lbFontSize = Label(frame, text='크기')
        lbFgColor = Label(frame, text='글자 색상')
        inFgColorSelected = Entry(frame, width=13)
        inFgColorSelected.insert(0, style.get('fgColor'))
        lbBgColor = Label(frame, text='배경 색상')
        inBgColorSelected = Entry(frame, width=13)
        inBgColorSelected.insert(0, style.get('bgColor'))
        
        lbFont.grid(row=0, column=0)
        lbFontStyle.grid(row=1, column=0)
        lbFontWeight.grid(row=2, column=0)
        lbFontSize.grid(row=3, column=0)
        lbFgColor.grid(row=4, column=0)
        inFgColorSelected.grid(row=4, column=1)
        lbBgColor.grid(row=5, column=0)
        inBgColorSelected.grid(row=5, column=1)

        # 글꼴 선택 Combobox
        currentFont = 0
        fontList = ["Gothic", "D2Coding", "Courier"]
        for font in enumerate(fontList):
            if(font[1] == style.get('font')):
                currentFont = font[0]
                break

        cbFont = ttk.Combobox(frame, values=fontList, width=10)
        cbFont.current(0)

        # 글꼴 스타일 선택 Combobox
        currentStyle = 0
        styleList = ["roman", "italic"]
        for fontStyle in enumerate(styleList):
            if(fontStyle[1] == style.get('fontStyle')):
                currentStyle = fontStyle[0]
                break

        cbFontStyle = ttk.Combobox(frame, values=styleList, width=10)
        cbFontStyle.current(currentStyle)

        # checked = 0
        self.checked = IntVar()
        # 글꼴 굵기 여부 선택 Checkbox
        cboxFontWeight = Checkbutton(frame, text='체크',variable=self.checked, onvalue=1, offvalue=0)

        # 글자 크기 선택 Combobox
        cbFontSize = ttk.Combobox(frame, values=[
                                        9,
                                        10,
                                        11,
                                        12,
                                        15,
                                        16,
                                        20], width=10)
        cbFontSize.current(4)
        
        # 색상표 호출
        fgColorBtn = Button(frame, text = "색상 선택", command = self.chooseFgColor)
        bgColorBtn = Button(frame, text = "색상 선택", command = self.chooseBgColor)

        # 위치 지정
        cbFont.grid(row=0, column=1)
        cbFontStyle.grid(row=1, column=1)
        cboxFontWeight.grid(row=2, column=1)
        cbFontSize.grid(row=3, column=1)
        fgColorBtn.grid(row=4, column=2)
        bgColorBtn.grid(row=5, column=2)

        self.cbFont = cbFont
        self.cbFontStyle = cbFontStyle
        self.cboxFontWeight = cboxFontWeight
        self.cbFontSize = cbFontSize
        self.inFgColorSelected = inFgColorSelected
        self.inBgColorSelected = inBgColorSelected

        trueBtn = Button(frame, text='확인', command=self.onApply)
        falseBtn = Button(frame, text='취소', command=self.onCancel)
        trueBtn.grid(row=6, column=0)
        falseBtn.grid(row=6, column=1)
        

    def onCancel(self):
        self.parent.on_child_popup_closed(self)
        self.frame.destroy()

    def onApply(self):
        print("Destroy", self)
        options = dict({
            "font": self.cbFont.get().strip(),
            "fontStyle": self.cbFontStyle.get().strip(),
            "fontWeight": 'bold' if ( self.checked.get() == 1 ) else 'normal' ,
            "fontSize": self.cbFontSize.get().strip(),
            "fgColor": self.inFgColorSelected.get().strip(),
            "bgColor": self.inBgColorSelected.get().strip()
        })
        print("option before destroy", options)

        self.parent.on_child_popup_closed(self, options)
        self.frame.destroy()

    def chooseFgColor(self):
        # variable to store hexadecimal code of color
        color_code = colorchooser.askcolor(title ="색상 선택")
        self.inFgColorSelected.delete(0, 'end')
        self.inFgColorSelected.insert(0, color_code[1])
        print(color_code[1])
        self.frame.lift()

    def chooseBgColor(self):
        # variable to store hexadecimal code of color
        color_code = colorchooser.askcolor(title ="색상 선택")
        self.inBgColorSelected.delete(0, 'end')
        self.inBgColorSelected.insert(0, color_code[1])
        print(color_code[1])
        self.frame.lift()
