from threading import Lock
import pickle

from thou.colours import FG_GREEN, FG_YELLOW, FG_RED, RESET


class BackedUpQueue:

    def __init__(self):
        self.lock = Lock()
        self._contents = list()

    def put(self, item):
        with self.lock:
            self._contents.append(item)

    def get(self, *args, **kwargs):
        with self.lock:
            return self._contents.pop(0)

    def empty(self):
        with self.lock:
            return len(self._contents) == 0

    def save(self):
        print(f'{FG_GREEN}Saving state{RESET}')
        with open('thou_links.pickle', 'wb') as f:
            with self.lock:
                pickle.dump(self._contents, f)

    def load(self):
        with open('thou_links.pickle', 'rb') as f:
            with self.lock:
                self._contents = pickle.load(f)
