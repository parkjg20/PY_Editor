from tkinter import *

class LineIndicator(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.text = Text(self)
        self.vsb = Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)
        
        self.text.bind("<KeyRelease-BackSpace>", self._on_change)
        self.text.bind("<KeyRelease-Return>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

# class CustomText(Text):
#     def __init__(self, *args, **kwargs):
#         Text.__init__(self, *args, **kwargs)
#         self._orig = self._w + "_orig"

#     def _proxy(self, *args):
#         # let the actual widget perform the requested action
#         cmd = (self._orig,) + args
#         result = self.call(cmd)

#         # generate an event if something was added or deleted,
#         # or the cursor position changed
#         if (args[0] in ("insert", "replace", "delete") or 
#             args[0:3] == ("mark", "set", "insert") or
#             args[0:2] == ("xview", "moveto") or
#             args[0:2] == ("xview", "scroll") or
#             args[0:2] == ("yview", "moveto") or
#             args[0:2] == ("yview", "scroll")
#         ):
#             self.event_generate("<<Change>>", when="tail")

#         # return what the actual widget returned
#         return result

class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

root = Tk()
LineIndicator(root).pack(side="top", fill="both", expand=True)
root.mainloop()