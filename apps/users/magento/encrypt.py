from base64 import b64encode, b64decode
from nacl.bindings import crypto_aead_chacha20poly1305_ietf_encrypt, crypto_aead_chacha20poly1305_ietf_decrypt
from nacl.utils import random as nacl_random
from django.conf import settings
import hashlib

class MagentoEncryptor:
    def __init__(self):
        """
        Initialize the MagentoEncryptor with the secret key, key version, and cipher type.
        The key is used for encryption, key_version is the version of the key, and cipher_type is the encryption type.
        """
        # Retrieve the key from settings
        self.key = settings.MAGENTO_ENCRYPT_KEY

        # Ensure the key is in bytes format
        if isinstance(self.key, str):
            # If the key is base64-encoded, decode it
            if self.key.startswith('base64'):
                self.key = b64decode(self.key[7:])  # Remove 'base64' prefix and decode
            else:
                # Convert the key to bytes (e.g., using UTF-8 encoding)
                self.key = self.key.encode('utf-8')

        # Derive a 32-byte key using the same method as Magento (assume SHA-256)
        if len(self.key) != 32:
            self.key = hashlib.sha256(self.key).digest()

        # At this point, the key is guaranteed to be 32 bytes
        assert len(self.key) == 32, "Key must be 32 bytes long for ChaCha20-Poly1305 encryption."

        self.key_version = '0'
        self.cipher_type = '3'

    def encrypt(self, data):
        """
        Encrypts the data using ChaCha20-Poly1305, compatible with Magento's encryption.

        :param data: The data to encrypt (string or bytes).
        :return: The formatted encrypted data (string) in Magento's format.
        """
        # Ensure data is a bytes object
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes if needed

        # Generate a random nonce (12 bytes for ChaCha20-Poly1305 IETF)
        nonce = nacl_random(12)

        # Encrypt the data using ChaCha20-Poly1305
        cipher_text = crypto_aead_chacha20poly1305_ietf_encrypt(
            data,  # Data is already in bytes
            nonce,  # Nonce is also used as additional data
            nonce,  # Nonce is also used as additional data
            self.key  # Secret key
        )

        # Combine nonce and ciphertext
        nonce_and_cipher_text = nonce + cipher_text

        # Encode the result in base64
        encrypted_data_base64 = b64encode(nonce_and_cipher_text).decode()

        # Format the encrypted data to match Magento's output format with a dynamic cipher type
        magento_format = f"{self.key_version}:{self.cipher_type}:{encrypted_data_base64}"

        return magento_format

    def decrypt(self, encrypted_data):
        """
        Decrypts the data encrypted using Magento's encryption mechanism.

        :param encrypted_data: The formatted encrypted data (string) in Magento's format.
        :return: The decrypted data (string).
        """
        # Strip any whitespace or newline characters that could cause padding issues
        encrypted_data = encrypted_data.strip()

        # Remove Magento format prefix "key_version:cipher_type:"
        parts = encrypted_data.split(":", 2)
        if len(parts) != 3 or parts[1] != self.cipher_type:
            raise ValueError("Invalid encrypted data format.")

        encrypted_data_base64 = parts[2]

        # Decode the base64-encoded data
        nonce_and_cipher_text = b64decode(encrypted_data_base64)

        # Extract the nonce (first 12 bytes) and the encrypted message
        nonce = nonce_and_cipher_text[:12]
        cipher_text = nonce_and_cipher_text[12:]

        try:
            # Decrypt the message using ChaCha20-Poly1305
            decrypted_data = crypto_aead_chacha20poly1305_ietf_decrypt(
                cipher_text,  # Encrypted message
                nonce,  # Nonce as additional data
                nonce,  # Nonce used during encryption
                self.key  # Secret key
            ).decode()
            return decrypted_data
        except Exception as e:
            # Handle decryption errors
            print(f"Decryption failed: {e}")
            return None
