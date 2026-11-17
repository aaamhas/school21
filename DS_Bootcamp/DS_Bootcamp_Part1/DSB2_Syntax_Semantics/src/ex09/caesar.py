import sys

def encode(sentence, num):
    new_sentence = ''
    for letter in sentence:
        if letter.isalpha():
            if letter.isupper():
                new_letter = chr((ord(letter)+num-65)%26+65)
            else:
                new_letter = chr((ord(letter)+num-97)%26+97)
        else:
            new_letter = letter
        new_sentence += new_letter
    return new_sentence

def decode(sentence, num):
    new_sentence = ''
    for letter in sentence:
        if letter.isalpha():
            if letter.isupper(): 
                new_letter = chr((ord(letter)-num-65)%26+65)
            else:
                new_letter = chr((ord(letter)-num-97)%26+97)
        else:
            new_letter = letter
        new_sentence += new_letter
    return new_sentence

def has_cyrillic(sentence):
    for char in sentence:
        if 'а' <= char.lower() <= 'я' or char.lower() == 'ё':
            return True
    return False

def process():
    s = sys.argv
    if len(s) != 4:
        raise ValueError("ошибка")
    comand = s[1]
    sentence = s[2]
    num = int(s[3])
    if has_cyrillic(sentence):
        raise ValueError("The script does not support your language yet.")
    else:
        if comand == 'encode':
            print(encode(sentence, num))
        elif comand == 'decode':
            print(decode(sentence, num))
        else:
            raise ValueError("ошибка")
    
if __name__ == '__main__':
    process()