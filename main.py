import shutil
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
    listDir = sorted(listDir)
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
    listDir = os.listdir(folderPath)
    listDir = sorted(listDir)
    res = ""
    for fileName in listDir:
        p = subprocess.Popen(['node', './stega-decode.js', f"{folderPath}/{fileName}", key], stdout=subprocess.PIPE)
        out = readCleanSTDOUT(p)
        # print(out)
        res = res + out
    # print(res)
    return res



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
    # print(p.stdout.read().decode())
    return (p.stdout.read().decode())

def getUserID():
    if not os.path.exists('./uuid.txt'):
        id = uuid.uuid4()
        with open ("./uuid.txt", "w") as f:
            f.write(str(id))
        return id
    else:
        with open("./uuid.txt","r") as f:
            return f.read()

def deleteFilesFromFolder(folder):
        for fileName in os.listdir(folder):
            file_path = os.path.join(folder, fileName)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


if __name__ == "__main__":    
    load_dotenv()
    api_url = os.getenv('API_MASTER_URL')
    user_id = getUserID()
    print(f"User id: {user_id}")

    menu = int(input("Select menu: \n1. New image set\n2. Request Image Set\n3. Revoke\n>>>"))
    attribute = "sysadmin"
    # try:
    #     az_sql.insertPerson(user_id, [attribute])
    # except:
    #     print("sql insert user exception")
    if menu == 1:   
        # send request for new picture set id
        res = json.loads(requests.get(f"{api_url}/newID").text)
        new_set_id = res.get('id')
        print(f"new set id: {new_set_id}")
        key = generate32BitKey()
        print(f"session key generated: {key}")

        # try:
        #     az_sql.insertImageSet(new_set_id, user_id, [attribute])
        # except:
        #     print("sql insert image set exception")

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
        # encrypted = encryptWithFernet(key, message)
        # print(encrypted)
        # decrypted = decryptWithFernet(key, encrypted)
        # print(decrypted)
        
        # encode: DONE!
        loopEncode(key, imageFolder, message)

        # encrypt key with cpabe
        abe_pubkey_path = "../abe/pub_key"
        sessionKeyFilePath = f"./keys/{new_set_id}.key.txt"
        try:
            print("Encrypting Session Key with CP-ABE")
            executeCommand(["cpabe-enc", abe_pubkey_path, sessionKeyFilePath, f"{attribute}"])
            print("Encrypting Session Key Finished")
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

        payload = {"files": [], "set_id": new_set_id, "uuid": str(user_id), "user_attributes": attribute.split()}

        awsBucketName = os.getenv('AWS_BUCKET_NAME')
        awsRegion = os.getenv('AWS_REGION')

        # CHANGE TO ENCRYPTED KEY PATH
        try:
            print(f"Uploading session key", end="")
            response = cloudClient.upload_file(f"./keys/{new_set_id}.key.txt.cpabe", awsBucketName, f"{user_id}/{new_set_id}/{new_set_id}.key.txt.cpabe")
            # response = cloudClient.upload_file(f"./keys/{new_set_id}.key.txt", awsBucketName, f"{user_id}/{new_set_id}/{new_set_id}.key.txt")
            print("...done", end="\n")
            keyUrl = f"https://{awsBucketName}.s3.{awsRegion}.amazonaws.com/{user_id}/{new_set_id}/{new_set_id}.key.txt.cpabe"
            payload["keyPath"] = keyUrl    
            # try:
            #     az_sql.insertESK(new_set_id, keyUrl)        
            # except:
            #     print("sql upload key exception")
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
                # try:
                #     az_sql.insertSG(new_set_id, keyUrl, url, seq)
                # except Exception as e:
                #     print("sql insert SG exception")
                #     print(e)
                seq+=1
                # print(url)
            except Exception as e:
                print(e)
        # print(payload)

        # send payload to master
        response = requests.post(f"{api_url}/new", json=payload)
        print(json.loads(response.text))

        # save plaintext and setid
        if not os.path.exists('./sets.json'):
            with open("./sets.json", "w") as f:
                dataToSave = json.dumps({ptPath: new_set_id })
                f.write(dataToSave)
        else:
            with open("./sets.json") as f:
                loadedData = json.loads(f.read())
                loadedData[ptPath] = new_set_id
                with open("./sets.json", "w") as w:
                    w.write(json.dumps(loadedData))
        deleteFilesFromFolder('./output')


    elif menu == 2:
        requestSetId = input("Image Set ID: ")
        payload = {"set_id": requestSetId, "uuid": user_id}
        response = requests.post(f"{api_url}/request", json=payload)
        responseJson = json.loads(response.text)
        # print(f"REQUEST RESPONSE: {responseJson}")
        encSKUrl = responseJson.get("key_url")
        sortedBySequence = sorted(responseJson.get('files'), key=lambda d: int(d['sequence']))         
        sortedToList = [x.get('url') for x in sortedBySequence]


        # download files
        if not os.path.exists('./downloads/images'):
            os.makedirs('./downloads/images')
        if not os.path.exists('./downloads/keys'):
            os.makedirs('./downloads/keys')
        keyFileName = encSKUrl.split("/")[-1]
        print("Downloading Encrypted Session Key")
        response = requests.get(encSKUrl)
        open(f"./downloads/keys/{keyFileName}", "wb").write(response.content)
        print("Encrypted Session Key Downloaded")
        for i in range(len(sortedToList)):
            url = sortedToList[i]
            # fileExtension = url.split(".")[-1]
            fileName = url.split("/")[-1]
            print(f"Downloading file: {fileName}", end="")
            response = requests.get(url)
            open(f"./downloads/images/{fileName}", "wb").write(response.content)
            print("...done")

        # FIX CPABE DECRYPTION
        try:
            print("Decrypting Session Key with CP-ABE")
            abe_pubkey_path = "../abe/pub_key"
            sessionKeyFilePath = f"./downloads/keys/{keyFileName}"
            abeKeyPath = "./sysadmin-key"
            # executeCommand(["cpabe-dec", abe_pubkey_path, abeKeyPath, sessionKeyFilePath])
            p = subprocess.run(f"cpabe-dec {abe_pubkey_path} {abeKeyPath} {sessionKeyFilePath}", shell=True, stdout=subprocess.DEVNULL)

            print("Decryption Finished")

        except Exception as e:
            print(e)


        # READ DECRYPTED SESSION KEY
        keyFileRead = open(f"./downloads/keys/{requestSetId}.key.txt", "r")
        keyString = keyFileRead.read()


        """
        MOCK DATA: 
        set id: d336d5fd-e502-4440-872c-f68cce4c71bc
        key: VTZfYZPvHnaiJCkKXqsnqJgaJztvYINz
        """
        print("Decrypted...")
        # USE ACTUAL KEY
        extractEncrypted = loopDecode(f"./downloads/images", keyString)

        # SAVE DECRYPTED TO FILE
        if not os.path.exists('./decrypted'):
            os.makedirs('./decrypted')
        with open(f"./decrypted/{requestSetId}.txt", "w") as f:
            f.write(extractEncrypted)
        print(f"Decrypted to /decrypted/{requestSetId}.txt")
        print("Deleting all files in downloads folder")
        deleteFilesFromFolder('./downloads/images')
        deleteFilesFromFolder('./downloads/keys')
        print("Deletion complete")
        print("Exiting program")
        exit(0)

    elif menu == 3:
        print("Revoke")
        revokeSetId = input("Picture Set ID: ")
        newAttributes = input("New Attributes (comma-separated): ")
        newAttributesList = newAttributes.split(",")
        print(newAttributesList)
        payload = {"uuid": user_id, "new_attr": newAttributesList, "set_id": revokeSetId}
        response = requests.post(f"{api_url}/revoke", json=payload)
        print(response.text)

