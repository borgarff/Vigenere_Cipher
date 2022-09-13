import string
from collections import Counter
from math import sqrt

# Letters freqency from A-Z in the english alphabeth
letterFrequency = [0.08167,0.01492,0.02782, 0.04253,0.12702,0.02228,0.02015,0.06094,0.06966,0.00153,0.00772,0.04025,0.02406,0.06749,0.07507,0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.0236,0.0015,0.01974,0.00074]

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# initializing string 
ciperfile = open("ciphertext.txt", "r")
ciphertext = ciperfile.read().replace(' ', '')
ciperfile.close()

# Length of ther cipher
count = len(ciphertext)

# Find the Index of convinience for the given string
def IOC(text):
    freqsum = 0.0
    total = 0
    freq = Counter(text)

    for i in alphabet:
        freqsum += freq[i] * (freq[i] - 1)
        total += freq[i]

    return(freqsum / (total * (total-1)))

# Checks if the string is monoalphabetic of polyalphabetic
# Finds the key lenght
def checkAverage():
    keyLenght = 1
    average = 0.0
    lists = [""]
    while average < 0.06:
        lists = [""]
        average = 0.0
        current = 0
        for i in range(keyLenght):
            lists.append("")
        keyLenght += 1


        for j in range(count):
            lists[current] += ciphertext[j]
            current += 1
            if current == keyLenght:
                current = 0

        for k in range(keyLenght):
            average += IOC(lists[k])
        average = average / keyLenght
    return keyLenght, lists

def vector(x,y):
    num = 0
    lenX = 0
    lenY = 0
    for i in range(len(x)):
        lenX += x[i]*x[i]
        lenY += y[i]*y[i]
        num += x[i]*y[i]
    return num / sqrt(lenX*lenY)

# Finds the keyword baised on statistics (Good for longer ciphers)
def findKey(keyLenght, lists):
    key = ""
    freq = []
    for i in range(keyLenght):
        freq.append([0]*26)

        for j in range(len(lists[i])):
            freq[i][alphabet.index(lists[i][j])] += 1
        
        for k in range(26):
            freq[i][k] = freq[i][k] / len(lists[i])

    # Checks the frequencies with a test-table
    for i in range(keyLenght):
        for j in range(26):
            testtable = freq[i][j:] + freq[i][:j]
            if vector(letterFrequency,testtable) > 0.9:
                key += alphabet[j]
    return key
    

# Decryption of the Vigenere cipher with known key
def decrypt(cText, key):
    planText = ""
    for i in range(len(cText)):
        x = (alphabet.index(cText[i]) - alphabet.index(key[i % len(key)])) % 26
        planText += alphabet[x]
    return(planText)

lenght, listLength = checkAverage()
key = findKey(lenght, listLength)
print("The keyword:", key)
plaintext = decrypt(ciphertext, key)
print("The plaintext:", plaintext)