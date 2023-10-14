import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import database.models.models as DbUserModels
from config.config import Settings

aes_key = Settings().AES_KEY

def encrypt(raw):
        raw = pad(raw.encode(),16)
        cipher = AES.new(aes_key.encode('utf-8'), AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

def decrypt(enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(aes_key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16)