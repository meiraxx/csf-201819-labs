from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
import sys
import argparse
import os
import binascii

# =====================
#     CLI OPTIONS
# =====================

op = argparse.ArgumentParser(description='AES_CTR custom CSF file decryptor!!')
op.add_argument('files', metavar='files', nargs='+', help='the file to decrypt')
op.add_argument('-o', '--out-dir', help="output dir", dest='outdir')
args = op.parse_args()

def decrypt_stealth_auth(content, authentication_cookie):
    # byte 1 = authentication type, 2-17 = input vector, 18 on = encrypted content
    iv, encrypted = content[1:17], content[17:]
    counter = Counter.new(128, initial_value = bytes_to_long(iv))
    cipher = AES.new(authentication_cookie, AES.MODE_CTR, counter = counter)

    return cipher.decrypt(encrypted) 

encrypted_file = args.files[0]
decrypted_file_name = os.path.basename(encrypted_file).replace(".encrypted","")
outdir = args.outdir
if not os.path.exists(outdir):
	os.mkdir(outdir)
outfile = outdir + os.sep + decrypted_file_name

# secret key can be an argument for this program instead, but is hardcoded for this project
secret_key = binascii.unhexlify("47683b9a9663c065353437b35c5d8519")


# Encryption 	(not appliable here)
#plain_text_original = "something secret"
#encryption_ctr = Counter.new(128)
#encryption_suite = AES.new(secret_key, AES.MODE_CTR, counter = encryption_ctr)
#cipher_text = encryption_suite.encrypt(plain_text_original)

f1 = open(encrypted_file, "rb")

result = ""
first_16 = long(binascii.hexlify(f1.read(16)),16)
decryption_ctr = Counter.new(128, initial_value=first_16)
decryptor = AES.new(secret_key, AES.MODE_CTR, counter = decryption_ctr)
data = f1.read(16)
while data:
	# Decryption
	# first 16 bytes (128 bits) is the initial value, other data is after...
	result += decryptor.decrypt(data)
	data=f1.read(16)

f1.close()
f2 = open(outfile, "w")
f2.write(result)
f2.close()
