# -*- coding: utf-8 -*-
import os
import json
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.font import Font
from stylePopup import StylePopup
from searchPopup import SearchPopup
from autocompPopup import AutocompPopup
from os import listdir, replace, sep
from os.path import isfile, join
import copy as copy

PROP_FILE_PATH = 'settings.json'

class TextEditor():
    '''텍스트 편집기'''
    def __init__(self, root):
        self.root = root
        self.TITLE = "P.Y Editor 1.0"
        self.current_dir = None
        self.file_path = None
        self.options = None
        self.auto_completes = None

        # child windows
        self.__stylePopup = None
        self.__searchPopup = None
        self.__autocompPopup = None

        self.set_title()
        
        frame = Frame(self.root)
        frame2 = Frame(self.root, width=150)
        
        self.frame = frame
        self.frame2 = frame2
        
        frame2.pack(side="left", fill="both", expand=1)
        frame.pack(side="right", fill="both", expand=1)

        self.root.protocol("WM_DELETE_WINDOW", self.file_quit)
        
        # draw gui는 properties 영향 X
        self.draw_gui()
        self.loadProperties()
        
        # menu, showView 는 properties 영향 받음
        self.make_menu()
        
        self.changeShowTabs()
        self.bind_events()


    def draw_gui(self):
        # vertical scrollbar
        self.yscrollbar = Scrollbar(self.frame, orient="vertical")
        self.yscrollbar.pack(side="right", fill="y")

        # horizontal scrollbar
        self.xscrollbar = Scrollbar(self.frame, orient="horizontal")
        self.xscrollbar.pack(side="bottom", fill="x")

        # line counter
        self.linenumbers = TextLineNumbers(self.frame, width=30, relief='sunken', borderwidth=1)
        self.linenumbers.pack(side="left", fill="both", expand=1)
        
        self.editor = Text(self.frame, yscrollcommand=self.yscrollbar.set, wrap="none", xscrollcommand=self.xscrollbar.set)
        self.editor.pack(side="left", fill="both", expand=1)
        self.editor.config(undo=True, width=80)
        self.editor.focus()

        self.editor.tag_configure("current_line", background="#e9e9e9")
        self.editor.tag_configure("search_keyword", background="#e9e9e9")
        self._highlight_current_line()
        self.yscrollbar.config(command=self.editor.yview)
        self.xscrollbar.config(command=self.editor.xview)
        self.linenumbers.attach(self.editor)

    def displayFileExplorer(self):

        for child in self.frame2.winfo_children():
            child.destroy()
        
        if self.current_dir != None:

            onlyFiles = [f for f in listdir(self.current_dir) if isfile(join(self.current_dir, f))]
            for i, fileName in enumerate(onlyFiles):
                lb = Label(self.frame2, text=fileName)
                realPath = join(self.current_dir, fileName).replace("\\", "/")
                lb.bind("<Double-Button-1>", (lambda e: self.file_open(filepath=join(self.current_dir, e.widget.cget("text")).replace("\\", "/"))))
                
                if(self.file_path != None):
                    if realPath.lower() == self.file_path.lower():
                        lb.configure(bg="red")

                lb.grid(row=i, column=0, sticky=W)
        else:
            openFolder = Button(self.frame2, text="Open Folder", command=self.folder_open)
            openFolder.grid(row=0, column=0)
        self.linenumbers.redraw(event=None)

    def make_menu(self):
        self.menubar = Menu(self.root)
        fmenu = Menu(self.menubar, tearoff=0)
        fmenu.add_command(label="New", command=self.file_new, accelerator="Ctrl+N")
        fmenu.add_command(label="Open...", command=self.file_open, accelerator="Ctrl+O")
        fmenu.add_command(label="Open Folder...", command=self.folder_open, accelerator="Ctrl+D")
        fmenu.add_command(label="Save", command=self.file_save, accelerator="Ctrl+S")
        fmenu.add_command(label="Save As ...", command=self.file_save_as, accelerator="Ctrl+Alt+S")
        fmenu.add_separator()
        fmenu.add_command(label="Exit", command=self.file_quit, accelerator="Alt+F4")
        self.menubar.add_cascade(label="File", menu=fmenu)
        
        emenu = Menu(self.menubar, tearoff=0)
        emenu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        emenu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        emenu.add_separator()
        emenu.add_command(label="Cut", command=self.edit_cut, accelerator="Ctrl+X")
        emenu.add_command(label="Copy", command=self.edit_copy, accelerator="Ctrl+C")
        emenu.add_command(label="Paste", command=self.edit_paste, accelerator="Ctrl+C")
        self.menubar.add_cascade(label="Edit", menu=emenu)
        
        # 폰트 설정 메뉴 추가
        fmenu = Menu(self.menubar, tearoff=0)
        fmenu.add_command(label="글꼴", command=self.display_style_popup)
        self.menubar.add_cascade(label="Style", menu=fmenu)

        dmenu = Menu(self.menubar, tearoff = 0)
        
        fileExplorerEnable = BooleanVar()
        fileExplorerEnable.set(True)

        if(self.options.get('showView').get('fileExplorer') is not None):
            fileExplorerEnable.set(self.options.get('showView').get('fileExplorer'))
        
        self.fileExplorerEnable = fileExplorerEnable
        dmenu.add_checkbutton(label="File Explorer", variable=self.fileExplorerEnable, onvalue=1, offvalue=0, command=(lambda: self.changeShowTabs()))
        self.menubar.add_cascade(label="Show", menu=dmenu)

        hmenu = Menu(self.menubar, tearoff=0)
        hmenu.add_command(label="도움말", command=self.help_showabout)
        hmenu.add_command(label="자동완성", command=self.display_autocomp_popup)
        self.menubar.add_cascade(label="Features", menu=hmenu)

        self.root.config(menu=self.menubar)
        
    def changeShowTabs(self, event=None):

        self.options.get('showView')['fileExplorer'] = self.fileExplorerEnable.get()
        if(not self.fileExplorerEnable.get()):
            self.frame2.pack_forget()
        else:
            self.frame.pack_forget()
            
            self.frame2.pack(side="left", fill="both", expand=1)
            self.frame.pack(side="right", fill="both", expand=1)
            self.displayFileExplorer()


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
                self.displayFileExplorer()

    def folder_open(self, event=None, dirPath=None):
        result = self.save_if_modified()
        if result != None:
            if dirPath == None:
                dirPath = filedialog.askdirectory()
            
            self.current_dir = dirPath
            try:
                self.displayFileExplorer()
            except FileNotFoundError as err:
                print("폴더 열기 실패")
                self.current_dir = None
                self.displayFileExplorer()

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

    # 도움말
    def help_showabout(self, event=None):
        helpText = 'P.Y Editor 1.0\n\n'
        helpText += '- 지원 기능\n'
        helpText += ' 1. 글꼴 선택\n'
        helpText += ' 2. 글꼴 굵기 선택\n'
        helpText += ' 3. 글꼴 스타일 설정\n'
        helpText += ' 4. 글씨 크기 설정\n'
        helpText += ' 5. 글꼴 색상 선택\n'
        helpText += ' 6. 배경색 선택\n' 
        helpText += ' 7. 텍스트 검색\n'
        helpText += ' 8. 사용자 설정 저장 및 불러오기\n'
        helpText += ' 9. 줄간격 조정\n'
        helpText += '10. 키워드 자동완성\n'
        helpText += '11. 자동완성 설정 저장\n'
        helpText += '12. 파일 익스플로러\n'
        helpText += '13. showTabs 설정 저장 및 불러오기\n'
        helpText += '14. 폴더 오픈\n'
        helpText += '15. 마지막 연 디렉터리 path 저장\n'
        helpText += '16. 도움말(기능 설명)\n'
        helpText += '17. 기능 단축키 구현\n\n'

        helpText += '- 유저 편의사항\n'
        helpText += ' 1. 사용자가 파일 확장자를 지정하지 않으면 자동으로 .txt파일로 저장\n'
        helpText += ' 2. 행 번호 표시\n'
        helpText += ' 3. Show - 파일 익스플로러 탭 활성화 상태 표시\n'
        helpText += ' 4. xscrollbar 추가\n'
        helpText += ' 5. 커서 색상과 글자 색상 동기화\n'
        helpText += ' 6. 커서가 위치한 줄 강조\n\n'

        helpText += 'P.Y Editor Made by\n' 
        helpText += '- Park Jin Guk\n'
        helpText += '- Yoo Seung Wan\n'

        messagebox.showinfo('P.Y Editor', helpText)

    def set_title(self, event=None):
        if self.file_path != None:
            title = os.path.basename(self.file_path)
        else:
            title = 'Untitled'
        self.root.title(title + ' - ' + self.TITLE)

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

        # 줄바꿈 표시를 위해 등록
        self.editor.bind("<<Change>>", self.linenumbers.redraw)
        self.editor.bind("<Configure>", self.linenumbers.redraw)
        self.editor.bind("<MouseWheel>", self.linenumbers.redraw)
        self.editor.bind("<KeyRelease>", self.linenumbers.redraw)
        self.editor.bind("<KeyPress>", self.linenumbers.redraw)
        # 줄바꿈 표시 등록 끝

        # 폴더 열기
        self.editor.bind("<Control-d>", self.folder_open)
        self.editor.bind("<Control-D>", self.folder_open)

        # 도움말 단축키 추가
        self.editor.bind("<F1>", self.help_showabout)

        # File Explorer toggle
        self.editor.bind("<Control-Shift-e>", self.fileExplorerToggle)
        self.editor.bind("<Control-Shift-E>", self.fileExplorerToggle)
        
        # 스타일 팝업
        self.editor.bind("<Control-Shift-f>", self.display_style_popup)
        self.editor.bind("<Control-Shift-F>", self.display_style_popup)

        # 단어 검색 팝업
        self.editor.bind("<Control-f>", self.display_search_popup)
        self.editor.bind("<Control-F>", self.display_search_popup)
        
        # 자동완성 활성화 키
        self.editor.bind("<Control-space>", self._auto_complete)

        
    # File Explorer 토글 표시
    def fileExplorerToggle(self, event=None):
        self.fileExplorerEnable.set(not self.fileExplorerEnable.get())
        self.changeShowTabs()

    # StylePopup 표시
    def display_style_popup(self, event=None):

        if self.__stylePopup is None:
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.__stylePopup = StylePopup(self, self.style,  x, y)
        
        self.__stylePopup.lift()

    # SearchPopup 표시
    def display_search_popup(self, event=None):
        if self.__searchPopup is None:
            x = self.root.winfo_x() + self.root.winfo_width()
            y = self.root.winfo_y()

            self.__searchPopup = SearchPopup(self, x, y)
        
        self.__searchPopup.lift()

    # AutocompPopup 표시
    def display_autocomp_popup(self, event=None):

        if self.__autocompPopup is None:
            x = self.root.winfo_x()
            y = self.root.winfo_y()
            self.__autocompPopup = AutocompPopup(self,  x, y, auto_completes=self.auto_completes)
        
        self.__autocompPopup.lift()


    # listen popup close
    def on_child_popup_closed(self, popup, options=None):
        if (type(popup) is StylePopup):
            if options is not None:
                self.style = options
                self.setStyles()
            
            self.__stylePopup = None
            # 속성 변경
        elif type(popup) is SearchPopup:
            self.__searchPopup = None
        elif type(popup) is AutocompPopup:
            if options is not None:
                self.auto_completes = options
            self.__autocompPopup = None

    # 스타일 적용
    def setStyles(self):
        print(self.style)
        fontObject = Font(
            family = self.style.get('font'), 
            size = self.style.get('fontSize'),
            weight = self.style.get('fontWeight'),
            slant = self.style.get('fontStyle'),
        )
        
        self.editor.configure(font=fontObject, insertbackground=self.style.get('fgColor')) # cursor색상 == font색상
        self.editor.config(fg=self.style.get('fgColor'), bg=self.style.get('bgColor'), spacing3=self.style.get('lineSpace'))
        self.linenumbers.redraw(event=None)

    # 설정들 Json으로 저장
    def saveProperties(self):
        props = {
            'style': self.style,
            'options': self.options,
            'current_dir': self.current_dir,
            'auto_completes': self.auto_completes
        }

        try:
            with open(PROP_FILE_PATH, 'w') as outfile:
                json.dump(props, outfile, indent=4)
        except FileNotFoundError as err:
            print(err)

    # 설정 Load
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

        self.style = None
        self.options = None
        self.current_dir = None
        self.auto_completes = None

        if properties != None:
            self.style = properties.get('style')
            self.options = properties.get('options')
            self.current_dir = properties.get('current_dir')
            self.auto_completes = properties.get('auto_completes')

        # 이 아래로 기본값 대입
        if self.style is None:
            self.style = {
                'font': 'System',
                'fontWeight': 'normal',
                'fontStyle': 'roman',
                'fontSize': 16,
                'lineSpace': 1,
                'fgColor': 'black',
                'bgColor': 'white'
            }

        self.setStyles()

        if self.options is None:
            self.options = {
                'showView': {
                    'fileExplorer': True
                }
            }

        if self.auto_completes is None:
            self.auto_completes = dict()

    # Editor에서 수정 이벤트 발생시 실행
    def _on_change(self, event):
        self.linenumbers.redraw()

    # 현재 라인 표시
    def _highlight_current_line(self, interval=100):
        '''현재 줄 표시 0.1초마다 갱신'''
        self.editor.tag_remove("current_line", 1.0, "end")
        self.editor.tag_add("current_line", "insert linestart", "insert lineend+1c")
        self.root.after(interval, self._highlight_current_line)

    # 자동 완성
    def _auto_complete(self, event=None):
        editor = self.editor
        temp = editor.index(INSERT)
        
        startIndex, endIndex, word = self.__find_word(editor, temp)
        
        if word in self.auto_completes.keys():
            replacedWord = self.auto_completes.get(word)
            editor.delete(startIndex, endIndex)
            editor.insert(startIndex, replacedWord)
        else:
            print("nothing to change")

    # 현재 커서가 위치한 단어 검색
    def __find_word(self, editor: Text, index):
        _startIndex = self.indexArth(index, plus=False)
        _endIndex = index

        word = ''
        while(True):
            startChar = editor.get(_startIndex).strip()
            endChar = editor.get(_endIndex).strip()
            
            startCol = int(_startIndex.split('.')[1])

            if startChar != '' and startCol >= 0:
                word = startChar + word
                _startIndex = self.indexArth(_startIndex, plus=False)

            if endChar != '':
                word = word + endChar
                _endIndex = self.indexArth(_endIndex, plus=True)

            if ((startChar == '' or startCol < 0)
                and endChar == ''):
                break
        
        return _startIndex, _endIndex, word

    # 에디터 커서 index 증가/ 감소
    def indexArth(self, index, plus=True):
        row, col = index.split('.')
        col = int(col) + 1 if plus else int(col) - 1
        return row + '.' + str(col)

class TextLineNumbers(Canvas):
    '''행번호 표시 기능을 위한 객체'''
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args, event=None):
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

    def setShowViewTabs(self):
        for key in self.options.showView:
            tab = self.options.showView.get(key)
            print(tab)
