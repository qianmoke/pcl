#!/usr/bin/env python
#coding=gbk
import sys
import awkv2
import re
import datetime
import xlwt
import xlrd
data='server.log'
request='data.txt'

#the time collect of pcl in server.log
class collect_pcltime:
  def __init__(self):
    self.m_actnames_start={}
    self.m_actnames_stop={}
    self.m_actnames_final={}
    self.m_request_actname=[]
    self.m_time_period1=['17:','18:','19:','20:','21:','22:','23:']
    self.m_time_period2=['00:','01:','02:','03:','04:']
    self.m_time_prepare=[]
  def begin(self):
    pass
  def prepare_time(self,day):
    now=str(datetime.datetime.strptime(day,"%Y-%m-%d"))
    tomorrow=str(datetime.datetime.strptime(day,"%Y-%m-%d")+datetime.timedelta(days=1))
    now_array=now.split()
    now_final=now_array[0]+" "
    tomorrow_array=tomorrow.split()
    tomorrow_final=tomorrow_array[0]+" "
    for period in self.m_time_period1:
      prepare_time=now_final + period
      self.m_time_prepare.append(prepare_time)
    for period in self.m_time_period2:
      prepare_time=tomorrow_final + period
      self.m_time_prepare.append(prepare_time)
  def request_actname(self,line):
    array=line.split()
    actname=array[0]
    self.m_request_actname.append(actname)
  def process_lines(self,line):
    try:
      for time in self.m_time_prepare: 
        if re.search(time ,line):
          for actname in self.m_request_actname:
            search="actname="+actname
            if re.search(search,line):
              if re.search("create",line):
                array=line.split()
                actname=array[7][9:]
                time=array[1][0:8]
                if self.m_actnames_start.has_key(actname):
                  if time not in self.m_actnames_start[actname]:
                    self.m_actnames_start[actname].append(time);
                else:
                  self.m_actnames_start[actname]=[];
                  self.m_actnames_start[actname].append(time);
              if re.search("update",line):
                array_stop=line.split()
                actname=array_stop[9][8:]
                time=array_stop[1][0:8]
                if self.m_actnames_stop.has_key(actname):
                  if time not in self.m_actnames_stop[actname]:
                    self.m_actnames_stop[actname].append(time);
                else:
                  self.m_actnames_stop[actname]=[];
                  self.m_actnames_stop[actname].append(time);
            
    except AttributeError:
      pass
    except IndexError:
      pass
  def cal_time(self):
    for actname in self.m_request_actname: 
      if self.m_actnames_start.has_key(actname):
        if self.m_actnames_stop.has_key(actname):
          time_start=self.m_actnames_start[actname]
          time_stop=self.m_actnames_stop[actname]
          
          if self.m_actnames_final.has_key(actname):
            if time_start not in self.m_actnames_final[actname]:
              self.m_actnames_final[actnaame].append(time_start);
            if time_stop not in self.m_actnames_final[actname]:
              self.m_actnames_final[actnaame].append(time_stop);
          else:
            self.m_actnames_final[actname]=[]
            self.m_actnames_final[actname].append(time_start);
            self.m_actnames_final[actname].append(time_stop);
            
          length=len(time_start)
          i=0
          while i<length:
            time1=datetime.datetime.strptime(time_start[i],"%H:%M:%S")
            time2=datetime.datetime.strptime(time_stop[i],"%H:%M:%S")
            time_final=str((time2-time1).seconds)
            self.m_actnames_final[actname].append(time_final);
            i +=1

  def end(self):
    pass
  def description(self):
    return "Collection Data of PCL Time"
  def result(self):
    s=""
    for actname in self.m_request_actname:
      if self.m_actnames_final.has_key(actname):
        time=str(self.m_actnames_final[actname])
      else:
        time=""
      s += actname
      s += " "
      s += time
      s += "\n"
    return s
  def output(self):
    workbook = xlwt.Workbook(encoding='gbk')
    sheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
    i=3
    for actname in self.m_request_actname:
      if self.m_actnames_final.has_key(actname):
        time=self.m_actnames_final[actname][2]
      else:
        time="error"
      sheet.write(i,0,actname)
      sheet.write(i,1,time)
      i +=1
    workbook.save('pcl.xlsx')

ar = awkv2.controller(data,request)
ar.subscribe(collect_pcltime())
ar.run()
ar.print_results()
