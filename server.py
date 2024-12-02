import socket
import threading
import pickle  # For serializing game state

HOST = '149.160.72.92'  # Localhost for testing
PORT = 5555

game_state = {
    "players": [{"x": 1, "y": 1, "direction": "RIGHT"}, {"x": 2, "y": 1, "direction": "RIGHT"}],
    "ghosts": [{"x": 9, "y": 9}, {"x": 10, "y": 10}],
    "board": [ ... ]  # Your game board
}

clients = []

def handle_client(conn, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            # Process input and update game state
            inputs = pickle.loads(data)
            # Update player position
            player_id = inputs['player_id']
            game_state['players'][player_id]['direction'] = inputs['direction']
            
            # Serialize and send updated game state to clients
            state_data = pickle.dumps(game_state)
            for client in clients:
                client.send(state_data)
        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break

    conn.close()
    clients.remove(conn)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)  # Allow 2 players
print("Server is running...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr)).start()
