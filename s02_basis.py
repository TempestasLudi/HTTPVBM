import socket


def send(connection, status_line, headers, body):
	encoding = "UTF-8"
	lines = [status_line] + headers + ["", body]
	connection.send("\r\n".join(lines).encode(encoding))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 8080))
s.listen(1)

status_line = "HTTP/1.1 200 OK"
body = '{"message": "Hello, World!"}';

headers = [
	"Content-Length: " + str(len(body)),
	"Content-Type: text/json",
];

while 1:
	connection, address = s.accept();
	send(connection, status_line, headers, body)
	connection.close();

# Probeer eens wat er gebeurt als je "text/json" in de Content-Type header in "text/plain" of "application/octet-stream" verandert
# Kijk eens wat er gebeurt als je "200 OK" in de status_line aanpast naar bijvoorbeeld "418 I'm a teapot"
