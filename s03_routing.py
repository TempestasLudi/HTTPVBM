import socket
import os


def send(connection, status_line, headers, body):
	encoding = "UTF-8"
	lines = [status_line] + headers + ["", body]
	connection.send("\r\n".join(lines).encode(encoding))


def read_up_to(connection, delimiter):
	read_data = "";
	while True:
		character = connection.recv(1).decode("UTF-8")
		if character == delimiter:
			return read_data
		read_data += character


def read_request_line(connection):
	return read_up_to(connection, " "), read_up_to(connection, " "), read_up_to(connection, "\r")

def read_file(path, request_line):
	if os.path.isdir(path):
		path = os.path.join(path, "page.html")

	name, extension = os.path.splitext(path)

	try:
		mime_type = mime_types[extension]
	except KeyError:
		mime_type = None

	try:
		file_handler = open(path)
		body = file_handler.read()
		file_handler.close()
		return body, mime_type, status_line
	except FileNotFoundError:
		return "Page Not Found", "text/plain", "HTTP/1.1 404 Page Not Found"

mime_types = {
	".html": "text/html",
	".txt": "text/plain",
	".json": "text/json",
	".css": "text/css"
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 8080))
s.listen(1)

while 1:
	connection, address = s.accept();

	headers = []
	mime_type = None
	status_line = "HTTP/1.1 200 OK"

	method, uri, protocol = read_request_line(connection)

	path = os.path.join("s03_routing", uri[1:])

	body, mime_type, status_line = read_file(path, status_line)

	headers.append("Content-Length: " + str(len(body)))
	if mime_type is not None:
		headers.append("Content-Type: " + mime_type)

	send(connection, status_line, headers, body)
	connection.close();
