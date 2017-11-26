from Tkinter import *
from opcthread import *

import util
from util import res

'''
	Window Class 
'''
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.exec_type = 0
        self.poll()

    def poll(self):
        global lst_command
        global cur_status

        if util.is_connected:
            if util.cur_status != '':
                self.cur_status.config(text=util.cur_status)
                self.cur_status.update_idletasks()

            for item in os.listdir(res['INVENTIA']['JSON_DIR']):
                item_path = os.path.join(res['INVENTIA']['JSON_DIR'], item)
                if os.path.isfile(item_path):
                    # print item
                    matches = re.search(util.JSON_REGEX, item)
                    if matches is not None:
                        stt_name = matches.group(1)
                        idx = matches.group(2)

                        util.lst_command[idx] = stt_name

                        os.rename(item_path, 'STORAGE\\' + item)
        else:
            pass
        self.master.after(100, self.poll)

    def init_window(self):
        self.master.title("OPC Client")

        for i in range(0, 7):
            for j in range(0, 4):
                lbl = Label(self.master, anchor=W, width=6)
                lbl.grid(column=i, row=j)
        self.gen_lbl = Label(self.master, text=res['naming']['PROG_NAME'], font=(None, 12), anchor=W)
        self.gen_lbl.grid(column=0, row=0, columnspan=7, rowspan=2)

        self.connect_btn = Button(self.master, text=res['naming']['BTN_DISCONNECT'], command=self.connect_server)
        self.connect_btn.grid(column=2, row=2, columnspan=3, rowspan=2)

        self.status = Label(self.master, text=res['naming']['LBL_STATUS'], anchor=W, padx=3, relief=RIDGE, borderwidth=1)
        self.status.grid(column=0, row=4, columnspan=1)
        self.cur_status = Label(self.master, text="OK", anchor=W, relief=RIDGE, borderwidth=1, width=45)
        self.cur_status.grid(column=1, row=4, columnspan=6)

    def connect_server(self):
        util.is_connected = not util.is_connected

        if util.is_connected:
            self.connect_btn.config(text=res['naming']['BTN_DISCONNECT'])
            self.cur_status.config(text=res['naming']['LBL_CONNECT_OK'])
        else:
            self.connect_btn.config(text=res['naming']['BTN_CONNECT'])
            self.cur_status.config(text=res['naming']['LBL_CONNECT_NG'])
        print util.is_connected

'''
	on_closing function 
'''
def on_closing():
    util.lock.acquire()
    try:
        util.is_running = False
    finally:
        util.lock.release()
    print 'is_running : ' + str(util.is_running)
    opc.join()
    root.destroy()


opc = OpcThread()
opc.start()
root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
app = Window(root)
app.master.mainloop()

''' 
================================================================================
								END OF FILE
================================================================================
''' 