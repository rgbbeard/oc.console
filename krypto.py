#!/usr/bin/python

import base64
from os.path import isfile, dirname
from utilities import (
    printerr,
    printalr,
    printinf,
    printsuc,
    import_module_error
)

try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    import_module_error("pycryptodome")

BASE = dirname(__file__)


class Krypto:
    _storage_file: str
    
    _key = None
    _iv = None

    _preloaded_conf: bool = False

    def __init__(self, storage_file="i.bin"):
        self._storage_file = f"{BASE}/{storage_file}"

        if isfile(self._storage_file):
            printinf("Found encryption file")

            self._load()
        else:
            printinf("Ecryption file not found, generating one...")

            self._key = get_random_bytes(16)
            self._iv = get_random_bytes(16)

            # Generate a i.bin file to use for future ecryptions
            self.encrypt("")

            printinf(f"File is: {storage_file}")

    def _save(self):
        with open(self._storage_file, "wb") as f:
            for item in [self._key, self._iv]:
                f.write(item + b"\n")

    # Generate and save key, nonce and tag
    def _load(self):
        with open(self._storage_file, "rb") as f:
            lines = f.read().splitlines()

        if len(lines) < 1:
            raise ValueError("Ecryption file corrupted: missing key")

        self._key = lines[0]

        if len(lines) == 2:
            self._iv = lines[1]

        self._preloaded_conf = True

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()

        cipher = AES.new(self._key, AES.MODE_CBC, self._iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))

        # Save key and iv only on the first encryption
        if not self._preloaded_conf:
            self._save()

        self._load()

        return ciphertext

    def decrypt(self, data):
        if isinstance(data, str):
            data = data.encode()

        if None in (self._key, self._iv):
            raise ValueError("Missing key or iv, cannot decrypt")

        cipher = AES.new(self._key, AES.MODE_CBC, iv=self._iv)
        plaintext = unpad(cipher.decrypt(data), AES.block_size)

        return plaintext
