import socket
import threading
import os
import wave
import time
import datetime
from tkinter import Tk, scrolledtext, Button, Entry, messagebox
from tkinter import filedialog as fd

# Server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 5117

# GUI window for the client
client_window = Tk()
client_window.title("Client")

# Text box to display received text messages
text_box = scrolledtext.ScrolledText(client_window, width=40, height=10)
text_box.pack()


# Function to establish connection with the server
def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SERVER_ADDRESS, SERVER_PORT)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))
    print(
        f"[{get_timestamp()}] Connection between client {sock.getsockname()} and server {server_address} is established")
    text_box.insert('end', f"[{get_timestamp()}] Connected to server {server_address}\n")

    # Handle server response in a separate thread
    response_thread = threading.Thread(target=handle_server_response, args=(sock,))
    response_thread.start()


# Function to handle server responses
def handle_server_response(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        text_message = data.decode()
        print(f"[{get_timestamp()}] Received text message from server: {text_message}")
        text_box.insert('end', f"[{get_timestamp()}] {text_message}\n")


# Function to send text messages to the server
def send_text_message(sock, message):
    sock.sendall(message.encode())


# Button to send text messages
def send_message():
    message = input_box.get()
    send_text_message(client_sock, message)
    input_box.delete(0, 'end')


# Button to browse and send audio recordings
def browse_and_send_audio():
    file_path = fd.askopenfilename(initialdir="/", title="Select a WAV File",
                                   filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*")))
    if file_path:
        send_audio_recording(file_path)


# Function to send audio recording to the server
def send_audio_recording(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    client_sock.sendall(data)


# Button to browse and send text files
def browse_and_send_text_file():
    file_path = fd.askopenfilename(initialdir="/", title="Select a Text File",
                                   filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if file_path:
        send_text_file(file_path)


# Function to send text file to the server
def send_text_file(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    client_sock.sendall(data)


# Button to browse and play canned audio recordings
def browse_and_play_canned_audio():
    file_path = fd.askopenfilename(initialdir="/CannedRecordings", title="Select a WAV File",
                                   filetypes=(("WAV Files", "*.wav"), ("All Files", "*.*")))
    if file_path:
        play_canned_audio(file_path)


# Function to play canned audio recordings locally
def play_canned_audio(file_path):
    os.system(file_path)


# Function to get timestamp in the specified format
def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S_%d%b%y")


# Connect to the server
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_to_server()

# GUI input box for sending messages
input_box = Entry(client_window, width=40)
input_box.pack()

# GUI button to send messages
button_send = Button(client_window, text="Send", command=send_message)
button_send.pack()

# GUI button to browse and send audio recordings
button_browse_audio = Button(client_window, text="Send Audio Recording", command=browse_and_send_audio)
button_browse_audio.pack()

# GUI button to browse and send text files
button_browse_text = Button(client_window, text="Send Text File", command=browse_and_send_text_file)
button_browse_text.pack()

# GUI button to browse and play canned audio recordings
button_play_canned_audio = Button(client_window, text="Play Canned Audio",
                                  command=browse_and_play_canned_audio)
button_play_canned_audio.pack()

# Run the client GUI window
client_window.mainloop()
