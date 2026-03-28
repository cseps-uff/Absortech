import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.application.main import start

if __name__ == "__main__":
    start()
