from decouple import config
from Crypto.Cipher import AES
import base64

SECRET_KEY = config('SECRET_KEY')
print("Decryption SECRET_KEY:", SECRET_KEY)


def decrypt_password(encrypted_password):
    try:
        # Decode the Base64-encoded encrypted password
        print("Decryption SECRET_KEY:", SECRET_KEY)

        encrypted_password_bytes = base64.b64decode(encrypted_password)
        print('encrypted', encrypted_password)
        # Create an AES cipher object with the secret key
        cipher = AES.new(SECRET_KEY.encode("utf-8"), AES.MODE_ECB)
        print('cipher', cipher)
        # Decrypt the password
        decrypted_bytes = cipher.decrypt(encrypted_password_bytes)
        print('decrypte_byte', decrypted_bytes)
        # Remove PKCS#7 padding
        pad_length = decrypted_bytes[-1]
        decrypted_password = decrypted_bytes[:-pad_length].decode("utf-8")
        print('decryptpass', decrypted_password)
        return decrypted_password
    except Exception as e:
        print("Decryption error:", e)
        raise ValueError("Invalid encryption or key mismatch")
