from dotenv import load_dotenv
import pyodbc
import os
load_dotenv()

SERVER = os.getenv('AZURE_SERVER')
DATABASE = os.getenv('AZURE_DATABASE')
USERNAME = os.getenv('AZURE_USERNAME')
PASSWORD = os.getenv('AZURE_PASSWORD')
DRIVER = os.getenv('AZURE_DRIVER')

def insertPerson(uid, attrList):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f"INSERT INTO Person VALUES ('{uid}','{','.join([str(attr) for attr in attrList])}');"
        with conn.cursor() as cursor:
            cursor.execute(query)

def insertImageSet(psid, uid, attrList):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f"INSERT INTO ImageSet VALUES ('{psid}', '{uid}', '{','.join([str(attr) for attr in attrList])}');"
        with conn.cursor() as cursor:
            cursor.execute(query)

def insertESK(psid, filePath):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f"INSERT INTO ESK VALUES ('{psid}','{filePath}');"
        with conn.cursor() as cursor:
            cursor.execute(query)

def insertSG(psid, enc_filePath, stego_filePath, seqNo):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f"INSERT INTO SG VALUES ('{psid}','{enc_filePath}', '{stego_filePath}', '{seqNo}');"
        with conn.cursor() as cursor:
            cursor.execute(query)

def getUserAttributes(userid):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''SELECT attriList FROM Person
                    WHERE userid = '{userid}';'''
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return row[0].split(',')
            else:
                return []

def getISAttributes(psid):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''SELECT permitAttriList FROM ImageSet
                WHERE psid = '{psid}';
                '''
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return row[0].split(',')
            else:
                return []

def getISOwner(psid):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''SELECT Person.userid, psid, attriList, permitAttriList FROM Person
                    INNER JOIN ImageSet ON Person.userid = ImageSet.userid
                    WHERE ImageSet.psid = '{psid}';
                '''
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return [x.split(',') for x in row]
            else:
                return []

def getSessionKey(psid):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''
                    SELECT ESK.psid, enc_filePath FROM ESK
                    INNER JOIN ImageSet ON ImageSet.psid = ESK.psid
                    WHERE ImageSet.psid = '{psid}';
                '''
        with conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return row[1]
            else:
                return []
def getAllImage(psid):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''
                   SELECT stego_filePath, seqNo FROM SG
                    INNER JOIN ImageSet ON ImageSet.psid = SG.psid
                    WHERE ImageSet.psid = '{psid}';
                '''
        with conn.cursor() as cursor:
            cursor.execute(query)
            res = []
            row = cursor.fetchone()
            while row:
                res.append({"url": row[0], "sequence": row[1]})
                row = cursor.fetchone()
    return res


def editESK(psid, newLink):
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''
        UPDATE ESK SET enc_filePath = '{newLink}' WHERE psid = '{psid}';
        UPDATE SG SET enc_filePath = '{newLink}' WHERE psid = '{psid}';
        '''
        with conn.cursor() as cursor:
            cursor.execute(query)


def resetDB():
    with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD) as conn:
        query = f'''
        DROP TABLE SG, ESK, ImageSet, Person
-- Create Person table
CREATE TABLE Person
(
    userid NVARCHAR(256)  PRIMARY KEY,
    attriList NVARCHAR(256) NOT NULL,

)

-- Create IS table
CREATE TABLE ImageSet
(
    psid NVARCHAR(256)  PRIMARY KEY,
    userid NVARCHAR(256) REFERENCES Person (userid),
    permitAttriList NVARCHAR(256) NOT NULL
)

-- Create ESK table
CREATE TABLE ESK
(
    psid NVARCHAR(256) REFERENCES ImageSet (psid),
    enc_filePath NVARCHAR(256),
)

-- Create SG table
CREATE TABLE SG
(
    psid NVARCHAR(256) REFERENCES ImageSet (psid),
    enc_filePath NVARCHAR(256),
    stego_filePath NVARCHAR(256) NOT NULL,
    seqNo INT,

)
        '''
        with conn.cursor() as cursor:
            cursor.execute(query)


if __name__ == "__main__":
    # insertPerson("test1", [1, 2])
    # insertImageSet(1, "test", [1, 2])
    # insertESK(1, "a")
    # insertSG(1, "a", "a", 2)
    # print(getUserAttributes("test"))
    # print(getUserAttributes("a"))
    # print(getISAttributes(1))
    # print(getISOwner(1))
    # print(getSessionKey(1))
    # print(getAllImage(1))
    # editESK(1, "c")
    resetDB()

