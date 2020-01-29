"""
" James Ryan
" Created: 19 Sep 19
"
" The purpose of the program is figure out the key which was used to encrypt a message based on it's plaintext and
" cyphertext. It is known that the encryption method aes-128-cbc was used, and that the key was an english word
" shorter than 16 characters
"
" Python3
" REQUIRES: pip -m install PyCryptodome
"""

# imports
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def crack_key(plain, cipher, iv):
    plain = plain.encode('utf-8')
    words = open("words.txt", "r")
    iv = bytes.fromhex(iv)

    while True:
        word = words.readline().strip('\n') # get next word from words.txt
        if word == '':
            break
        key = word[0:16].ljust(16, '#').encode('utf-8')
        cipher0 = AES.new(key, AES.MODE_CBC, iv)
        cipher1 = cipher0.encrypt(pad(plain, AES.block_size))
        if cipher == cipher1.hex():
            words.close()
            return word

        # print(cipher1.hex())
    words.close()
    return None


def main():
    print("Program Start\n"
          "=============\n")
    file = open("input.txt", "r")
    line1 = file.readline().strip('\n')
    line2 = file.readline().strip('\n')
    line3 = file.readline().strip('\n')
    line4 = file.readline().strip('\n')
    file.close()

    print("Input File:")
    print(line1)
    print(line2)
    print(line3)
    print(line4)
    plaintext = line1.split(': ')[1]
    print("\nPlaintext:\n{0}\n".format(plaintext))
    ciphertext = line2.split(': ')[1] + line3.strip(" ")
    print("Ciphertext:\n{0}\n".format(ciphertext))
    initialValue = line4.split(':         ')[1]
    print("Initial Value:\n{0}\n".format(initialValue))
    key = crack_key(plaintext, ciphertext, initialValue)
    if key is None:
        print("Key not found in list.\n")
    else:
        print("Key:\n   {0}\n".format(key))
    print("End of Program\n"
          "==============")


if __name__ == "__main__":
    main()
