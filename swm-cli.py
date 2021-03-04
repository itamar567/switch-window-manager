from multiprocessing.connection import Client
from Preferences import Preferences
import sys

# Send received args to server
server = Client(Preferences.address)
server.send(sys.argv[1:])
