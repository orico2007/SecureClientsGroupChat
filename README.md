# SecureClientsGroupChat

SecureClientsGroupChat is a multi-client group chat application that utilizes SSL encryption to ensure secure communication between users. The project consists of a server and multiple clients, with a GUI-based client implementation.

## Features

- **SSL Encryption**: Secure communication using TLS/SSL.
- **Multi-client Support**: Allows multiple clients to connect and chat.
- **Message History**: Stores the last 50 messages for new clients.
- **GUI Client**: A Tkinter-based graphical interface for user interaction.
- **Night Mode**: Toggleable dark mode for better readability.

## Installation

### Prerequisites
- Python 3.x
- `tkinter` (built-in with Python)
- `openssl` for generating SSL certificates

### Generating SSL Certificates
Run the following commands to generate a self-signed SSL certificate:
```sh
openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -days 365 -nodes
```

### Cloning the Repository
```sh
git clone https://github.com/yourusername/SecureClientsGroupChat.git
cd SecureClientsGroupChat
```

## Running the Server
Start the server using:
```sh
python server.py
```
The server will run on `192.168.1.246:8080` (modify as needed).

## Running the Client
Start the client GUI using:
```sh
python client.py
```
Enter a username when prompted and start chatting securely!

## Protocol
The communication follows a custom protocol using prefixed message lengths for structured data transmission. The `protocol.py` file handles sending and receiving messages efficiently.

## Security Considerations
- Uses SSL to encrypt messages in transit.
- Requires a valid server certificate for client authentication.
- Implements message length validation to prevent buffer overflow attacks.

## Future Enhancements
- User authentication with login/logout.
- Encrypted message storage.
- Support for file sharing.

## Contributors
- Ori Cohen

Feel free to contribute by submitting pull requests!

