import socket
import threading
import datetime
import os
import wave
import time
import pygame
# import speech_recognition as sr
# from gtts import gTTS
from tkinter import Tk, scrolledtext, Button, messagebox, Entry
from tkinter import filedialog as fd

# Server address and port
SEAHAWK_IP_ADDRESS = '192.168.0.92'
SERVER_PORT = 40000

# GUI window for the server
server_window = Tk()
server_window.title("Server")

# Audio File Directories
cannedrecordings = r'C:\Users\gray\Documents\XJ\Projects\Comms\ZyCraft_Audio\CannedRecordings'
receiveaudiorecordings = r'C:\Users\gray\Documents\XJ\Projects\Comms\ZyCraft_Audio\ReceivedAudioRecordings'


# Text box to display received text messages
text_box = scrolledtext.ScrolledText(server_window, width=80, height=30)
text_box.pack()


# Function to establish connection with client
def start_server():
    try:
        threading.Thread(target=handle_text_thread, daemon=True).start()

    except socket.error as e:
        print(f"Error: {e}")
        exit(1)


def handle_text_thread():
    server_address = (SEAHAWK_IP_ADDRESS, SERVER_PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f'[{datetime.datetime.now()}] Server started. Listening for connections...')
    text_box.insert('end', f"[{get_timestamp()}] Connected to Client {server_address}\n")

    while True:
        client_sock, client_address = server_socket.accept()
        print(f'Client is connected{client_address}')
        threading.Thread(target=handle_client, args=(client_sock, client_address), daemon=True).start()


def handle_push_to_talk_thread():
    server_address = (SEAHAWK_IP_ADDRESS, SERVER_PORT)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)

    while True:
        client_sock, client_address = server_socket.accept()
        text_box.insert('end', f'Ready to Receive Audio \n')
        threading.Thread(target=handle_client, args=(client_sock, client_address), daemon=True).start()


# Function to handle client requests
def handle_client(connection):
    while True:
        try:
            data = connection.recv(1024)
            if not data:
                continue
            # Received text message
            text_message = data.decode()
            text_box.insert('end', f" [{get_timestamp()}] {text_message}\n")
            # Delay before playing audio
            time.sleep(2)

            # if text_message.endswith("_recording.wav"):
            #     play_audio_recording()
            #
            # elif text_message.endswith("siren.wav"):
            #     play_siren()
            #
            # elif text_message.endswith("hello.wav"):
            #     play_canned_audio1()

        except Exception as e:
            print(e)
            break


# Function to save audio recording
def save_audio_recording(data):
    timestamp = datetime.datetime.now().strftime("%H%M%S_%d%m%Y")
    filename = f"ReceivedAudioRecordings/{timestamp}_voice_recording.wav"
    if not os.path.exists("ReceivedAudioRecordings"):
        os.makedirs("ReceivedAudioRecordings")

    with wave.open(filename, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(44100)
        file.writeframes(data)


# Function to send text message
def send_text_message(connection, message):
    try:
        connection.sendall(message.encode())
        text_box.insert('end', f" [{get_timestamp()}] {message}\n")
    except ConnectionAbortedError:
        messagebox.showerror("Error", "The connection was aborted by the server.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def send_message():
    message = input_box.get()
    send_text_message(client_sock, message)
    input_box.delete(0, 'end')

def play_siren():
    # Initialize Pygame
    pygame.init()
    # Load the media file
    media_file = r"C:\Users\gray\Documents\XJ\Projects\Comms\ZyCraft_Audio\CannedRecordings\siren.wav"
    pygame.mixer.music.load(media_file)

    # Play the media file
    pygame.mixer.music.play()

    # Wait for the media file to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up resources
    pygame.quit()

def play_audio_recording():
    # Initialize Pygame
    pygame.init()
    # Load the media file
    media_file = r"C:\Users\gray\Documents\XJ\Projects\Comms\ZyCraft_Audio\CannedRecordings\hello.wav"
    pygame.mixer.music.load(media_file)

    # Play the media file
    pygame.mixer.music.play()

    # Wait for the media file to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up resources
    pygame.quit()

def play_canned_audio1():
    # Initialize Pygame
    pygame.init()
    # Load the media file
    media_file = r"C:\Users\gray\Documents\XJ\Projects\Comms\ZyCraft_Audio\CannedRecordings\hello.wav"
    pygame.mixer.music.load(media_file)

    # Play the media file
    pygame.mixer.music.play()

    # Wait for the media file to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up resources
    pygame.quit()

# Function to transcribe audio using speech recognition
# def transcribe_audio():
#     recent_file = get_recent_audio_file()
#     if recent_file:
#         r = sr.Recognizer()
#         with sr.AudioFile(recent_file) as source:
#             audio = r.record(source)
#         try:
#             text = r.recognize_google(audio)
#             print(f"[{get_timestamp()}] Transcribed text: {text}")
#             with open("TranscribedText/transcribed_text.txt", 'a') as file:
#                 file.write(text + "\n")
#         except sr.UnknownValueError:
#             print(f"[{get_timestamp()}] Speech Recognition could not understand audio")
#         # except sr.RequestError as e:e
#         #     print(f"[{get_timestamp()}] Error in Speech Recognition service: {e}")


# Function to get the most recent audio file
def get_recent_audio_file():
    if not os.path.exists("ReceivedAudioRecordings"):
        return None
    files = os.listdir("ReceivedAudioRecordings")
    if len(files) == 0:
        return None
    files.sort(key=lambda x: os.path.getmtime(os.path.join("ReceivedAudioRecordings", x)))
    return os.path.join("ReceivedAudioRecordings", files[-1])


# Function for text-to-speech conversion
# def text_to_speech(text):
#     tts = gTTS(text)
#     tts.save("temp_audio.mp3")
#     pygame.mixer.init()
#     pygame.mixer.music.load("temp_audio.mp3")
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)


# Function to get timestamp in the specified format
def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S_%d%b%y")

# Function to play a .wav file locally
def play_audio_file(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


# GUI input box for sending messages
input_box = Entry(server_window, width=80)
input_box.pack()

# GUI button_push_to_talk to send messages
button_send = Button(server_window, text="Send", command=lambda: send_text_message(), args =)
button_send.pack()

# Start the server
start_server()

# Establish connection with the server
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.connect((SEAHAWK_IP_ADDRESS, SERVER_PORT))

# Run the server GUI window
server_window.mainloop()
