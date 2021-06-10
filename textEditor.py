# -*- coding: utf-8 -*-
import os
import json
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.font import Font
from stylePopup import StylePopup
from searchPopup import SearchPopup
from os import listdir, replace, sep
from os.path import isfile, join

PROP_FILE_PATH = 'settings.json'

class TextEditor():
    '''텍스트 편집기'''
    def __init__(self, root):
        self.root = root
        self.TITLE = "P.Y Editor 1.0"
        self.current_Dir = "C:/PY_Editor"
        self.file_path = None
        self.set_title()
        
        frame = Frame(self.root)
        frame2 = Frame(self.root)
        
        self.frame = frame
        self.frame2 = frame2
        self.draw_gui()
        self.draw_file_list()
        

        frame2.pack(side="left", fill="both", expand=1)
        frame.pack(side="right", fill="both", expand=1)
        
        self.root.protocol("WM_DELETE_WINDOW", self.file_quit)
        self.make_menu()
        self.bind_events()

    def draw_gui(self):
        self.yscrollbar = Scrollbar(self.frame, orient="vertical")
        self.editor = Text(self.frame, yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.config(command=self.editor.yview)
        self.yscrollbar.pack(side="right", fill="y")
                
        self.linenumbers = TextLineNumbers(self.frame, width=30)
        self.linenumbers.attach(self.editor)
        self.linenumbers.pack(side="left", fill="both", expand=1)
        
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.config(wrap="word", undo=True, width=80)
        self.editor.focus()

    def draw_file_list(self):
        fileExplorer = Frame(self.frame2, width=150)
        # fileExplorer.pack(side="left", fill='both', expand=1)
        fileExplorer.grid(row=0, column=0)
        onlyFiles = [f for f in listdir(self.current_Dir) if isfile(join(self.current_Dir, f))]
        for i, fileName in enumerate(onlyFiles):
            lb = Label(self.frame2, text=fileName)
            realPath = join(self.current_Dir, fileName).replace("\\", "/")
            print(i, realPath, self.file_path)
            
            if(self.file_path != None):
                if realPath.lower() == self.file_path.lower():
                    lb.configure(bg="red")
                    print(i, "일치 !")
            lb.grid(row=i, column=0, sticky=W)

    def make_menu(self):
        self.menubar = Menu(self.root)
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
        hmenu.add_command(label="P.Y Editor", command=self.help_showabout)
        self.menubar.add_cascade(label="Help", menu=hmenu)
        
        # 폰트 설정 메뉴 추가
        fmenu = Menu(self.menubar, tearoff=0)
        fmenu.add_command(label="글꼴", command=self.display_font_popup)
        self.menubar.add_cascade(label="Fonts", menu=fmenu)

        dmenu = Menu(self.menubar, tearoff = 0)
        dmenu.add_checkbutton(label="File Explorer")
        self.menubar.add_cascade(label="Show View", menu=dmenu)

        self.root.config(menu=self.menubar)

        properties = self.loadProperties()
        self.style = None
        if properties != None:
            self.style = properties.get('style')

        if self.style is None:
            self.style = {
                'font': 'Gothic',
                'fontWeight': 'normal',
                'fontStyle': 'roman',
                'fontSize': 16,
                'fgColor': 'black',
                'bgColor': 'white'
            }

        self.setStyles()
        
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
                self.draw_file_list()
                
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
        
        # 스타일 설정 정보 저장
        self.saveProperties()

        result = self.save_if_modified()
        
        if result != None:
            self.root.destroy()

    def edit_cut(self, event=None):
        self.editor.event_generate("<<Cut>>")

    def edit_copy(self, event=None):
        self.editor.event_generate("<<Copy>>")

    def edit_paste(self, event=None):
        self.editor.event_generate("<<Paste>>")
        
    def help_showabout(self, event=None):
        helpText = 'P.Y Editor 1.0\n\n'
        helpText += '지원 기능\n'
        helpText += '- 글꼴 선택\n'
        helpText += '- 굵기 선택\n'
        helpText += '- 스타일 설정\n'
        helpText += '- 글씨 크기 설정\n'
        helpText += '- 글꼴 색상 선택\n'
        helpText += '- 배경색 선택\n' 
        helpText += '- 텍스트 검색\n\n'

        helpText += 'P.Y Editor Made by\n' 
        helpText += '- Park Jin Guk\n'
        helpText += '- Yoo Seung Wan\n'

        messagebox.showinfo('P.Y Editor', helpText)

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

        self.editor.bind("<<Change>>", self._on_change)
        self.editor.bind("<Configure>", self._on_change)
        
        
        self.editor.bind("<MouseWheel>", self._on_change)
        self.editor.bind("<KeyRelease>", self._on_change)
        self.editor.bind("<KeyPress>", self._on_change)

        self.editor.bind("<Control-o>", self.file_open)
        self.editor.bind("<Control-O>", self.file_open)
        self.editor.bind("<Control-s>", self.file_save)
        self.editor.bind("<Control-S>", self.file_save)
        
        self.editor.bind("<Control-f>", self.display_search_popup)
        self.editor.bind("<Control-F>", self.display_search_popup)

        self.editor.bind("<Control-y>", self.redo)
        self.editor.bind("<Control-Y>", self.redo)
        self.editor.bind("<Control-z>", self.undo)
        self.editor.bind("<Control-Z>", self.undo)
    
    # StylePopup 생성
    def display_font_popup(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()

        popup = StylePopup(self, self.style,  x, y)

    def display_search_popup(self, event=None):
        x = self.root.winfo_x() + self.root.winfo_width()
        y = self.root.winfo_y()

        popup = SearchPopup(self, x, y)


    def on_child_popup_closed(self, popup, options=None):
        if (type(popup) is StylePopup) and options is not None:
            self.style = options

            self.setStyles()
            # 속성 변경
        elif type(popup) is SearchPopup:
            print('search')
            pass

    def setStyles(self):
        
        fontObject = Font(
            family = self.style.get('font'), 
            size = self.style.get('fontSize'),
            weight = self.style.get('fontWeight'),
            slant = self.style.get('fontStyle')
        )
        
        self.editor.configure(font=fontObject)
        self.editor.config(fg=self.style.get('fgColor'), bg=self.style.get('bgColor'))
        self._on_change(event=None)

    def saveProperties(self):
        props = {
            'style': self.style
        }

        try:
            with open(PROP_FILE_PATH, 'w') as outfile:
                json.dump(props, outfile, indent=4)
        except FileNotFoundError as err:
            print(err)

    def loadProperties(self):
        properties = None
        
        try:
            with open(PROP_FILE_PATH, 'r', encoding='utf8') as readfile:
                
                file = ''
                for line in readfile:
                    file += line

                if len(file) > 0:
                    print(file)
                    properties = json.loads(s=file)
        except FileNotFoundError as err:
            print(err)

        return properties

    def _on_change(self, event):
        self.linenumbers.redraw()

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
