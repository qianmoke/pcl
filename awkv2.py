#custome awk.py module

class controller:
  
  def __init__(self,f1,f2):
    self.m_file_data = file(f1)
    self.m_file_request = file(f2)
    self.m_handlers =[]
    self.m_time="2015-10-29"

  def subscribe(self,o):
    self.m_handlers.append(o)
  
  def run(self):
    for o in self.m_handlers:
      o.begin()
      o.prepare_time(self.m_time)
      
    s1=self.m_file_request.readline()
    while s1 !="":
      for o in self.m_handlers:
        o.request_actname(s1)
      s1=self.m_file_request.readline()

    
    s2=self.m_file_data.readline()
    while s2 !="":
      for o in self.m_handlers:
        o.process_lines(s2)
      s2=self.m_file_data.readline()

    for o in self.m_handlers:
      o.cal_time()

    for o in self.m_handlers:
      o.output()

    for o in self.m_handlers:
      o.end()

  def print_results(self):
    print
    print "Results:"
    print
    for o in self.m_handlers:
      print '----------------------------------'
      print o.description()
      print '----------------------------------'
      print o.result()
