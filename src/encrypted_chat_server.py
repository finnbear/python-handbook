# +---------+
# | Imports |
# +---------+
import sys
import ujson
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import traceback
#import SimpleHTTPServer
#import SocketServer

# +-----------+
# | Constants |
# +-----------+

server_port = 4001
server_path = "/chat/"

# +-----------+
# | Variables |
# +-----------+

data = []

# +--------+
# | main() |
# +--------+

def main():
	serveHTTP()

# +---------+
# | Classes |
# +---------+

class Handler(BaseHTTPRequestHandler):
	# For GET requests
	def do_GET(self):
		if server_path in self.path:
			# Set up response
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()

			# Write response
			self.wfile.write(ujson.dumps(data))
		return
	
	# For POST requests
	def do_POST(self):
		if server_path in self.path:
			# Get form data
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':'application/x-www-form-urlencoded'}
			)
			print form
			try:
				# Extract form data
				json = form["json"]		
				print(json)		
				#message = ujson.loads(json)
				data.append(json.value)

				# Set up response
				self.send_response(200)
				self.send_header('Content-type','text/json')
				self.end_headers()

				# Write response
				self.wfile.write("200")
			except Exception, error:
				traceback.print_exc()			
				# Set up response
				self.send_response(400)
				self.send_header('Content-type','text/json')
				self.end_headers()

				# Write response
				self.wfile.write("400")
		return

# +-----------+
# | Functions |
# +-----------+

def serveHTTP():
	try:
		# Create a socket server at the correct port
		httpd = HTTPServer(("", server_port), Handler)

		# Begin to serve
		print "HTTP server started at port", server_port
		httpd.serve_forever()
	except KeyboardInterrupt:
		httpd.socket.close()

# +---------+
# | Program |
# +---------+

main()
