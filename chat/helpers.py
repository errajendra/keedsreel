from Crypto.Cipher import AES
import base64
from django.conf import settings


def encrypt_message(message):
    key = settings.ENCRYPTION_KEY[:32]
    # Pad the message to a multiple of 16 bytes
    padded_message = message + ((16 - len(message) % 16) * chr(16 - len(message) % 16))
    
    # Convert the key and message to bytes
    key = bytes(key.encode('utf-8'))
    padded_message = bytes(padded_message.encode('utf-8'))
    
    # Create the AES cipher
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Encrypt the message
    encrypted_message = cipher.encrypt(padded_message)
    
    # Encode the encrypted message as base64
    encoded_message = base64.b64encode(encrypted_message)
    
    return encoded_message


def decrypt_message(encoded_message):
    key = settings.ENCRYPTION_KEY[:32]
    # Convert the key and encoded message to bytes
    key = bytes(key.encode('utf-8'))
    encoded_message = base64.b64decode(encoded_message)
    
    # Create the AES cipher
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Decrypt the message
    decrypted_message = cipher.decrypt(encoded_message)
    
    # Remove padding from the decrypted message
    unpadded_message = decrypted_message[:-ord(decrypted_message[-1:])]
    
    # Decode the decrypted message as a string
    message = unpadded_message.decode('utf-8')
    
    return message
