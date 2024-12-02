import socket
import pygame
import pickle

HOST = '149.160.72.92'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

player_id = None  # Assigned by server upon connection

# Receive initial player ID
data = client.recv(1024)
player_id = int(data.decode())

def send_input(direction):
    inputs = {"player_id": player_id, "direction": direction}
    client.send(pickle.dumps(inputs))

# Game loop to send inputs and render game state
