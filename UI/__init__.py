# -*- coding: utf-8 -*-

from Tkinter import *
from ttk import *
import db
import tkFileDialog
import read_excel
import write_excel


# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args , **kw)            
#         Frame.size(1000,1000)
        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set,height = 500,width = 700)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
#id 姓名 电话 学术职称 医学职称  医院大名 医院小名 科室 擅长
list_data = ['操作','编号','省','市', '  姓名','  电话','学术职称','医学职称', '医院(大名)','医院(小名)', '科室', '擅长','简介']
table_list =['操作','ID','SHENG','SHI','NAME','PHONE','XUESHUZHICHENG','YIXUEZHICHENG','YIYUAN_DAMING','YIYUAN_XIAOMING','KESHI','SHANCHANG','jianjie']
map_ent = [];

def insert_diag():
    filename = tkFileDialog.askopenfilename()
    print 111
    if(len(filename)>0):
        print filename
        read_excel.excel_table_byindex(filename)

def out_diag():
    filename = tkFileDialog.asksaveasfilename()
    print filename
    if(len(filename)>0):
        write_excel.write_xls(get_data_by_where(), filename)

# 获取输入的内容
seac_key =' 1=1 '

def get_data_by_where():
    global seac_key
    seac_key = ' 1=1 '
    for list_index in range(len(list_data) - 1):
        ent = map_ent[list_index]
        key = ent.get()
        if len(key) > 0:
            jion_sea_key(key, list_index)
    
    couser = db.show_like_doctor(seac_key)
    return couser

def GetValue():
    app.rm_all_text()
    couser = get_data_by_where()
    app.show_data(couser, 0)
 
# 进行字 SQL 语句拼接
def jion_sea_key(key,index_list):
    global seac_key
    seac_key =  seac_key+ '  and '+table_list[index_list+1]+ " like '%"+key+"%'" 
    
def clear_text():
    for list_index in range(len(list_data) - 1):
        ent = map_ent[list_index]
        ent.delete(0,'end')
              

def createTtitle(root, start, stop):
    framet_title = Frame(root);
    framet_title.pack(anchor=W)  # 创建表头的 frame
    for index in range(start, stop):
        Label(framet_title, text=list_data[index] + ':   ').pack(side=LEFT)
        ent = Entry(framet_title)
        ent.pack(side=LEFT)
        map_ent.append(ent)
    if stop ==len(list_data):
        button = Button(framet_title, text='搜索', command=GetValue)
        button.pack(side=LEFT)
        button = Button(framet_title, text='导入数据', command=insert_diag)
        button.pack(side=LEFT)
        button = Button(framet_title, text='导出数据', command=out_diag)
        button.pack(side=LEFT)
        button = Button(framet_title, text='清空', command=clear_text)
        button.pack(side=LEFT)
        
def setwidth(index):
    if index in (0,1):
        return 6
    if index in (2,3):
        return 5
    return  13

def setwidthcontent(index):
    if index == 0:
        return 2
    if index in (1,2,3):
        return 4
    return  12
        
def create_list_title(root):
    framet_title = Frame(root);
    framet_title.pack(anchor=W)  # 创建表头的 frame
    for index in range(len(list_data)):
        Label(framet_title, text=list_data[index], width=setwidth(index)).pack(side=LEFT, anchor=W)


def delete_doctor(index):
        print index 
        db.detele_doctor(index) 
        GetValue();
class FrameApp(Tk):
        def show_data(self, couser, j):
            for one_doctor in couser:
                index =str(one_doctor[0]);
                button = Button(self.frame.interior,text='删除',command = lambda index=index:delete_doctor(index),width=setwidthcontent(0))  
#                 button.bind('Button'+click, lambda:delete_doctor(click))
                button.grid(row=j, column=0)
                for i in range(len(list_data)-1):
                    ent = Entry(self.frame.interior, width=setwidthcontent(i+1))
                    ent.grid(row=j, column=i+1)
                    ent.insert(0, one_doctor[i])
                
                j = j + 1
            couser.close()
        
        
        def rm_all_text(self):
            for child in self.frame.interior.winfo_children():
                child.destroy()
            
            
        def set_son(self, root):
            self.frame = VerticalScrolledFrame(root, height=500, width=400)
            self.frame.pack(anchor=W)
            couser = db.show_all_doctor()
            j = 0
            self.show_data(couser, j)

        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)
            db.create_db()
            self.title('医生搜索1.0')
            createTtitle(root, 1, 6)
            createTtitle(root, 6, 10)
            createTtitle(root, 10, len(list_data))
#             createTtitle(root, 13, len(list_data))
            create_list_title(root)
            self.set_son(root)
                


    
app = FrameApp()
app.minsize(800, 500)
app.mainloop()


