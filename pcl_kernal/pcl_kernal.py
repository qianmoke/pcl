#!/usr/bin/env python
import sys
import re
import datetime
import xlwt
import xlrd

pcl_col=0
actname_id_col=2
actname_col=3
time_col=6
actname_id_sequence=[]
dic_time={}
dic_name={}
dic_pcl={}
workbook = xlrd.open_workbook('pcl_kernal.xlsx')
for sheet in workbook.sheets():
  if sheet.name == "2015-10-09":
    for row in xrange(sheet.nrows):
      if row != 0:
        actname_id=sheet.cell(row,actname_id_col).value
        time=sheet.cell(row,time_col).value
        actname=sheet.cell(row,actname_col).value
        pcl=sheet.cell(row,pcl_col).value
        if dic_time.has_key(actname_id):
         if time >= dic_time[actname_id]:
           dic_time[actname_id].append(time)
        else:
          dic_time[actname_id]=[]
          dic_time[actname_id].append(time)

        if actname_id not in dic_name.keys():
          dic_name[actname_id]=[]
          dic_name[actname_id].append(actname)

        if actname_id not in dic_pcl.keys():
          dic_pcl[actname_id]=[]
          dic_pcl[actname_id].append(pcl)
        
        if actname_id not in actname_id_sequence:
          actname_id_sequence.append(actname_id)

workbook = xlwt.Workbook(encoding='utf-8')
sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
i=0
for actname_id in actname_id_sequence:
    time=dic_time[actname_id][0]
    pcl=dic_pcl[actname_id][0]
    actname=dic_name[actname_id][0]
    sheet.write(i,0,pcl)
    sheet.write(i,1,actname_id)
    sheet.write(i,2,actname)
    sheet.write(i,3,time)
    i +=1
workbook.save('pcl_kernal_process.xlsx')

