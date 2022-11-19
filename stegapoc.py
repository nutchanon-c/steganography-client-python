
import cv2
import string
import os


def stegaEncode(key, file, text):
    
    d={}
    c={}

    for i in range(255):
        d[chr(i)]=i
        c[i]=chr(i)
    
    
    #print(c)

    x=cv2.imread(file)

    i=x.shape[0]
    j=x.shape[1]
    print(i,j)

    # key=input("Enter key to edit(Security Key) : ")
    # text=input("Enter text to hide : ")
    # text="gAAAAABjeIy4MIjOsYbHb-yQB1tRwDVS1iTycVcbl6rs5F3fedHOkYbReCqSG7YZgCGWYAi3rmmh-LncQp-458dCdOKluTnPyA=="
    # text = '''
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    # '''
    kl=0
    tln=len(text)
    z=0 #decides plane
    n=0 #number of row
    m=0 #number of column

    l=len(text) # TODO: DIVIDE STRING HERE

    for i in range(l):
        x[n,m,z]=d[text[i]]^d[key[kl]]
        n=n+1
        m=m+1
        m=(m+1)%3 #this is for every value of z , remainder will be between 0,1,2 . i.e G,R,B plane will be set automatically.
                    #whatever be the value of z , z=(z+1)%3 will always between 0,1,2 . The same concept is used for random number in dice and card games.
        kl=(kl+1)%len(key)
        
    cv2.imwrite(f"{file}.enc.jpg",x) 
    # os.startfile("encrypted_img.jpg")
    print("Data Hiding in Image completed successfully.")
    #x=cv2.imread(“encrypted_img.jpg")
        

    kl=0
    tln=len(text)
    z=0 #decides plane
    n=0 #number of row
    m=0 #number of column


    

    
    
 
    
    
    