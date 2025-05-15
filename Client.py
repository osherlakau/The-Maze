import socket
import keyboard

IP = '127.0.0.1'
port = 5000

# Build socket between server and client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, port))

# All 6 functions send message
def on_right(event):
    client_socket.send("R".encode())

def on_down(event):
    client_socket.send("D".encode())

def on_left(event):
    client_socket.send("L".encode())

def on_up(event):
    client_socket.send("U".encode())

def exit(event):
    client_socket.send("esc".encode())

def reset(event):
    client_socket.send("enter".encode())

# Read key and send (arrows)
keyboard.on_press_key("right", on_right)
keyboard.on_press_key("down", on_down)
keyboard.on_press_key("left", on_left)
keyboard.on_press_key("up", on_up)

# Read key and send (chars)
keyboard.on_press_key("d", on_right)
keyboard.on_press_key("s", on_down)
keyboard.on_press_key("a", on_left)
keyboard.on_press_key("w", on_up)

# Read key and send (exit)
keyboard.on_press_key("esc", exit)

# Read key and send (reset)
keyboard.on_press_key("enter", reset)

# Wait for key press (esc)
keyboard.wait("esc")
