import socket
import threading
import re


def validate_key(key):
    if len(key) != 80:
        print("Invalid key format: Should be exactly 80 characters long.")
        return False
    parts = [key[i:i+8] for i in range(0, 80, 8)]
    part1 = parts[0]
    if not re.match(r"^[A-Za-z0-9]{8}$", part1) or sum(c.isupper() for c in part1) < 2 or sum(c.islower() for c in part1) < 2:
        print("Part 1 failed:", part1)
        return False
    part2 = parts[1]
    if not re.match(r"^[A-Za-z0-9]{8}$", part2) or sum(c.isdigit() for c in part2) < 2 or sum(ord(c) for c in part2) % 7 != 0:
        print("Part 2 failed:", part2)
        return False
    part3 = parts[2]
    if not re.match(r"^[A-Za-z0-9@#!$]{8}$", part3) or sum(c in "@#!$" for c in part3) < 2:
        print("Part 3 failed:", part3)
        return False
    part4 = parts[3]
    if not re.match(r"^[a-z]{8}$", part4) or part4[0] != part4[-1]:
        print("Part 4 failed:", part4)
        return False
    part5 = parts[4]
    if not re.match(r"^[A-Za-z0-9]{8}$", part5) or int(''.join(filter(str.isdigit, part5)) or "0") % 5 != 0:
        print("Part 5 failed:", part5)
        return False
    part6 = parts[5]
    if not re.match(r"^[A-Za-z0-9]{8}$", part6) or sum(c.isupper() for c in part6) < 3:
        print("Part 6 failed:", part6)
        return False
    part7 = parts[6]
    if not re.match(r"^[a-z@#!$]{8}$", part7) or sum(c in "@#!$" for c in part7) != 1:
        print("Part 7 failed:", part7)
        return False
    part8 = parts[7]
    if not re.match(r"^[a-z0-9]{8}$", part8):
        print("Part 8 failed:", part8)
        return False
    part9 = parts[8]
    if not re.match(r"^[A-Z]{8}$", part9) or sum(ord(c) for c in part9) % 3 != 0:
        print("Part 9 failed:", part9)
        return False
    part10 = parts[9]
    if not re.match(r"^\d{8}$", part10) or sum(int(c) for c in part10) != 30:
        print("Part 10 failed:", part10)
        return False
    return True

connected_clients = []

def handle_client(client_socket, addr):
    try:
        # Receive the password from the client
        password = client_socket.recv(1024).decode('utf-8')

        # Check if the password matches
        if validate_key(password) == True:

            client_socket.send(b"AUTH_SUCCESS")
            print(f"Client {addr} authenticated successfully.")
            connected_clients.append((client_socket, addr))

            # Proceed with normal communication






        else:
            client_socket.send(b"AUTH_FAIL")
            print(f"Client {addr} failed authentication.")
            client_socket.close()
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
        client_socket.close()
    finally:
        if (client_socket, addr) in connected_clients:
            connected_clients.remove((client_socket, addr))
def start_server():
    server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('::', 40723))  # Bind to all available IPv6 interfaces on port 40724
    server.listen(5)
    print("Server listening on port 40723 (IPv6)...")

    # Accept clients in a separate thread
    def accept_clients():
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_handler.start()

    threading.Thread(target=accept_clients, daemon=True).start()

    # Command input loop to send commands to authenticated clients
    while True:
        if connected_clients:
            print("\nConnected clients:")
            for i, (client_socket, addr) in enumerate(connected_clients):
                print(f"{i}: {addr}")
            try:
                client_index = int(input("\nEnter the client number to send a command to: "))
                command = input("Enter command to send (e.g., /send_picture): ")
                client_socket, addr = connected_clients[client_index]
                client_socket.send(command.encode('utf-8'))  # Send command to client
            except (ValueError, IndexError):
                print("Invalid client number. Please try again.")
        else:
            print("No clients connected.")

if __name__ == "__main__":
    start_server()
