# coding=UTF-8
"""
Created on 2014-10-24

@author: iAmFarago@gmail.com
"""

import os
from tkinter import *
from tkinter import messagebox

import redis


CFG_SEC__DB = "DB"
CFG_KEY__DB_HOST = "host"
CFG_KEY__DB_PORT = "port"
CFG_KEY__DB_USER = "user"
CFG_KEY__DB_PWD = "password"
CFG_KEY__DB_AUTH = "auth"
CFG_KEY__DB_NAME = "db_name"
CFG_SEC__FILE = "FILE"
CFG_KEY__FILE_REPO_DIR = "repo_dir"
CFG_KEY__FILE_PKG_INFO = "package_info"

MENU_FONT_STYLE = 'Arial sans serif'
MENU_FONT_STYLE_CHAR = 'courier new'
NENU_BACKGROUND_COLOR = 'white'
MENU_FOREGROUND_COLOR = '#225588'
GLOB_FONT_SIZE_normal = 12
GLOB_FONT_WEIGHT = 'normal'

BUTTON_TEXT__GO_PROCESS = '执行，Go !!'
BUTTON_TEXT__PROCESSING = "正在处理..."

PYTHON_VERSION = "Python3.4.2"
SOFTWARE_VERSION = "1.0.0_Beta"
PANEL_TITLE = 'Redis Python客户端 - by Tanj(v_' + SOFTWARE_VERSION + ')'

ABOUT_ME = '''
作者：Tanj（谭剑）
来自：多好科技（http://www.farago.tech）
Email：arantam@qq.com
QQ：112960591
发布时间：2014-10-24
更新时间：2014-10-24
'''
ABOUT_VERSION = '''开发工具：''' + PYTHON_VERSION + '''
当前软件版本为：''' + SOFTWARE_VERSION
ABOUT_TUTORIAL = '该工具为操作Redis的Python客户端，可输入命令并显示操作结果'


class Fedis(object):
    def __init__(self):
        # 初始化
        self.top = Tk()
        # 标题和图标
        self.top.title('Redis-Python客户端 版本：' + SOFTWARE_VERSION)  # 窗口标题
        self.top.iconbitmap('fedis.ico')  # 更换tk图标
        self.top.resizable(0, 0)
        # 菜单
        menubar = Menu(self.top)
        file_menu = Menu(menubar, tearoff=0, fg='#225588', bg='white',
                         font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal, GLOB_FONT_WEIGHT))
        file_menu.add_command(label='退出(X)', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal), command=self.close_and_exit)
        menubar.add_cascade(label='文件(F)', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal, GLOB_FONT_WEIGHT),
                            menu=file_menu)
        about_menu = Menu(menubar, tearoff=0, fg=MENU_FOREGROUND_COLOR, bg=NENU_BACKGROUND_COLOR)
        about_menu.add_command(label='使用说明', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal), command=self.abouttutorial)
        about_menu.add_command(label='关于作者', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal), command=self.aboutauthor)
        about_menu.add_command(label='关于本工具', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal), command=self.aboutsoftware)
        menubar.add_cascade(label="帮助(H)", menu=about_menu)
        self.top.config(menu=menubar, bg="#225588")

        # # --
        self.frame1 = Frame(self.top, width=720)
        # 输入框 -- 主机
        Label(self.frame1, text="Redis主机:", font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal)).grid(row=0, column=0,
                                                                                                sticky=E, pady=3,
                                                                                                padx=1)
        self.hostVar = StringVar()
        self.hostEntry = Entry(self.frame1, textvariable=self.hostVar,
                               font=(MENU_FONT_STYLE_CHAR, GLOB_FONT_SIZE_normal), width=30)
        self.hostEntry.grid(row=0, column=2, sticky=W, pady=3, padx=1)
        self.hostVar.set("")
        self.hostEntry.focus_set()
        # 输入框 -- 端口
        Label(self.frame1, text='端口:', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal)).grid(row=0, column=3, sticky=E,
                                                                                           pady=3,
                                                                                           padx=1)
        self.portVar = StringVar()
        self.portEntry = Entry(self.frame1, textvariable=self.portVar,
                               font=(MENU_FONT_STYLE_CHAR, GLOB_FONT_SIZE_normal), width=8).grid(row=0, column=4,
                                                                                                 sticky=W, pady=1,
                                                                                                 padx=1)
        self.portVar.set("")

        # 输入框 -- 签名
        Label(self.frame1, text='签名:', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal)).grid(row=0, column=5, sticky=E,
                                                                                           pady=3,
                                                                                           padx=1)
        self.authVar = StringVar()
        self.authEntry = Entry(self.frame1, textvariable=self.authVar,
                               font=(MENU_FONT_STYLE_CHAR, GLOB_FONT_SIZE_normal), width=8).grid(row=0, column=6,
                                                                                                 sticky=W, pady=1,
                                                                                                 padx=1)
        self.portVar.set("")
        # 按钮 -- 测试连通性
        Button(self.frame1, text="测试连接", command=self.test_connection, fg='#0d0', bg='white',
               font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal, GLOB_FONT_WEIGHT)).grid(row=0, column=7, sticky=EW, pady=1,
                                                                                     padx=1)
        # # --
        self.frame2 = Frame(self.top, width=720)
        # 输入命令
        Label(self.frame2, text="输入命令：", font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal)).grid(row=1, column=0,
                                                                                             sticky=E, pady=3,
                                                                                             padx=1)
        self.cmdVar = StringVar(self.frame2)
        self.cmdEntry = Entry(self.frame2, textvariable=self.cmdVar,
                              font=(MENU_FONT_STYLE_CHAR, GLOB_FONT_SIZE_normal), width=76)
        # self.cmdEntry.bind('<Return>', self.go_process)
        self.cmdEntry.grid(row=1, column=1, sticky=W, pady=3, padx=1)
        self.cmdVar.set("在这里输入Redis命令")

        self.frame3 = Frame(self.top, width=720)
        # 流类型
        Label(self.frame3, text='编码方式:', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal)).grid(row=0, column=0, sticky=E,
                                                                                             pady=3, padx=1)
        self.endecFlag = IntVar(self.frame3)
        Radiobutton(self.frame3, variable=self.endecFlag, value=1, text='字符').grid(row=0, column=1, sticky=W)
        Radiobutton(self.frame3, variable=self.endecFlag, value=2, text='字节').grid(row=0, column=2, sticky=W)
        self.endecFlag.set(1)
        # 按钮 - 执行生成文件处理
        self.goProcessButton = Button(self.frame3, text="执行，Go !!", command=self.go_process, fg='blue',
                                      bg='white', font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal, GLOB_FONT_WEIGHT))
        self.goProcessButton.grid(row=0, column=3, sticky=E, pady=3, padx=1, columnspan=2)
        # self.goProcessButton.config(state='disabled')

        # # --
        self.frame4 = Frame(self.top, width=720, height=100)
        # 显示查询结果
        self.labelFrame = LabelFrame(self.frame4, text='查询结果',
                                     font=(MENU_FONT_STYLE, GLOB_FONT_SIZE_normal, GLOB_FONT_WEIGHT))
        self.labelFrame.pack(side=LEFT, ipadx=20, fill=BOTH, expand=1)
        self.resultArea = Text(self.labelFrame, font=(MENU_FONT_STYLE_CHAR, GLOB_FONT_SIZE_normal), width=30)
        self.resultArea.pack(side=LEFT, fill=BOTH, expand=1)

        # frameX.pack()
        self.frame1.pack(expand=YES, fill=BOTH)
        self.frame2.pack(expand=YES, fill=BOTH)
        self.frame3.pack(expand=YES, fill=BOTH)
        self.frame4.pack(expand=YES, fill=BOTH)

    def validate_host_port_cfg(self):
        host = self.hostVar.get()
        port = self.portVar.get()
        if host.strip() == "":
            messagebox.showwarning('警告', "请填写'主机'!")
            return False
        hostRegexp = re.compile(r'(([12][0-9][0-9]|[1-9][0-9]|[1-9])\.){3}([12][0-9][0-9]|[1-9][0-9]|[1-9])')
        if host.upper() != 'LOCALHOST' and not hostRegexp.match(host):
            messagebox.showwarning('警告', "非法的主机: \n" + host)
            return False
        if port.strip() == "":
            messagebox.showwarning('警告', "请填写'端口'!")
            return False
        if not port.isalnum():
            messagebox.showwarning('警告', "非法的端口: \n" + host)
            return False
        return True

    # click close_button
    def close_and_exit(self, event=None):
        self.top.quit()

    # test connection
    def test_connection(self):
        isvalid = self.validate_host_port_cfg()
        if not isvalid:
            return isvalid
        try:
            r = redis.StrictRedis(host=self.hostVar.get(), port=self.portVar.get(), password=self.authVar.get())
            pingmsg = r.ping()
        except redis.exceptions.ConnectionError as e:
            messagebox.showerror('错误', '连接Redis服务失败，请检查配置！错误代码=' + str(e))
            return False
        if pingmsg:
            messagebox.showinfo('提示', 'Redis服务连接 OK')
            return True
        else:
            messagebox.showinfo('提示', '连接不成功！请确认主机名称和端口号是否填写正确，或Redis服务是否已启动！')
            return False

    # connect to Redis
    def connect_redis(self):
        faredis = redis.StrictRedis(host=self.hostVar.get(), port=self.portVar.get(), password=self.authVar.get())
        try:
            resp = faredis.execute_command(self.cmdVar.get())
            # str(b'','utf-8')可以吧BYTES转换成unicode;bytes('','utf-8')反向操作
            self.response_proc(resp)
        except redis.exceptions.ResponseError as e:
            messagebox.showerror('错误', '执行命令失败！错误代码=' + str(e))
            return

    def response_proc(self, resp):
        self.resultArea.delete(1.0, END)
        if type(resp) == type(None):
            self.resultArea.insert(1.0, 'None')
            return
        if type(resp) == type(b''):
            resp = str(resp, 'utf-8')

        if type(resp) == type('str'):
            self.resultArea.insert(1.0, resp)
        elif type(resp) == type([]):
            for item in resp:
                self.resultArea.insert(1.0, '({0}) {1}\n'.format(resp.index(item), str(item, 'utf-8')))
        elif type(resp) == type({}):
            for k, v in resp:
                self.resultArea.insert(1.0, str(k) + '=' + str(v))
        elif type(resp) == type(()):
            for item in resp:
                self.resultArea.insert(1.0, '({0}) {1}\n'.format(resp.index(item), str(item, 'utf-8')))
        else:
            messagebox.showerror('错误', '未知的数据类型')

    def go_process(self):
        self.goProcessButton['text'] = BUTTON_TEXT__GO_PROCESS
        self.connect_redis()

    @staticmethod
    def aboutauthor():
        messagebox.showinfo("关于作者", ABOUT_ME)

    @staticmethod
    def aboutsoftware():
        messagebox.showinfo("软件版本", ABOUT_VERSION)

    @staticmethod
    def abouttutorial():
        messagebox.showinfo("使用说明", ABOUT_TUTORIAL)


def main():
    Fedis()
    # show
    mainloop()


def _fix_run_path():
    # 当前运行目录；
    _prog_cur_path = os.getcwd()
    # 调用命令；
    _prog_run_path = os.path.dirname(sys.argv[0])
    # 如果获取运行目录失败，或者在运行目录下执行该程序；
    if not _prog_run_path:
        return
    # 切换目录到程序所在目录；
    if _prog_cur_path != _prog_run_path:
        os.chdir(_prog_run_path)
    return


if __name__ == '__main__':
    _fix_run_path()
    main()
