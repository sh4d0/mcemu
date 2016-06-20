import keyring
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

# Convuluted password obfuscation technique
# uses RSA (priv/pub) to encrypt a password used for a servce
# RSA private key is stored in users' keyring - should be "difficult" to retrieve
# Keyfile contains password encrypted with users' public key
# password protected by private key, private key stored in keyring


def main(argv):
    encrypt = argv[0]
    keyfile = argv[1]
    service = argv[2]
    username = argv[3]

    if isinstance(encrypt, str):
        if encrypt.lower().startswith('t'):
            encrypt = True
        else:
            encrypt = False

    if encrypt:
        password = argv[4]
        key = RSA.generate(1024)
        cipher = PKCS1_v1_5.new(key)

        keyring.set_password(service, username, key.exportKey())

        with open(keyfile, 'wb') as outf:
            outf.write(cipher.encrypt(password))
    else:
        key = RSA.importKey(keyring.get_password(service, username))
        cipher = PKCS1_v1_5.new(key)

        with open(keyfile, 'rb') as inf:
            return cipher.decrypt(inf.read(), None)


if __name__ == '__main__':
    main(sys.argv[1:])
