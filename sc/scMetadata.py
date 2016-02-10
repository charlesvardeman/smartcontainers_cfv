# Metadata functions

from sarge import Command, Capture, get_stdout, get_stderr, capture_stdout
import provinator

class scMetadata:
    def __init__(self):
        pass

    def fileCopyOut(self, dockerlocation, containerid, filename, path):
            copy_cmd =  str(dockerlocation) + ' cp ' + containerid + ":" + path + filename + " ."
            thisCommand = Command(copy_cmd)
            thisCommand.run()

    def fileCopyIn(self, dockerlocation, containerid, filename, path):
            copy_cmd =  str(dockerlocation) + ' cp '+ filename + " " + containerid + ":" + path + filename
            thisCommand = Command(copy_cmd)
            thisCommand.run()

    def appendData(self, filepath):
        with open(filepath, 'a') as provfile:
            provfile.write(provinator.get_commit_data())

    def hasProv(self, containerid, filename, path):
        file = capture_stdout("docker exec " + containerid + " ls " + path)
        for line in file.stdout:
            if filename in line:
                return True
        return False