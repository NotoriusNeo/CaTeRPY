# CaTeRPY
A python script to recursively encrypt/decrypt folders with AES-CTR, using the pycryptodome and bcrypt libraries.

## Disclaimer / Here be dragons!
!! Things may not work as intended !!

This tool was developed to learn more about encryption/decryption and how it works in Python.
You are the sole responsible and liable to any damage by the usage of this tool.
Please ensure you have a backup of your data before proceeding!

# Usage
This tool was built with python3.11 in mind but may run in lower versions. 

It requires pycryptodome and bcrypt to be installed!

``pip install pycryptodome``

``pip install bcrypt``

### To encrypt
``python3.11 CaTeR.PY -e -p <password> -s <salt file name> <path of folder to encrypt> <output path>``

### To decrypt
``python3.11 CaTeR.PY -d -p <password> -s <salt file name> <path of folder to decrypt> <output path>``
