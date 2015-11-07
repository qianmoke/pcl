#coding=gbk
import xlrd
table=xlrd.open_workbook('2015_10.xlsx')
print "There are {} sheets in the workbook".format(table.nsheets)
for booksheet in table.sheets():
  a=booksheet.nrows
  b=booksheet.ncols
  print a,b
