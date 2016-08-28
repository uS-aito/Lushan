#coding: utf-8
import imaplib
import email
from datetime import datetime,timedelta
from aes_cipher import AESCipher
from getpass import getpass

class gmailer(object):
	def __init__(self):
		cipher = AESCipher(getpass())
		try:
			id,ps = cipher.read_pass("gmail-id-pass.txt")
		except:
			print "Cannot read id-pass.txt"
			exit()

		try:
			self.gmail = imaplib.IMAP4_SSL("imap.gmail.com")
			self.gmail.login(id,ps)
		except:
			print "Login Failed."
			return

	def get_inbox(self):
		self.gmail.select("INBOX")

	def get_unseen(self):
		self.typ, self.data = self.gmail.search(None,"(UNSEEN)")
	
	def get_mailheaders(self,num=5):
		if self.typ != "OK" or self.data == "":
			print "ERROR: Invalid typ or data"
			return
		self.data = self.data[0].split()
		self.data.reverse()
		result_list = []
		for mid in self.data[:num]:
			result, d = self.gmail.fetch(mid,"(RFC822)")
			raw_email = d[0][1]
			tmp = []
			tmp.append(mid)
			try:
				msg = email.message_from_string(raw_email.decode("utf-8"))
				msg_encoding = "UTF-8" #email.Header.decode_header(msg.get('Subject'))[0][1] or 'iso-2022-jp'
				msg = email.message_from_string(raw_email.decode(msg_encoding))
				#print msg.keys()

				try:
					fromObj = email.Header.decode_header(msg.get("From"))
					addr = ""
					for f in fromObj:
						if isinstance(f[0],bytes):
							addr += f[0].decode(msg_encoding)
						else:
							addr += f[0]
				except:
					addr = ""
				tmp.append(addr)
				try:
					dateObj = email.Header.decode_header(msg.get("Date"))
					date = self.__date_decode(dateObj)
				except:
					date = ""
				tmp.append(date)
				result_list.append(tmp)
			except:
				"ERROR: Message encode error"
		print result_list
		return result_list

	def get_body(self,mid):
		result, d = self.gmail.fetch(mid,"(RFC822)")
		body = ""
		raw_email = d[0][1]
		try:
			msg = email.message_from_string(raw_email.decode("utf-8"))
			msg_encoding = "utf-8" #email.Header.decode_header(msg.get('Subject'))[0][1] or 'iso-2022-jp'
			msg = email.message_from_string(raw_email.decode(msg_encoding))
		except:
			"ERROR: Message encode error"
			return ""

		if msg.is_multipart():
			for payload in msg.get_payload():
				if payload.get_content_type() == "text/plain":
					body = payload.get_payload()
		else:
			if msg.get_content_type() == "text/plain":
				body = msg.get_payload()
		return body

	def __date_decode(self,date):
		mon_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
		date_list = date[0][0].split()[1:]
		time_list = date_list[3].split(":")
		decoded = datetime(int(date_list[2]), mon_list.index(date_list[1])+1, int(date_list[0]), int(time_list[0]), int(time_list[1]), int(time_list[2]))
		decoded = decoded - timedelta(hours=int(date_list[4][1:3]))
		return decoded

	def close(self):
		self.gmail.close()
		self.gmail.logout()

if __name__ == "__main__":
	gm = gmailer()
	try:
		gm.get_inbox()
		gm.get_unseen()
		header_list = gm.get_mailheaders()
		print "getbody"
		print gm.get_body(9651)
	finally:
		print "gm close"
		gm.close()
