# -*- coding: utf-8 -*- 
import  xdrlib , sys
import xlrd
import db
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)
# 根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file, colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
#     print ncols
    colnames = table.row_values(colnameindex)  # 某一行数据 
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row and len(colnames)>8:
            app =''
            for i in range(len(colnames)):
              
                if i==3:
                    app = app+'__'+str(int(row[i]));
                else:
                    app =app+'__'+row[i];
                
            db.insert_doctor_by_info(app[2:])

# excel_table_byindex()


