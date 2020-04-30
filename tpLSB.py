import os
import numpy as np
import random, math
import sys
from cmath import sqrt
import imageio
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt

"""
Reads an image file
filename : path of the image file
:returns the array of the pixels of the image (in RGB style)
"""
def read_img(filename):
    pixels = imageio.imread(filename)
    return pixels

"""
Writes an image file
filename : path of the file to write in
pixels : array of pixels to write from
"""
def write_img(filename, pixels):
    imageio.imwrite(filename, pixels)


"""
Returns the content of a text file
filename : path of the file
:returns string of the content
"""
def messageRead(fileName):
    file = open(fileName, "r")
    content = file.read()
    file.close()
    return content

"""
Writes a text into a file
message : text to write
filename : path of the file to write in
"""
def messageWrite(message, fileName):
    file = open(fileName, "w")
    file.write(message)
    file.close()


"""
Converts an integer into a list of '1' or '0' (binary)
(the integer has to been positive and between 0 and 255,
the list length is then of 8)
integer : int to convert
:returns a list of bits
"""
def intToBits(integer):
    temp = integer
    listBits = []  # initialisation du tableau de bits
    for i in range(7, -1, -1):
        if temp // (2 ** i):
            listBits.append(1)
            temp = temp % (2 ** i)
        else:
            listBits.append(0)
    return listBits

"""
Converts a list of bits into an integer
listBits : list of bits to convert
:returns the corresponding integer
"""
def bitsToInt(listBits):
    integer = 0  # entier correspondant au tableau de bits
    for i in range(len(listBits)):
        integer += (listBits[i] * (2 ** (len(listBits) - 1 - i)))
    return integer

"""
Converts a character into its corresponding list of bits
according to the ASCII table
char : character to convert
:returns list of bits 
"""
def charToBits(char):
    intAssociated = ord(char)   # integer ASCII of the character
    return intToBits(intAssociated)

"""
Converts a list of bits into its corresponding character
according to the ASCII table
listBits : list to convert
:returns the corresponding character
"""
def bitsToChar(listBits):
    intAssociated = bitsToInt(listBits)
    char = chr(intAssociated)     # character corresponding to the ASCII integer
    return char

"""
Returns an encrypted message with the AES algorithm
key : bytes used to construct the AES key
messageToEncrypt : string to encrypt
:returns string encrypted
"""
def encryptAES(key, messageToEncrypt):
    cipher_suite = Fernet(key)
    messageEncrypted = cipher_suite.encrypt(bytes(messageToEncrypt, "utf-8"))
    return messageEncrypted.decode('utf-8')

"""
Returns a decrypted message with the AES algorithm
key : bytes used to construct the AES key
messageToDecrypt : string to decrypt
:returns string decrypted
"""
def decryptAES(key, messageToDecrypt):
    cipher_suite = Fernet(key)
    messageDecrypted = cipher_suite.decrypt(bytes(messageToDecrypt, 'utf-8'))
    return messageDecrypted.decode('utf-8')


"""
Returns the size of a message into a list of bits format,
the number of bits in this list is calculated from the number of
pixels in an image
Then, additional 0 are added to the list if needed
sizeMessage : size of a text message
numberOfPixels : number of pixels of an image array
:returns list of bits
"""
def getSizeInList(sizeMessage,numberOfPixels):
    numberOfLSB = numberOfPixels*3
    numberOfBits = math.ceil(math.log2(numberOfLSB))
    while numberOfBits % 3 != 0:
        numberOfBits += 1
    if sizeMessage is None:
        return numberOfBits * "0"
    toReturn = format(sizeMessage*8, '0'+str(numberOfBits)+'b')
    return toReturn


"""
Returns the name of a file without its entire path or extension
path : string
:returns file name
"""
def getFileName(path):
    extensionIndex = path.find(".")
    withoutExtension = path[:extensionIndex]
    lastSlash = withoutExtension.rfind("/")
    fileName = withoutExtension[lastSlash+1:]
    return fileName


"""
Inserts a message into an array of pixels of an image,
according to the LSB classic algorithm
message : message to hide
imageArrayToInsert : array of pixels of an image
:returns the new array where the message has been inserted in the LSBs
"""
def insertWithoutRandom(message, imageArrayToInsert):
    tempArray = np.copy(imageArrayToInsert)  # copy of the nparray of the image
    width = len(tempArray[0])
    height = len(tempArray)
    sizeList = getSizeInList(len(message),width*height) #list of bits of the size of the message
                                                        #Has to be inserted in the beginning of the array
    concatList = []
    for k in range(len(sizeList)):
        concatList.append(int(sizeList[k]))
    for i in range(len(message)):
        listBitsChar = charToBits(message[i])
        for j in range(len(listBitsChar)):
            concatList.append(listBitsChar[j])
    start = 0                   #concatList contains all the bits (including the message length) to insert
    for l in range(height):
        for e in range(width):
            [r, g, b] = tempArray[l][e]
            if start < len(concatList):
                rToBits = intToBits(r)
                rToBits[len(rToBits)-1] = concatList[start]
                r = bitsToInt(rToBits)
                start += 1
            if start < len(concatList):
                gToBits = intToBits(g)
                gToBits[len(gToBits) - 1] = concatList[start]
                g = bitsToInt(gToBits)
                start += 1
            if start < len(concatList):
                bToBits = intToBits(b)
                bToBits[len(bToBits) - 1] = concatList[start]
                b = bitsToInt(bToBits)
                start += 1
            tempArray[l][e] = [r, g, b]
    return tempArray

"""
Inserts a message into an array of pixels of an image,
according to the LSB random algorithm
message : message to hide
imageArrayToInsert : array of pixels of an image
:returns the new array where the message has been inserted in the LSBs
"""
def insertWithRandom(message, imageArrayToInsert):
    tempArray = np.copy(imageArrayToInsert)  # copy of the nparray of the image
    width = len(tempArray[0])
    height = len(tempArray)
    sizeList = getSizeInList(len(message), width * height)  # list of bits of the size of the message
    # Has to be inserted in the beginning of the array
    concatList = []
    for k in range(len(sizeList)):
        concatList.append(int(sizeList[k]))
    for i in range(len(message)):
        listBitsChar = charToBits(message[i])
        for j in range(len(listBitsChar)):
            concatList.append(listBitsChar[j])
    start = 0                   #concatList contains all the bits (including the message length) to insert
    RANDOM = [-1,1]
    for l in range(height):
        for e in range(width):
            [r, g, b] = tempArray[l][e]
            if start < len(concatList):
                rToBits = intToBits(r)
                if rToBits[len(rToBits)-1]!=concatList[start]:
                   if r==255:r=254
                   elif r==0:r=1
                   else:r+=RANDOM[random.randint(0,1)]
                start += 1
            if start < len(concatList):
                gToBits = intToBits(g)
                if gToBits[len(gToBits) - 1] != concatList[start]:
                    if g == 255:g = 254
                    elif g == 0:g = 1
                    else:g += RANDOM[random.randint(0, 1)]
                start += 1
            if start < len(concatList):
                bToBits = intToBits(b)
                if bToBits[len(bToBits) - 1] != concatList[start]:
                    if b == 255:b= 254
                    elif b == 0:b = 1
                    else:b += RANDOM[random.randint(0, 1)]
                start += 1
            tempArray[l][e] = [r, g, b]
    return tempArray

"""
Extracts a message from an array of pixels of an image,
according to the LSB algorithm (either classic of random)
imageArrayToExtract : array of pixels of an image
:returns the extracted message
"""
def extract(imageArrayToExtract):
    concatList = []
    tempArray = np.copy(imageArrayToExtract)  # copy of the nparray of the image
    width = len(tempArray[0])
    height = len(tempArray)
    start = 0
    length = len(getSizeInList(None,width*height))  #gives the number of bits which has been
                                                    #necessary to hide the message length
    size = 0
    sizeList = []
    sizeX, sizeY = 0, 0
    for j in range(height):
        for k in range(width):
            [r, g, b] = tempArray[j][k]
            if size < length:
                rToBits = intToBits(r)
                sizeList.append(rToBits[len(rToBits) - 1])
                size += 1
                sizeX, sizeY = j, k
            if size < length:
                gToBits = intToBits(g)
                sizeList.append(gToBits[len(gToBits) - 1])
                size += 1
                sizeX, sizeY = j, k
            if size < length:
                bToBits = intToBits(b)
                sizeList.append(bToBits[len(bToBits) - 1])
                size += 1
                sizeX, sizeY = j, k
    messageLength = bitsToInt(sizeList)         #gets the message length
    for l in range(height):
        for e in range(width):
            if(l> sizeX or e > sizeY):
                [r, g, b] = tempArray[l][e]
                if start < messageLength:
                    rToBits = intToBits(r)
                    concatList.append(rToBits[len(rToBits) - 1])
                    start += 1
                if start < messageLength:
                    gToBits = intToBits(g)
                    concatList.append(gToBits[len(gToBits)-1])
                    start += 1
                if start < messageLength:
                    bToBits = intToBits(b)
                    concatList.append(bToBits[len(bToBits)-1])
                    start += 1
    message = ""
    for i in range(messageLength):
        characterListBits = concatList[(i*8):(i*8+8)] # gets a sublist of 8 elements, because character are encoded in ASCII
        character = bitsToChar(characterListBits)   # gets a character with its ASCII bit's list
        message = message+character
    return message

"""
Launches a detection analysis of possible message hiding in an image
according to the Sample Pair Analysis
filename : path of the image file
:returns a score of detection 
"""
def detection(fileName):
    map = {0: 'R', 1: 'G', 2: 'B'}
    pixels = read_img(fileName)
    width, height, channels = pixels.shape
    averageScore = 0.0
    for color in range(3):
        colorValues = pixels[:, :, color]
        x = 0;y = 0;k = 0
        for j in range(height):
            for i in range(width-1):
                currentValue = colorValues[i, j]
                nextValue = colorValues[i + 1, j]
                if (nextValue%2 == 0 and currentValue < nextValue) or (nextValue%2 == 1 and currentValue > nextValue):
                    x += 1
                if (nextValue%2 == 0 and currentValue > nextValue) or (nextValue%2 == 1 and currentValue < nextValue):
                    y += 1
                if round(nextValue/2) == round(currentValue/2):
                    k += 1
        if k == 0:
            print("Error with detection")
            sys.exit(0)
        a = 2 * k
        b = 2*(2*x-width*(height-1))
        c = y-x
        bp = (-b+sqrt(b**2-4*a*c))/(2*a)
        bm = (-b-sqrt(b**2-4*a*c))/(2*a)
        beta = min(bp.real, bm.real)
        averageScore += beta
        print(map[color] + ": ", beta)
    return abs(averageScore/3.0)


"""
Launches a massive detection analysis on different files
listOfFileName : list of all the files to analyze
:returns a list of the detection score
"""
def massiveDetection(listOfFileName):
    result =[]
    for filename in listOfFileName:
        try:
            res = detection(filename)
            result.append(res)
        except SystemError:
            print(filename)
    return result


"""
Launches a process of insertion (LSB classic) on different files,
the message is encrypted before insertion if the key is not null
The inserted images are saved in the "roc/ImagesStega" folder
listOfFileName : list of all the files to insert in
key : bytes to construct an AES key
message : message to insert (possibly encrypted before insertion)
"""
def massiveInsertionWithoutRandom(listOfFileName, key, message):
    messageToInsert = message
    if(key != None):
        messageToInsert = encryptAES(key, message)
    for filename in listOfFileName:
        print(filename)
        img = read_img(filename)
        temp = insertWithoutRandom(messageToInsert, img)
        write_img("roc/ImagesStega/"+getFileName(filename)+"_norandom.bmp", temp)


"""
Launches a process of insertion (LSB random) on different files,
the message is encrypted before insertion if the key is not null
The inserted images are saved in the "roc/ImagesStega" folder
listOfFileName : list of all the files to insert in
key : bytes to construct an AES key
message : message to insert (possibly encrypted before insertion)
"""
def massiveInsertionWithRandom(listOfFileName, key, message):
    messageToInsert = message
    if (key != None):
        messageToInsert = encryptAES(key, message)
    for filename in listOfFileName:
        print(filename)
        img = read_img(filename)
        temp = insertWithRandom(messageToInsert, img)
        write_img("roc/ImagesStega/"+getFileName(filename)+"_random.bmp", temp)


"""
Launches a process of extraction (LSB classic) on different files,
the message is decrypted after extraction if the key is not null
The extracted messages are saved in the "roc/messagesExtracted" folder
listOfFileName : list of all the files to extract from
key : bytes to construct an AES key
"""
def massiveExtractionWithoutRandom(listOfFileName, key):
    for filename in listOfFileName:
        imgWithoutRandom = read_img("roc/ImagesStega/" + getFileName(filename) + "_norandom.bmp")
        messageExtracted = extract(imgWithoutRandom)
        if(key != None):
            messageExtracted = decryptAES(key, messageExtracted)
        messageWrite(messageExtracted, "roc/messagesExtracted/message_" + getFileName(filename) + "_norandom.txt")

"""
Launches a process of extraction (LSB random) on different files,
the message is decrypted after extraction if the key is not null
The extracted messages are saved in the "roc/messagesExtracted" folder
listOfFileName : list of all the files to extract from
key : bytes to construct an AES key
"""
def massiveExtractionWithRandom(listOfFileName, key):
    for filename in listOfFileName:
        imgWithRandom = read_img("roc/ImagesStega/"+getFileName(filename)+"_random.bmp")
        messageExtracted = extract(imgWithRandom)
        if (key != None):
            messageExtracted = decryptAES(key, messageExtracted)
        messageWrite(messageExtracted, "roc/messagesExtracted/message_"+getFileName(filename)+"_random.txt")



"""
Constructs a ROC curve for a certain steganographic rate
listOfFileNameNoHide : list of all the files with no hidden messages
listOfFileNameHide : list of all the files with hidden messages
rate : steganographic rate
saveFile : path to save the curve file
"""
def constructROCCurve(listOfFileNameNoHide, listOfFileNameHide, rate, saveFile):
    resultNoHide = massiveDetection(listOfFileNameNoHide)
    resultHide = massiveDetection(listOfFileNameHide)
    step, upStepNoHide, upStepHide = 0.05, 0, 0
    for res in resultNoHide:
        if (res >= step): upStepNoHide += 1
    for res in resultHide:
        if(res >= step): upStepHide += 1

    joinedResult = resultNoHide + resultHide
    joinedResult.sort(reverse=True)
    numberOfNoHide, numberOfHide = 0, 0
    plotX, plotY = [0], [0]
    for i in range(len(joinedResult)):
        if (joinedResult[i] in resultNoHide):
            numberOfNoHide += 1
            TFP = float(numberOfNoHide) / float(len(resultNoHide))
            TVP = float(numberOfHide) / float(len(resultHide))
            plotX.append(TFP)
            plotY.append(TVP)
        elif (joinedResult[i] in resultHide):
            numberOfHide += 1
            TFP = float(numberOfNoHide) / float(len(resultNoHide))
            TVP = float(numberOfHide) / float(len(resultHide))
            plotX.append(TFP)
            plotY.append(TVP)
    plt.plot(plotX, plotY, '-o')
    plt.xlabel('TFP')
    plt.ylabel('TVP')
    plt.axis([0, 1, 0, 1])
    plt.title('ROC curve --- Steganographic rate : '+str(rate)+"%")
    text = "True positive > step rate :"+str((float(upStepHide)/float(upStepHide+upStepNoHide))*100)+"%"
    text = text + "     False positive > step rate :"+str((float(upStepNoHide)/float(upStepHide+upStepNoHide))*100)+"%"
    plt.figtext(0.5, 0.005, text, wrap=True, horizontalalignment='center', fontsize=8)
    plt.savefig(saveFile)
    plt.clf()

"""
Main method
"""
def main():
    args = sys.argv
    if(len(args) == 1):
        usage()
        sys.exit(0)

    if (args[1] == "examples" and args[2] == "noencryption"):
        print("Running examples without encryption:")
        img1 = read_img(str(args[3]))
        height, width = len(img1), len(img1[0])
        print("Image " + str(args[3]) + " (" + str(height) + "x" + str(width) + " pixels)")
        filename = getFileName(args[3])

        message100 = messageRead("messagesToInsert/message100.txt")
        message600 = messageRead("messagesToInsert/message600.txt")
        message1500 = messageRead("messagesToInsert/message1500.txt")
        message3000 = messageRead("messagesToInsert/message3000.txt")
        print()
        print("Starting insertion LSB classic:")
        print("100 characters message ...")
        print("Steganography rate :" + str((100.0 / float(width * height * 3)) * 100) + "%")
        nr100 = insertWithoutRandom(message100, img1)
        write_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom100.bmp", nr100)

        print("600 characters message ...")
        print("Steganography rate :" + str((600.0 / float(width * height * 3)) * 100) + "%")
        nr600 = insertWithoutRandom(message600, img1)
        write_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom600.bmp", nr600)

        print("1500 characters message ...")
        print("Steganography rate :" + str((1500.0 / float(width * height * 3)) * 100) + "%")
        nr1500 = insertWithoutRandom(message1500, img1)
        write_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom1500.bmp", nr1500)

        print("3000 characters message ...")
        print("Steganography rate :" + str((3000.0 / float(width * height * 3)) * 100) + "%")
        nr3000 = insertWithoutRandom(message3000, img1)
        write_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom3000.bmp", nr3000)
        print("Finish insertion LSB classic")
        print()
        print("Starting insertion LSB random:")
        print("100 characters message ...")
        print("Steganography rate :" + str((100.0 / float(width * height * 3)) * 100) + "%")
        nr100 = insertWithRandom(message100, img1)
        write_img("examplesNoEncryption/insertionRandom/" + filename + "_random100.bmp", nr100)

        print("600 characters message ...")
        print("Steganography rate :" + str((600.0 / float(width * height * 3)) * 100) + "%")
        nr600 = insertWithRandom(message600, img1)
        write_img("examplesNoEncryption/insertionRandom/" + filename + "_random600.bmp", nr600)

        print("1500 characters message ...")
        print("Steganography rate :" + str((1500.0 / float(width * height * 3)) * 100) + "%")
        nr1500 = insertWithRandom(message1500, img1)
        write_img("examplesNoEncryption/insertionRandom/" + filename + "_random1500.bmp", nr1500)

        print("3000 characters message ...")
        print("Steganography rate :" + str((3000.0 / float(width * height * 3)) * 100) + "%")
        nr3000 = insertWithRandom(message3000, img1)
        write_img("examplesNoEncryption/insertionRandom/" + filename + "_random3000.bmp", nr3000)
        print("Finish insertion LSB random")
        print()
        print("Starting extraction of classic inserted images :")
        print("100 characters inserted image ...")
        imgnr100 = read_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom100.bmp")
        messageExtracted100 = extract(imgnr100)
        messageWrite(messageExtracted100, "examplesNoEncryption/messagesExtracted/" + filename + "_norandom100.txt")

        print("600 characters inserted image ...")
        imgnr600 = read_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom600.bmp")
        messageExtracted600 = extract(imgnr600)
        messageWrite(messageExtracted600, "examplesNoEncryption/messagesExtracted/" + filename + "_norandom600.txt")

        print("1500 characters inserted image ...")
        imgnr1500 = read_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom1500.bmp")
        messageExtracted1500 = extract(imgnr1500)
        messageWrite(messageExtracted1500, "examplesNoEncryption/messagesExtracted/" + filename + "_norandom1500.txt")

        print("3000 characters inserted image ...")
        imgnr3000 = read_img("examplesNoEncryption/insertionNoRandom/" + filename + "_norandom3000.bmp")
        messageExtracted3000 = extract(imgnr3000)
        messageWrite(messageExtracted3000, "examplesNoEncryption/messagesExtracted/" + filename + "_norandom3000.txt")
        print("Finish classic inserted images extraction")
        print()
        print("Starting extraction of random inserted images :")
        print("100 characters inserted image ...")
        imgr100 = read_img("examplesNoEncryption/insertionRandom/" + filename + "_random100.bmp")
        messageExtracted100 = extract(imgr100)
        messageWrite(messageExtracted100, "examplesNoEncryption/messagesExtracted/" + filename + "_random100.txt")

        print("600 characters inserted image ...")
        imgr600 = read_img("examplesNoEncryption/insertionRandom/" + filename + "_random600.bmp")
        messageExtracted600 = extract(imgr600)
        messageWrite(messageExtracted600, "examplesNoEncryption/messagesExtracted/" + filename + "_random600.txt")

        print("1500 characters inserted image ...")
        imgr1500 = read_img("examplesNoEncryption/insertionRandom/" + filename + "_random1500.bmp")
        messageExtracted1500 = extract(imgr1500)
        messageWrite(messageExtracted1500, "examplesNoEncryption/messagesExtracted/" + filename + "_random1500.txt")

        print("3000 characters inserted image ...")
        imgr3000 = read_img("examplesNoEncryption/insertionRandom/" + filename + "_random3000.bmp")
        messageExtracted3000 = extract(imgr3000)
        messageWrite(messageExtracted3000, "examplesNoEncryption/messagesExtracted/" + filename + "_random3000.txt")
        print("Finish random inserted images extraction")

    if (args[1] == "examples" and args[2] == "encryption"):
        print("Running examples with encryption:")
        key = b'pvaIQQ4De6Qi-VwqLS1xNfa_Yh1WfMLuPB4LSBIz4n8='
        print("AES key :"+str(key))
        img1 = read_img(str(args[3]))
        height, width = len(img1), len(img1[0])
        print("Image "+str(args[3])+" ("+str(height)+"x"+str(width)+" pixels)")
        filename = getFileName(args[3])

        message100 = messageRead("messagesToInsert/message100.txt")
        message600 = messageRead("messagesToInsert/message600.txt")
        message1500 = messageRead("messagesToInsert/message1500.txt")
        message3000 = messageRead("messagesToInsert/message3000.txt")
        message100Encrypted = encryptAES(key, message100)
        message600Encrypted = encryptAES(key, message600)
        message1500Encrypted = encryptAES(key, message1500)
        message3000Encrypted = encryptAES(key, message3000)
        print()
        print("Starting insertion LSB classic:")
        print("100 characters message ...")
        #print("Encrypted message :" + message100Encrypted)
        print("Steganography rate :"+str((len(message100Encrypted)/float(width*height*3))*100)+"%")
        nr100 = insertWithoutRandom(message100Encrypted, img1)
        write_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom100.bmp", nr100)

        print("600 characters message ...")
        #print("Encrypted message :" + message600Encrypted)
        print("Steganography rate :" + str((len(message600Encrypted) / float(width * height * 3)) * 100) + "%")
        nr600 = insertWithoutRandom(message600Encrypted, img1)
        write_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom600.bmp", nr600)

        print("1500 characters message ...")
        #print("Encrypted message :" + message1500Encrypted)
        print("Steganography rate :" + str((len(message1500Encrypted) / float(width * height * 3)) * 100) + "%")
        nr1500 = insertWithoutRandom(message1500Encrypted, img1)
        write_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom1500.bmp", nr1500)

        print("3000 characters message ...")
        #print("Encrypted message :" + message3000Encrypted)
        print("Steganography rate :" + str((len(message3000Encrypted) / float(width * height * 3)) * 100) + "%")
        nr3000 = insertWithoutRandom(message3000Encrypted, img1)
        write_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom3000.bmp", nr3000)
        print("Finish insertion LSB classic")
        print()

        print("Starting insertion LSB random:")
        print("100 characters message ...")
        #print("Encrypted message :" + message100Encrypted)
        print("Steganography rate :" + str((len(message100Encrypted) / float(width * height * 3)) * 100) + "%")
        nr100 = insertWithRandom(message100Encrypted, img1)
        write_img("examplesEncryption/insertionRandom/"+filename+"_random100.bmp", nr100)

        print("600 characters message ...")
        #print("Encrypted message :" + message600Encrypted)
        print("Steganography rate :" + str((len(message600Encrypted) / float(width * height * 3)) * 100) + "%")
        nr600 = insertWithRandom(message600Encrypted, img1)
        write_img("examplesEncryption/insertionRandom/"+filename+"_random600.bmp", nr600)

        print("1500 characters message ...")
        #print("Encrypted message :" + message1500Encrypted)
        print("Steganography rate :" + str((len(message1500Encrypted) / float(width * height * 3)) * 100) + "%")
        nr1500 = insertWithRandom(message1500Encrypted, img1)
        write_img("examplesEncryption/insertionRandom/"+filename+"_random1500.bmp", nr1500)

        print("3000 characters message ...")
        #print("Encrypted message :" + message3000Encrypted)
        print("Steganography rate :" + str((len(message3000Encrypted) / float(width * height * 3)) * 100) + "%")
        nr3000 = insertWithRandom(message3000Encrypted, img1)
        write_img("examplesEncryption/insertionRandom/"+filename+"_random3000.bmp", nr3000)
        print("Finish insertion LSB random")
        print()

        print("Starting extraction of classic inserted images :")
        print("100 characters inserted image ...")
        imgnr100 = read_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom100.bmp")
        messageExtracted100 = extract(imgnr100)
        #print("Extracted string :" + messageExtracted100)
        messageDecrypted100 = decryptAES(key, messageExtracted100)
        messageWrite(messageDecrypted100, "examplesEncryption/messagesExtracted/"+filename+"_norandom100.txt")

        print("600 characters inserted image ...")
        imgnr600 = read_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom600.bmp")
        messageExtracted600 = extract(imgnr600)
        #print("Extracted string :" + messageExtracted600)
        messageDecrypted600 = decryptAES(key, messageExtracted600)
        messageWrite(messageDecrypted600, "examplesEncryption/messagesExtracted/"+filename+"_norandom600.txt")

        print("1500 characters inserted image ...")
        imgnr1500 = read_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom1500.bmp")
        messageExtracted1500 = extract(imgnr1500)
        #print("Extracted string :" + messageExtracted1500)
        messageDecrypted1500 = decryptAES(key, messageExtracted1500)
        messageWrite(messageDecrypted1500, "examplesEncryption/messagesExtracted/"+filename+"_norandom1500.txt")

        print("3000 characters inserted image ...")
        imgnr3000 = read_img("examplesEncryption/insertionNoRandom/"+filename+"_norandom3000.bmp")
        messageExtracted3000 = extract(imgnr3000)
        #print("Extracted string :" + messageExtracted3000)
        messageDecrypted3000 = decryptAES(key, messageExtracted3000)
        messageWrite(messageDecrypted3000, "examplesEncryption/messagesExtracted/"+filename+"_norandom3000.txt")
        print("Finish classic inserted images extraction")
        print()

        print("Starting extraction of random inserted images :")
        print("100 characters inserted image ...")
        imgr100 = read_img("examplesEncryption/insertionRandom/"+filename+"_random100.bmp")
        messageExtracted100 = extract(imgr100)
        #print("Extracted string :" + messageExtracted100)
        messageDecrypted100 = decryptAES(key, messageExtracted100)
        messageWrite(messageDecrypted100, "examplesEncryption/messagesExtracted/"+filename+"_random100.txt")

        print("600 characters inserted image ...")
        imgr600 = read_img("examplesEncryption/insertionRandom/"+filename+"_random600.bmp")
        messageExtracted600 = extract(imgr600)
        #print("Extracted string :" + messageExtracted600)
        messageDecrypted600 = decryptAES(key, messageExtracted600)
        messageWrite(messageDecrypted600, "examplesEncryption/messagesExtracted/"+filename+"_random600.txt")

        print("1500 characters inserted image ...")
        imgr1500 = read_img("examplesEncryption/insertionRandom/"+filename+"_random1500.bmp")
        messageExtracted1500 = extract(imgr1500)
        #print("Extracted string :" + messageExtracted1500)
        messageDecrypted1500 = decryptAES(key, messageExtracted1500)
        messageWrite(messageDecrypted1500, "examplesEncryption/messagesExtracted/"+filename+"_random1500.txt")

        print("3000 characters inserted image ...")
        imgr3000 = read_img("examplesEncryption/insertionRandom/"+filename+"_random3000.bmp")
        messageExtracted3000 = extract(imgr3000)
        #print("Extracted string :" + messageExtracted3000)
        messageDecrypted3000 = decryptAES(key, messageExtracted3000)
        messageWrite(messageDecrypted3000, "examplesEncryption/messagesExtracted/"+filename+"_random3000.txt")
        print("Finish random inserted images extraction")

    if(args[1] == "curves"):
        listOfFileName = ["BMP/canyon.bmp", "BMP/canyon2.bmp", "BMP/foret.bmp", "BMP/mer.bmp",
                          "BMP/monument.bmp", "BMP/porte.bmp", "BMP/reflet.bmp",
                          "BMP/sky.bmp", "BMP/tableau.bmp", "BMP/tableau2.bmp", "BMP/tournesol.bmp",
                          "BMP/vache.bmp", "BMP/vague.bmp", "BMP/ciel.bmp", "BMP/sol.bmp",
                          "BMP/sortie.bmp", "BMP/hosto.bmp", "BMP/banlieue.bmp", "BMP/dame.bmp",
                          "BMP/cafe.bmp", "BMP/arbre2.bmp","BMP/coin.bmp","BMP/maison.bmp",
                          "BMP/photo.bmp", "BMP/pinceau.bmp"]

        listOfFileName2 = ["roc/ImagesStega/canyon_norandom.bmp", "roc/ImagesStega/canyon2_norandom.bmp",
                           "roc/ImagesStega/foret_norandom.bmp", "roc/ImagesStega/mer_norandom.bmp",
                           "roc/ImagesStega/monument_norandom.bmp", "roc/ImagesStega/porte_norandom.bmp",
                           "roc/ImagesStega/reflet_norandom.bmp", "roc/ImagesStega/sky_norandom.bmp",
                           "roc/ImagesStega/tableau_norandom.bmp", "roc/ImagesStega/tableau2_norandom.bmp",
                           "roc/ImagesStega/tournesol_norandom.bmp", "roc/ImagesStega/vache_norandom.bmp",
                           "roc/ImagesStega/vague_norandom.bmp", "roc/ImagesStega/ciel_norandom.bmp",
                           "roc/ImagesStega/sol_norandom.bmp", "roc/ImagesStega/sortie_norandom.bmp",
                           "roc/ImagesStega/hosto_norandom.bmp", "roc/ImagesStega/banlieue_norandom.bmp",
                           "roc/ImagesStega/cafe_norandom.bmp", "roc/ImagesStega/dame_norandom.bmp",
                           "roc/ImagesStega/arbre2_norandom.bmp", "roc/ImagesStega/coin_norandom.bmp",
                           "roc/ImagesStega/maison_norandom.bmp", "roc/ImagesStega/photo_norandom.bmp",
                           "roc/ImagesStega/pinceau_norandom.bmp"]

        message100 = messageRead("messagesToInsert/message100.txt")
        message600 = messageRead("messagesToInsert/message600.txt")
        message1500 = messageRead("messagesToInsert/message1500.txt")
        message3000 = messageRead("messagesToInsert/message3000.txt")
        message10000 = messageRead("messagesToInsert/message10000.txt")

        massiveInsertionWithoutRandom(listOfFileName, None, message100)
        massiveExtractionWithoutRandom(listOfFileName, None)

        constructROCCurve(listOfFileName, listOfFileName2, 0.22, "roc/curves/curveROC0_22.png")

        massiveInsertionWithoutRandom(listOfFileName, None, message600)
        massiveExtractionWithoutRandom(listOfFileName, None)

        constructROCCurve(listOfFileName, listOfFileName2, 1.33, "roc/curves/curveROC1_33.png")

        massiveInsertionWithoutRandom(listOfFileName, None, message1500)
        massiveExtractionWithoutRandom(listOfFileName, None)

        constructROCCurve(listOfFileName, listOfFileName2, 3.33, "roc/curves/curveROC3_33.png")

        massiveInsertionWithoutRandom(listOfFileName, None, message3000)
        massiveExtractionWithoutRandom(listOfFileName, None)

        constructROCCurve(listOfFileName, listOfFileName2, 6.66, "roc/curves/curveROC6_66.png")

        massiveInsertionWithoutRandom(listOfFileName, None, message10000)
        massiveExtractionWithoutRandom(listOfFileName, None)

        constructROCCurve(listOfFileName, listOfFileName2, 22.22, "roc/curves/curveROC22_22.png")

    if(args[1] == "clear"):
        clearDirectory("examplesEncryption/insertionNoRandom")
        clearDirectory("examplesEncryption/insertionRandom")
        clearDirectory("examplesEncryption/messagesExtracted")
        clearDirectory("examplesNoEncryption/insertionNoRandom")
        clearDirectory("examplesNoEncryption/insertionRandom")
        clearDirectory("examplesNoEncryption/messagesExtracted")
        clearDirectory("roc/ImagesStega")
        clearDirectory("roc/messagesExtracted")
        clearDirectory("roc/curves")


"""
Gives usage of how run the script
"""
def usage():
    print("To run examples without encryption, run the following command")
    print("      python tpLSB.py examples noencryption <pathToImage>")
    print("To run examples with encryption, run the following command")
    print("      python tpLSB.py examples encryption <pathToImage>")
    print("To create ROC curves, according to three different steganographic rates, run the following command")
    print("      python tpLSB.py curves")
    print("To clear directories where files could have been added, run the following command")
    print("      python tpLSB.py clear")


"""
Deletes all the files of a directory
path : path of the directory
"""
def clearDirectory(path):
    filelist = [f for f in os.listdir(path)]
    for f in filelist:
        os.remove(os.path.join(path, f))



if __name__ == '__main__':
    main()