import socket


def send(connection, status_line, headers):
	encoding = "UTF-8"
	lines = [status_line] + headers + [""]
	connection.send("\r\n".join(lines).encode(encoding))


def is_prime(n):
	if n < 2:
		return False
	if n == 2:
		return True
	if n % 2 == 0:
		return False
	i = 3;
	while i * i <= n:
		if n % i == 0:
			return False
		i += 2;
	return True


def send_chunk(text, connection):
		lines = ["", str(len(text)), text]
		try:
			connection.send("\r\n".join(lines).encode(encoding))
		except ConnectionResetError:
			return False
		return True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('localhost', 8080))
s.listen(1)

status_line = "HTTP/1.1 200 OK"

headers = [
	"Content-Type: text/plain",
	"Transfer-Encoding: chunked",
];

while 1:
	running = True
	encoding = "UTF-8"
	connection, address = s.accept();
	send(connection, status_line, headers)
	text = send_chunk("2\n", connection)
	i = 3;
	while running:
		if is_prime(i):
			running = send_chunk(str(i) + "\n", connection)
		i += 2
