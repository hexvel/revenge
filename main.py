import threading
from start import start

if __name__ == '__main__':
    threading.Thread(target=start, args=()).start()
