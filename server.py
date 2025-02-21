import socket
import threading
import time

class ChatServer:
    def __init__(self):
        self.clients = []
        self.CHAT_IP = "127.0.0.1"
        self.CHAT_PORT = 5555
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.CHAT_IP, self.CHAT_PORT))
        server.listen(5)  # Allows multiple connections

        print("Server listening on port 5555")

        while True:
            client_socket, addr = server.accept()
            self.clients.append(client_socket)
            print(f"New connection from {addr}")
            thread = threading.Thread(target=self.handle_clients, args=(client_socket, addr))
            thread.start()

    def handle_clients(self, client_socket, address):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"{address[1]}: {data.decode()}")

                self.broadcast(data, client_socket,address)

            except Exception as e:
                print(f"Error: {e}")
                break

        print(f"Connection closed: {address}")
        client_socket.close()
        self.clients.remove(client_socket)

    def broadcast(self, message, sender_socket,address):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(f"{address[1]}: {message.decode()}".encode())
                except:
                    client.close()
                    self.clients.remove(client)


# Start the server
if __name__ == "__main__":
    ChatServer()
