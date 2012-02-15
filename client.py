import sys, threading, xmlrpclib

results = []
expression = sys.argv[1]

def work(server, expression):
  s = xmlrpclib.ServerProxy(server)
  result = s.tbgs(expression)
  results.append(result)

threads = []

for x in ('http://neel.mit.edu:8000/RPC2',
    'http://dtdstudyroom-1.mit.edu:8000/RPC2',
    'http://tvroom.mit.edu:8000/RPC2',
    'http://dbenhaim.mit.edu:8000/RPC2'):
#for x in ('http://neel.mit.edu:8000/RPC2',):
  t = threading.Thread(target=work, args=(x, expression))
  threads.append(t)
  t.start()

for t in threads:
  t.join()

for result in results:
  for r in result:
    print r[0], ":\t\t", r[1]
