from tkinter import *

def falseClicked():
    win.destroy()

win = Tk()
win.title('글자 스타일 변경')

lbFont = Label(win, text='글꼴', width=10)
lbFontStyle = Label(win, text='글꼴 스타일')
lbFontSize = Label(win, text='크기')
lbFont.grid(row=0, column=0)
lbFontStyle.grid(row=1, column=0)
lbFontSize.grid(row=2, column=0)

inFont = Entry(win, width=20)
inFontStyle = Entry(win)
inFontSize = Entry(win)
inFont.grid(row=0, column=1)
inFontStyle.grid(row=1, column=1)
inFontSize.grid(row=2, column=1)

trueBtn = Button(win, text='확인')
falseBtn = Button(win, text='취소', command=falseClicked)
trueBtn.grid(row=3, column=0)
falseBtn.grid(row=3, column=1)

win.mainloop()