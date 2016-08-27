import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from getpass import getpass
import sys


class AESCipher(object):
    def __init__(self, key, block_size=32):
        self.key = hashlib.md5(key).hexdigest()
        self.bs = block_size

    def __encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def __decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def __pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def __unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
    
    def write_pass(self):
        sys.stdout.write("Master ")
        cipher = AESCipher(getpass())
        sys.stdout.write("ID: ")
        id = raw_input()
        ciphered = cipher.encrypt(getpass())

if __name__ == "__main__":
    print id
    print ciphered
