import socket

def sendWithSize(message, conn):
    message = message.encode()
    length = str(len(message)).zfill(8)
    conn.sendall(length.encode() + message)

def recvWithSize(conn):
    length_data = conn.recv(8)
    if not length_data:
        return None
    try:
        length = int(length_data.decode().strip())
    except ValueError:
        return None
    message = b""
    while len(message) < length:
        chunk = conn.recv(length - len(message))
        if not chunk:
            return None
        message += chunk
    return message.decode()
