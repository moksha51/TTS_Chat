import tkinter as tk
from audio import record_audio, play_canned_message, play_recent_audio, save_audio
import sys
import socket
import errno
from main import SEAHAWK_IP_ADDRESS


def play_recent_audio_message():
    play_recent_audio()
    print("Replaying most recent audio transmission")

def start_gui_server():

    window = tk.Tk()
    window.title("Radio Comms(Server)")

    recent_audio_button = tk.Button(window, text="Replay", command=play_recent_audio_message)
    recent_audio_button.pack()

    play_siren_button = tk.Button(window, text="Play", command=play_recent_audio_message)
    recent_audio_button.pack()

    window.mainloop()


start_gui_server()
