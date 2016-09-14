# -*- coding: utf-8 -*- 
import xlwt

def write_xls(couser,path):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(u'医生详情')
    j = 0
    for one_doctor in couser:
                for i in range(9):
                    sheet.write(j, i, one_doctor[i])
                
                j = j + 1
    couser.close()  
    workbook.save(path+'.xls')
    
