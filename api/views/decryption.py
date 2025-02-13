from decouple import config
from Crypto.Cipher import AES
import base64

SECRET_KEY = config('SECRET_KEY')


def decrypt_password(encrypted_password):
    try:
        encrypted_password_bytes = base64.b64decode(encrypted_password)
       
        cipher = AES.new(SECRET_KEY.encode("utf-8"), AES.MODE_ECB)
        
        decrypted_bytes = cipher.decrypt(encrypted_password_bytes)
        
        pad_length = decrypted_bytes[-1]
        decrypted_password = decrypted_bytes[:-pad_length].decode("utf-8")
        
        return decrypted_password
    except Exception as e:
        # print("Decryption error:", e)
        raise ValueError("Invalid encryption or key mismatch")
