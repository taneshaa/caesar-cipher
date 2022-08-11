from curses import keyname
from distutils.dep_util import newer_pairwise
from corpus_loader import word_list, name_list
import enum


alphabet = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i', 10: 'j', 11: 'k',
            12: 'l', 13: 'm', 14: 'n', 15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 's', 20: 't', 21: 'u', 22: 'v', 23: 'w', 24: 'x', 25: "y", 26: 'z'}

Uppercase = [x.upper() for x in alphabet.values()]
Lowercase = [x.lower() for x in alphabet.values()]


def encrypt(sentence, key):
    encrypted = ""
    for letter in sentence:
        if letter in Uppercase + Lowercase:
            temp = list(alphabet.keys())[
                list(alphabet.values()).index(letter.lower())] + key
            if temp > 26:
                temp %= 26
            if temp <= -1:
                temp += 26
        if letter in Uppercase:
            encrypted += alphabet[abs(temp)].upper()
        elif letter in Lowercase:
            encrypted += alphabet[abs(temp)].lower()
        else:
            encrypted += letter
    return encrypted


def decrypt(sentence, key):
    return encrypt(sentence, -key)


def crack(encrypted_str, percent=0.8):
    words = encrypted_str.split(" ")
    deciphered = []
    key = []
    for word in words:
        for j in range(1, 26):
            new_word = ""
            search_word = ""
            for i, letter in enumerate(word):
                if letter in Uppercase + Lowercase:
                    temp = list(alphabet.keys())[
                        list(alphabet.values()).index(letter.lower())] + j
                    if temp > 26:
                        temp %= 26
                    new_word += alphabet[abs(temp)]
                    search_word += alphabet[abs(temp)]
                else:
                    new_word += letter
            if search_word in word_list + name_list and len(search_word) > 1:
                deciphered.append(new_word)
    if len(deciphered) > 0 and len(words)/len(deciphered) > 0.2:
        for word in deciphered:
            for j in range(1, 26):
                new_word = ""
                for i, letter in enumerate(word):
                    if letter in Uppercase + Lowercase:
                        temp = list(alphabet.keys())[
                            list(alphabet.values()).index(letter.lower())] + j
                        if temp > 26:
                            temp %= 26
                        new_word += alphabet[abs(temp)]
                    else:
                        new_word += letter
                if new_word in words:
                    length = list(alphabet.keys())[
                        list(alphabet.values()).index(new_word[0].lower())]
                    length1 = list(alphabet.keys())[
                        list(alphabet.values()).index(word[0].lower())]
                    if length - length1 < 0:
                        key.append((length + 26) - length1)
                    else:
                        key.append(length - length1)
        if len(key) and len(key)/len(deciphered) > percent:
            return decrypt(encrypted_str, most_frequent(key))
    return ""


def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


if __name__ == "__main__":
    harry_potter = """
    Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal, thank you very much. They were the last people you'd expect to be involved in anything strange or mysterious, because they just didn't hold with such nonsense. Mr. Dursley was the director of a fi rm called Grunnings, which made drills. He was a big, beefy man with hardly any neck, although he did have a very large mustache.
    """
    harry_potter_encrpted = """
    Wb. kxn Wbc. Nebcvoi, yp xewlob pyeb, Zbsfod Nbsfo, gobo zbyen dy cki drkd droi gobo zobpomdvi xybwkv, drkxu iye fobi wemr. Droi gobo dro vkcd zoyzvo iye'n ohzomd dy lo sxfyvfon sx kxidrsxq cdbkxqo yb wicdobsyec, lomkeco droi tecd nsnx'd ryvn gsdr cemr xyxcoxco. Wb. Nebcvoi gkc dro nsbomdyb yp k ps bw mkvvon Qbexxsxqc, grsmr wkno nbsvvc. Ro gkc k lsq, loopi wkx gsdr rkbnvi kxi xomu, kvdryeqr ro nsn rkfo k fobi vkbqo wecdkmro.
    """
    print("\n")
    print("** This app encrypts, decrypts a nessage as well as crack an encrpted code using Cesar's Cipher **")
    print("** Here's an example using a passage from Harry Potter **")
    print("\n")
    print("** Encryted **\n",  encrypt(harry_potter, 10))
    print("** Decrypted **\n", decrypt(harry_potter_encrpted, 10))
    print("\nDecoding...\n")
    print("** Cracked code **\n", crack(harry_potter_encrpted, 0.6))
    decode = input(
        "It's your turn, enter an encrypted message or press enter to quit:\n\n")
    if decode:
        print("\n** Cracked code **\n\n", crack(decode, 0.2))
    print("\n\n** Thank you for using this app! **")
