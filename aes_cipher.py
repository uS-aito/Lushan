#coding: utf-8
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
		raw = self.__pad(raw)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(raw))

	def __decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self.__unpad(cipher.decrypt(enc[AES.block_size:]))

	def __pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	def __unpad(self, s):
		return s[:-ord(s[len(s)-1:])]
	
	def write_pass(self,fname="id-pass.txt"):
		sys.stdout.write("ID: ")
		id = self.__encrypt(raw_input())
		ps = self.__encrypt(getpass())
		with open(fname,"w") as wfp:
			wfp.write(id+"\n")
			wfp.write(ps+"\n")

	def read_pass(self,fname="id-pass.txt"):
		with open(fname,"r") as rfp:
			id = self.__decrypt(rfp.readline())
			ps = self.__decrypt(rfp.readline())
		return (id,ps)

if __name__ == "__main__":
	sys.stdout.write("Master ")
	aesc = AESCipher(getpass())
	
	sys.stdout.write("Input id-pass file name[id-pass.txt]")
	fname = raw_input()
	if fname == "":
		fname="id-pass.txt"

	aesc.write_pass(fname)
	id, ps = aesc.read_pass(fname)
	print id
	print ps