import socket
import threading
import ssl
import protocol

class Server:
    def __init__(self):
        self.ADDR = ("192.168.1.246", 8080)
        self.clients = []
        self.lock = threading.Lock()
        self.message_history = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.ADDR)
        self.s.listen()
        print(f"Server is running on {self.ADDR}...")

        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    def sendMessage(self, sender_conn, username, message):
        final_message = f"{username}: {message}"
        self.message_history.append(final_message)
        if len(self.message_history) > 50:
            self.message_history.pop(0)
        with self.lock:
            for conn, conn_username in self.clients:
                if conn != sender_conn:
                    protocol.sendWithSize(final_message, conn)

    def recvMessage(self, conn):
        try:
            message = protocol.recvWithSize(conn)
            if message:
                username = self.getClientUsername(conn)
                print(f"Received: {message} from {username}")
                self.sendMessage(conn, username, message)
        except:
            self.removeClient(conn)

    def handle_client(self, conn):
        protocol.sendWithSize("Enter your username:", conn)
        username = protocol.recvWithSize(conn)
        with self.lock:
            self.clients.append((conn, username))
        for msg in self.message_history:
            protocol.sendWithSize(msg, conn)
        try:
            while True:
                self.recvMessage(conn)
        except:
            pass
        finally:
            self.removeClient(conn)

    def removeClient(self, conn):
        with self.lock:
            self.clients = [(c, u) for c, u in self.clients if c != conn]
        conn.close()

    def getClientUsername(self, conn):
        for c, u in self.clients:
            if c == conn:
                return u
        return "Unknown"

    def main(self):
        while True:
            conn, addr = self.s.accept()
            print(f"New connection from {addr}")
            conn = self.context.wrap_socket(conn, server_side=True)
            print(f"SSL connection established with {addr}")
            threading.Thread(target=self.handle_client, args=(conn,)).start()

if __name__ == "__main__":
    server = Server()
    server.main()
