import os
from tkinter import *
from tkinter import filedialog, messagebox
from popup import StylePopup

# 앱 클래스 ㅁㄴㅇㄻㄴㅇㄹ
class TextEditor():
    '''텍스트 편집기'''
    def __init__(self, root):
        self.root = root
        self.TITLE = "TkInter 편집기"
        self.file_path = None
        self.set_title()
        self.__childWindows = []
        
        frame = Frame(root)
        self.yscrollbar = Scrollbar(frame, orient="vertical")
        self.editor = Text(frame, yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.editor.yview)
        self.yscrollbar.pack(side="right", fill="y")
        
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.config(wrap="word", undo=True, width=80)
        self.editor.focus()
        frame.pack(fill="both", expand=1)
        
        root.protocol("WM_DELETE_WINDOW", self.file_quit)
        self.make_menu()
        self.bind_events()
    
    def make_menu(self):
        self.menubar = Menu(root)
        fmenu = Menu(self.menubar, tearoff=0)
        fmenu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        fmenu.add_command(label="Open...", command=self.file_open, accelerator="Ctrl+O")
        fmenu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")
        fmenu.add_command(label="Save As ...", command=self.file_save_as, accelerator="Ctrl+Alt+S")
        fmenu.add_command(label="Exit", command=self.file_quit, accelerator="Alt+F4")
        self.menubar.add_cascade(label="File", menu=fmenu)
        
        emenu = Menu(self.menubar, tearoff=0)
        emenu.add_command(label="Cut", command=self.edit_cut)
        emenu.add_command(label="Copy", command=self.edit_copy)
        emenu.add_command(label="Paste", command=self.edit_paste)
        self.menubar.add_cascade(label="Edit", menu=emenu)

        hmenu = Menu(self.menubar, tearoff=0)
        hmenu.add_command(label="TkEditor 편집기", command=self.help_showabout)
        self.menubar.add_cascade(label="Help", menu=hmenu)
        
        # 폰트 설정 메뉴 추가
        fmenu = Menu(self.menubar, tearoff=0)
        fmenu.add_command(label="글꼴", command=self.display_font_popup)
        self.menubar.add_cascade(label="Fonts", menu=fmenu)

        root.config(menu=self.menubar)
        
    def save_if_modified(self):
        if self.editor.edit_modified():
            caption = '저장 확인'
            msg = '이 파일은 수정되었습니다. 저장하시겠습니까?'
            
            # yes = True, no = False, cancel = None
            response = messagebox.askyesnocancel(caption, msg)
            if response:
                result = self.file_save()
                if result == 'saved':
                    return True # if it's saved succesfully
                else: 
                    return None # failed to save
            else:
                return response # choose no or cancel
        else:
            return True # nothing to changes
        
    def file_new(self, event=None):
        result = self.save_if_modified()
        if result != None:
            # Clear editor
            self.editor.delete(1.0, "end")
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.file_path = None
            self.set_title()
            
    def file_open(self, event=None, filepath=None):
        def readfile(filepath):
            try:
                with open(filepath, encoding="utf-8") as f:
                    fileContents = f.read()
            except FileNotFoundError as e:
                print(e)
                print('파일 읽기 실패!'.center(30, '*'))
            else:
                # append strings to editor from file
                self.editor.delete(1.0, "end")
                self.editor.insert(1.0, fileContents)
                self.editor.edit_modified(False)
                self.file_path = filepath
                print('파일 읽기 완료!'.center(30, '*'))
            
        result = self.save_if_modified()
        if result != None:
            if filepath == None:
                filepath = filedialog.askopenfilename()
            if filepath != None and filepath != '':
                readfile(filepath)
                self.set_title()
                
    def file_save(self, event=None):
        if self.file_path == None:
            result = self.file_save_as()
        else:
            result = self.file_save_as(filepath = self.file_path)
        return result

    def file_save_as(self, event=None, filepath=None):
        if filepath == None:
            ftypes = (('Text files', '*.txt'), ('Python files', '*.py *.pyw'), ('All files', '*.*'))
            filepath = filedialog.asksaveasfilename(filetypes=ftypes)
            print(filepath)

        text = self.editor.get(1.0, "end-1c")
        # 사용자 편의 기능 1. 파일명만 입력 했을 때 확장자를 자동으로 입력해줌
        if len(filepath) > 0:
            if filepath.find('.') == -1:
                filepath = filepath + '.txt'
                
            try:
                with open(filepath, 'wb') as f:
                    f.write(bytes(text, 'UTF-8'))
            except FileNotFoundError as e:
                print(e)
                print('파일 쓰기 실패!'.center(30, '*'))
            else:
                self.editor.edit_modified(False)
                self.file_path = filepath
                self.set_title()
                return 'saved'
        else:
            print('저장 취소')

    def file_quit(self, event=None):
        '''종료 버튼이나 메뉴 Exit를 클릭하면 실행'''
        result = self.save_if_modified()
        
        # Close all child windows
        for popup in self.__childWindows:
            try:
                popup.destroy()
            except Exception as e:
                print(e)
            
        if result != None:
            self.root.destroy()

    def edit_cut(self, event=None):
        self.editor.event_generate("<<Cut>>")

    def edit_copy(self, event=None):
        self.editor.event_generate("<<Copy>>")

    def edit_paste(self, event=None):
        self.editor.event_generate("<<Paste>>")
        
    def help_showabout(self, event=None):
        messagebox.showinfo('TkInter 편집기', 'TkInter 편집기 버전 0.1')

    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = 'Untitled'
        self.root.title(title + ' = ' + self.TITLE)

    def undo(self, event=None):
        self.editor.edit_undo()

    def redo(self, event=None):
        self.editor.edit_redo()

    def bind_events(self, event=None):
        self.editor.bind("<Control-o>", self.file_open)
        self.editor.bind("<Control-O>", self.file_open)
        self.editor.bind("<Control-s>", self.file_save)
        self.editor.bind("<Control-S>", self.file_save)
        self.editor.bind("<Control-y>", self.redo)
        self.editor.bind("<Control-Y>", self.redo)
        self.editor.bind("<Control-z>", self.undo)
        self.editor.bind("<Control-Z>", self.undo)
    
    def display_font_popup(self):
        print(self)
        popup = StylePopup(self)
        popup.createGUI()
        
        self.__childWindows.append(popup)
        print(self.__childWindows)

    def removeChildWindow(self, child):
        self.__childWindows.remove(child)
        
root = Tk()
root.geometry('800x600')
editor = TextEditor(root)
root.mainloop()
