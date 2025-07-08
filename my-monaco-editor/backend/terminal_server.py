import os
import sys
import threading

from flask import Flask
from flask_socketio import SocketIO, emit
from ptyprocess import PtyProcess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store PtyProcess instance for each session
pty_processes = {}

@socketio.on('connect')
def connect():
    print('Client connected')
    # Start a new PtyProcess for each connection
    try:
        # Use the default shell for the user
        shell = PtyProcess.spawn([os.environ.get('SHELL', 'bash')])
        pty_processes[os.getpid()] = shell
        print(f"PTY process started with PID: {shell.pid}")

        # Start a thread to read from the PTY and send to client
        threading.Thread(target=read_from_pty, args=(shell,)).start()
        emit('output', 'Welcome to the interactive terminal!\n')
    except Exception as e:
        print(f"Error starting PTY process: {e}")
        emit('output', f"Error starting terminal: {e}\n")

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')
    current_pid = os.getpid()
    if current_pid in pty_processes:
        shell = pty_processes[current_pid]
        shell.close()
        del pty_processes[current_pid]
        print(f"PTY process for PID {current_pid} closed.")

@socketio.on('input')
def handle_input(data):
    current_pid = os.getpid()
    if current_pid in pty_processes:
        shell = pty_processes[current_pid]
        try:
            shell.write(data)
        except Exception as e:
            print(f"Error writing to PTY: {e}")

@socketio.on('resize')
def handle_resize(data):
    current_pid = os.getpid()
    if current_pid in pty_processes:
        shell = pty_processes[current_pid]
        try:
            shell.setwinsize(data['rows'], data['cols'])
        except Exception as e:
            print(f"Error resizing PTY: {e}")

def read_from_pty(shell):
    while shell.isalive():
        try:
            output = shell.read(1024).decode(errors='ignore')
            if output:
                socketio.emit('output', output)
        except EOFError:
            # PTY closed
            break
        except Exception as e:
            print(f"Unexpected error in read_from_pty: {e}")
            break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
