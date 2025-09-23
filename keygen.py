#!/usr/bin/python

from os import stat
from os.path import isfile
from utilities import try_install, display_error_message

try:
	from Crypto.Cipher import AES
	from Crypto.Random import get_random_bytes
except ImportError as ie:
	display_error_message("pycryptodome")


class KeyGen:
	__key: str = None
	__cipher = None
	__tag = None
	__nonce = None

	_keyfile: str = "./i.bin"

	def __init__(self):
		if isfile(self._keyfile) and stat(self._keyfile).st_size > 0:
			try:
				with open(self._keyfile, "rb") as c:
					self.__key, self.__cipher, self.__tag, self.__nonce = c.readlines()

			except Exception as e:
				self.generate_key(16)
		else:
			self.generate_key(16)

	def generate_key(self, bytes: int = 16):
		tmp = get_random_bytes(bytes)
		self.__key = tmp
		
		with open(self._keyfile, "wb") as c:
			c.write(tmp)

	def decrypt(self, target: str):
		return self.__cipher.decrypt_and_verify(target, self.__tag, self.__nonce)

	def encrypt(self, target: str):
		self.__nonce = self.__cipher.nonce
		self.__cipher = AES.new(
			self.__key, 
			AES.MODE_EAX,
			self.__nonce
		)
		text, tag = self.__cipher.encrypt_and_digest(target)
		self.__tag = tag

		return text
