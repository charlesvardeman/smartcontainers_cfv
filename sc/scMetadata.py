# Metadata functions

from sarge import Command, Capture, get_stdout, get_stderr, capture_stdout
import provinator

class scMetadata:
    def __init__(self):
        pass

    def appendData(self, filepath):
        with open(filepath, 'a') as provfile:
            provfile.write(provinator.get_commit_data())
