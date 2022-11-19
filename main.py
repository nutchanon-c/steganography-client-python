import subprocess
import os
from dotenv import load_dotenv

def itersplit_into_x_chunks(string, x): # we assume here that x is an int and > 0
    size = len(string)
    chunksize = size//x
    for pos in range(0, size, chunksize):
        yield string[pos:pos+chunksize]

def loopEncode(key, path, message):
    listDir = os.listdir(path)
    print(len(listDir))
    splitList = list(itersplit_into_x_chunks(message, len(listDir)))
    for i in range(len(listDir)):
        word = splitList[i]
        fileName = listDir[i]
        f = os.path.join(path, fileName)
        print(f)
        p = subprocess.Popen(['node', './stega-encode.js', f, word, key, f"{(str(i)).zfill(len(str(len(listDir))))}.jpg"], stdout=subprocess.PIPE)
        out = readCleanSTDOUT(p)
        print(out)

    # for filename in listDir:
    #     f = os.path.join(path, filename)
    #     print(f)

    #     p = subprocess.Popen(['node', './stega-encode.js', f, message, key], stdout=subprocess.PIPE)
    #     out = readCleanSTDOUT(p)
    #     print(out)

def loopDecode(folderPath, key):
    pass

def executeCommand(command):
    pass


def executeCommandAndGetValue(command):
    # TODO: implement. See dunder main
    pass


def readCleanSTDOUT(p):
    return (p.stdout.read().decode()).strip()



if __name__ == "__main__":    
    # TODO: LOAD UUID
    # TODO: LOAD KEY FROM FILE?
    load_dotenv()

    key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    message = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
    outputFolderPath = "./output"
    imageFolder = "./images"
    if not os.path.exists(outputFolderPath):
        os.mkdir("output")


    loopEncode(key, imageFolder, message)

    # listDir = os.listdir(imageFolder)
    # for filename in listDir:
    #     f = os.path.join(imageFolder, filename)
    #     print(f)

    #     p = subprocess.Popen(['node', './stega-encode.js', f, message, key], stdout=subprocess.PIPE)
    #     out = readCleanSTDOUT(p)
    #     print(out)
    # p = subprocess.Popen(['node', './stega-decode.js'], stdout=subprocess.PIPE)
    # out = readCleanSTDOUT(p)
    # print(out)
    # for char in out:
    #     print(char)
    # testValue = os.getenv('TEST_VALUE')
    # print(testValue)