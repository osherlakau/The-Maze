import socket
import keyboard
import json

IP = '127.0.0.1'
port = 5000

# Build socket between server and client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, port))

def send_command(command):
    message = json.dumps({"command": command}) + "\n"
    client_socket.send(message.encode())

# All 6 functions send message
def on_right(event):
    send_command("R")

def on_down(event):
    send_command("D")

def on_left(event):
    send_command("L")

def on_up(event):
    send_command("U")

def exit(event):
    send_command("esc")

def reset(event):
    send_command("enter")

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
