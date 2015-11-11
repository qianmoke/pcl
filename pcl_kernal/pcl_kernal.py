#!/usr/bin/env python
import sys
import re
import datetime
import xlwt
import xlrd

num_col=0
start_time_col=5
stop_time_col=6
time_col=7

yesterday_result_f={}
today_result_f={}
sequence=[]
sequence_final=[]
today = xlrd.open_workbook('2015-11-06.xlsx')
yesterday = xlrd.open_workbook('2015-10-09.xlsx')
def choose_f(workbook,dic_time,time_sequence):
  for sheet in workbook.sheets():
    for row in xrange(sheet.nrows):
      if row != 0:
        start_time=sheet.cell(row,start_time_col).value
        stop_time=sheet.cell(row,stop_time_col).value
        time=sheet.cell(row,time_col).value
        if dic_time.has_key(start_time):
          if time >= dic_time[start_time][0]:
           dic_time[start_time][0]=time
        else:
          dic_time[start_time]=[]
          dic_time[start_time].append(time)
          time_sequence.append(start_time)
  return dic_time,time_sequence
      
def output_to_xls(dic_time,time_sequence,file_name):       
  output = xlwt.Workbook(encoding='utf-8')
  output_sheet = output.add_sheet('Sheet 1')
  i=0
  for time in time_sequence:
    output_sheet.write(i,0,time)
    out=len(dic_time[time])-1
    output_sheet.write(i,1,dic_time[time][out])
    i +=1
  output.save(file_name)

choose_f(today,yesterday_result_f,sequence)
output_to_xls(yesterday_result_f,sequence,'l1.xls')
i=0
for now in sequence:
  if i>0:
    time_now=datetime.datetime.strptime(now,"%H:%M:%S")
    time_fre=datetime.datetime.strptime(sequence_final[i-1],"%H:%M:%S")
    delta=(time_now-time_fre).seconds
    period=delta + yesterday_result_f[now][0]
    #print now,sequence_final[i-1],delta,yesterday_result_f[now][0],period
    if period >= yesterday_result_f[sequence_final[i-1]][0]:
      sequence_final.append(now)
      i +=1
  else:
    sequence_final.append(now)
    i +=1
output_to_xls(yesterday_result_f,sequence_final,'l2.xls')
