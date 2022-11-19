import subprocess
import os
from dotenv import load_dotenv
import uuid
import random
import string
import requests
import json
from cryptography.fernet import Fernet
import base64
import textwrap
import math
from itertools import islice
import boto3
import az_sql

def generate32BitKey():
    res = ''.join(random.choices(string.ascii_letters, k=32))
    return res


def itersplit_into_x_chunks(string, x): # we assume here that x is an int and > 0
    size = len(string)
    chunksize = size//x
    for pos in range(0, size, chunksize):
        yield string[pos:pos+chunksize]

def loopEncode(key, path, message):
    listDir = os.listdir(path)
    # messageSplitList = textwrap.wrap(message,  math.ceil(len(message) / (len(listDir) - 1)))    
    # print("".join(splitList))
    # print(len(listDir))
    # print(len(messageSplitList))
    # print(messageSplitList)
    # print(''.join(messageSplitList) == message)

    chunksize = -(-len(message) // len(listDir))
    iterator = iter(message)
    messageSplitList = []
    for _ in range(len(listDir)):
        messageSplitList.append(''.join(islice(iterator, chunksize)))
        # print(''.join(list(islice(iterator, chunksize))))
    # print(messageSplitList)

    for i in range(len(listDir)):
        word = messageSplitList[i]  
        fileName = listDir[i]
        f = os.path.join(path, fileName)
        # print(f)
        p = subprocess.Popen(['node', './stega-encode.js', f, word, key, f"{(str(i)).zfill(len(str(len(listDir))))}.jpg"], stdout=subprocess.PIPE)
        out = readCleanSTDOUT(p)
        # print(out)
        

def loopDecode(folderPath, key):
    pass

def executeCommand(commandList):
    p = subprocess.Popen(commandList, stdout=subprocess.PIPE)
    pass


def executeCommandAndGetValue(command):
    # TODO: implement. See dunder main
    pass

def encryptWithFernet(key, message):    
    encodedKey = key.encode("utf-8")
    keyB64 = base64.b64encode(encodedKey)
    fernet = Fernet(keyB64)
    encryptedMessage = fernet.encrypt(bytes(message, encoding="utf-8"))
    encryptedString = encryptedMessage.decode("utf-8")
    return encryptedString

def decryptWithFernet(key, message):
    encodedKey = key.encode("utf-8")
    keyB64 = base64.b64encode(encodedKey)
    fernet = Fernet(keyB64)
    decrypted = fernet.decrypt(message.encode("utf-8"))
    decryptedString = decrypted.decode("utf-8")
    return decryptedString

def readCleanSTDOUT(p):
    return (p.stdout.read().decode()).strip()

def getUserID():
    if not os.path.exists('./uuid.txt'):
        id = uuid.uuid4()
        with open ("./uuid.txt", "w") as f:
            f.write(str(id))
        return id
    else:
        with open("./uuid.txt","r") as f:
            return f.read()



if __name__ == "__main__":    
    load_dotenv()
    api_url = os.getenv('API_MASTER_URL')
    user_id = getUserID()
    print(f"User id: {user_id}")

    menu = int(input("Select menu: \n1. New image set\n2. Request Image Set\n3. Revoke\n"))
    attribute = "sysadmin"
    try:
        az_sql.insertPerson(user_id, [attribute])
    except:
        print("sql insert user exception")
    if menu == 1:        
        # send request for new picture set id
        res = json.loads(requests.get(f"{api_url}/newID").text)
        new_set_id = res.get('id')
        print(f"new set id: {new_set_id}")
        key = generate32BitKey()
        print(f"session key generated: {key}")

        try:
            az_sql.insertImageSet(new_set_id, user_id, [attribute])
        except:
            print("sql insert image set exception")

        # save key to file
        if not os.path.exists("./keys"):
            os.makedirs("./keys")
        with open(f"./keys/{new_set_id}.key.txt", "w") as f:
            f.write(key)        

        # ask for plaintext file
        ptPath = input("Plaintext file path: ")

        # read plaintext from file
        try:
            f = open(ptPath, "r")
            message = f.read()
            # print(message)
            f.close()
        except Exception as e:
            print(f"open file error: {e}")
            exit(1)
        

        
        # ask for image folder?
        imageFolder = "./images"
        
        outputFolderPath = "./output"

        if not os.path.exists(outputFolderPath):
            os.mkdir("output")

        # encrypt plaintext with key using fernet
        encrypted = encryptWithFernet(key, message)
        # print(encrypted)
        # decrypted = decryptWithFernet(key, encrypted)
        # print(decrypted)
        
        # encode: DONE!
        loopEncode(key, imageFolder, message)

        # encrypt key with cpabe
        abe_pubkey_path = "../abe/pub_key"
        sessionKeyFilePath = f"./keys/{new_set_id}.key.txt"
        try:
            executeCommand(["cpabe-enc", abe_pubkey_path, sessionKeyFilePath, f"({attribute})"])
        except:
            print("execute command error")
        
        # loop upload and add each url to Map {url: url, sequence: sequence_number}
        cloudClient = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        clientResponse = cloudClient.list_buckets()

        outputDirList = os.listdir('./output')

        payload = {"files": [], "set_id": new_set_id, "uuid": user_id, "user_attributes": attribute.split()}

        awsBucketName = os.getenv('AWS_BUCKET_NAME')
        awsRegion = os.getenv('AWS_REGION')

        # CHANGE TO ENCRYPTED KEY PATH
        try:
            print(f"Uploading session key", end="")
            response = cloudClient.upload_file(f"./keys/{new_set_id}.key.txt.cpabe", awsBucketName, f"{user_id}/{new_set_id}/{new_set_id}.key.txt")
            # response = cloudClient.upload_file(f"./keys/{new_set_id}.key.txt", awsBucketName, f"{user_id}/{new_set_id}/{new_set_id}.key.txt")
            print("...done", end="\n")
            keyUrl = f"https://{awsBucketName}.s3.{awsRegion}.amazonaws.com/{user_id}/{new_set_id}/{new_set_id}.key.txt"
            payload["keyPath"] = keyUrl    
            try:
                az_sql.insertESK(new_set_id, keyUrl)        
            except:
                print("sql upload key exception")
        except Exception as e:
            print(e)


        seq = 1
        for fileName in outputDirList:
            # print(fileName)
            try:
                print(f"Uploading {fileName}", end="")
                response = cloudClient.upload_file(f"./output/{fileName}", awsBucketName, f"{user_id}/{new_set_id}/{fileName}")
                print("...done", end="\n")
                url = f"https://{awsBucketName}.s3.{awsRegion}.amazonaws.com/{user_id}/{new_set_id}/{fileName}"
                payload["files"].append({"url": url, "sequence": seq})
                try:
                    az_sql.insertSG(new_set_id, keyUrl, url, seq)
                except Exception as e:
                    print("sql insert SG exception")
                    print(e)
                seq+=1
                # print(url)
            except Exception as e:
                print(e)
        # print(payload)

        # send payload to master
        response = requests.post(f"{api_url}/new", json=payload)
        print(json.loads(response.text))
        
        

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