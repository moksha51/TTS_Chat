import socket
import threading
import os
import wave
import time
import datetime
from tkinter import Tk, scrolledtext, Button, Entry, messagebox
from tkinter import filedialog as fd
import pyaudio
import pygame
import numpy as np
import socket
import threading
import datetime
import os

# Server address and port
SEAHAWK_ADDRESS = '192.168.0.92'
SERVER_PORT = 40000

# GUI window for the client
client_window = Tk()
client_window.title("Client")

# Text box to display received text messages
text_box = scrolledtext.ScrolledText(client_window, width=80, height=40)
text_box.pack()

########################### AUDIO VARIABLES############################
# Create a PyAudio object
audio = pyaudio.PyAudio()

# PyAudio configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Create
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Audio recording variables
is_recording = False
frames = []


##########################################################################

# Function to establish connection with the server
def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SEAHAWK_ADDRESS, SERVER_PORT)
    sock.connect(server_address)
    print(
        f"[{get_timestamp()}] Connection between client {sock.getsockname()} and server {server_address} is established")
    text_box.insert('end', f"[{get_timestamp()}] Connected to server {server_address}\n")

    # Handle server response in a separate thread
    response_thread = threading.Thread(target=handle_server_response, args=(sock,))
    response_thread.start()


# Function to handle server responses
def handle_server_response(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                continue
            text_message = data.decode()
            print(f"[{get_timestamp()}] Received text message from server: {text_message}")
            text_box.insert('end', f" Base: [{get_timestamp()}] {text_message}\n")
        except Exception as e:
            print(e)
            break

# Function to send text messages to the server
def send_text_message(sock, message):
    try:
        sock.sendall(message.encode())
        text_box.insert('end', f" Base: [{get_timestamp()}] {message}\n")
    except ConnectionAbortedError:
        messagebox.showerror("Error", "The connection was aborted by the server.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Button to send text messages
def send_message():
    message = input_box.get()
    send_text_message(client_sock, message)
    input_box.delete(0, 'end')


def siren_send():
    message = 'siren.wav'
    send_text_message(client_sock, message)
    input_box.delete(0, 'end')


def canned_audio_send():
    message = 'hello.wav'
    send_text_message(client_sock, message)
    input_box.delete(0, 'end')


def audio_send(frames, audio):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (SEAHAWK_ADDRESS, SERVER_PORT)
    sock.connect(server_address)
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    while push_to_talk_press().is_set():
        try:
            data = stream.read(CHUNK)
            sock.sendall(data)
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sock.close()

    while True:
        if len(frames) > 0:
            data = frames.pop(0)
            client_sock.sendall(data)
            send_thread = threading.Thread(target=audio_send(frames, audio), args=(sock,))
            send_thread.start()


# Function to start recording audio
def audio_record_start(frames, audio):
    print("Recording started...")
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    data = stream.read(CHUNK)
    frames.append(data)


# Function to stop recording audio
def audio_record_stop(audio):
    # Create a Stream object
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Recording stopped...")
    stream.stop_stream()
    stream.close()


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


def push_to_talk_press():
    threading.Thread(target=audio_record_start(frames, audio)).start()
    print('ptt button works')


def push_to_talk_release():
    threading.Thread(target=audio_record_stop).start()
    threading.Thread(target=audio_send(frames, audio)).start()


# Establish connection with the server
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((SEAHAWK_ADDRESS, SERVER_PORT))

# GUI input box for sending messages
input_box = Entry(client_window, width=80)
input_box.pack()

# GUI button_push_to_talk to send messages
button_send = Button(client_window, text="Send", command=lambda: send_text_message(client_sock, input_box.get()))
button_send.pack()

# GUI button_push_to_talk for push-to-talk
button_push_to_talk = Button(client_window, text="Push to Talk", width=10, height=10)
button_push_to_talk.pack()

# Bind button_push_to_talk events
button_push_to_talk.bind("<ButtonPress>", lambda event: push_to_talk_press())
button_push_to_talk.bind("<ButtonRelease>", lambda event: push_to_talk_release())

# GUI button_push_to_talk to browse and send audio recordings
button_browse_audio = Button(client_window, text="Send Audio Recording", command=browse_and_send_audio)
button_browse_audio.pack()

# GUI button_push_to_talk to browse and send text files
button_browse_text = Button(client_window, text="Send Text File", command=browse_and_send_text_file)
button_browse_text.pack()

# GUI button_push_to_talk to send canned siren
button_siren_send = Button(client_window, text="Siren",
                           command=siren_send())
button_siren_send.pack()

# GUI button_push_to_talk to send canned audio
button_canned_audio_send = Button(client_window, text="Canned Audio",
                                  command=canned_audio_send())
button_canned_audio_send.pack()

connect_to_server()

# Run the client GUI window
# client_window.mainloop()

# Run client on contineous loop
while True:
    client_window.update()
