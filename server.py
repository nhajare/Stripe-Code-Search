import re, SimpleXMLRPCServer, subprocess, sys, threading

num_threads = 4
files_list = [[] for x in range(num_threads)]

file_names = open('files').readlines()
for x in range(len(file_names)):
  try:
    line = file_names[x].strip()
    f = open(line)
    contents = f.read()
    f.close()
    files_list[x % num_threads].append((line, contents))
  except IOError:
    pass

def tbgs(expression):
  matches = []
  regex = re.compile(expression)

  def work(files):
    for f in files:
      name, contents = f
      match = regex.search(contents)
      if match:
        matches.append((name, match.group(0)))
        if len(matches) > 1000:
          break

  threads = []
  for x in range(num_threads):
    args = (files_list[x],)
    t = threading.Thread(target=work, args=args)
    t.start()
    threads.append(t)

  for t in threads:
    t.join()

  return matches

class RequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
  rpc_paths = ('/RPC2',)

hostname = subprocess.check_output(['hostname']).strip()
server = SimpleXMLRPCServer.SimpleXMLRPCServer((hostname, 8000),
    requestHandler=RequestHandler)
server.register_function(tbgs)
print 'Starting server...'
server.serve_forever()
