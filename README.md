# CSPRNG-project

This project focuses on stream cipher encryption and decryption using BBS and LCG to generate the random keystreams. `cipher.py` contains all the code, and can be called from the command line. Also note that the LCG and BBS params are initialized randomly so you can't expect to get the same encrypted text each time.

## Usage instructions:

usage: `cipher.py [-h] --key KEY [--plaintext PLAINTEXT]`

`plaintext` defaults to `Hello, Stream Cipher!`

ex:

```
$ python cipher.py --key testkey123 --plaintext "some test plaintext"
Encrypted BBS: rnme uert plaioudyu
Encrypted LCG: }f}js:h
^&#bs@S
Decrypted BBS: some test plaintext
Decrypted LCG: some test plaintext

$ python cipher.py --key hello --plaintext "some test plaintext"
Encrypted BBS: some!tdsu pmaioteyu
Encrypted LCG: fx<@_)6qh}:7PjW0
Decrypted BBS: some test plaintext
Decrypted LCG: some test plaintext

$ python cipher.py --key hello
Encrypted BBS: Idmmo- Sure`l!Bipidr
Encrypted LCG: Lm$$)PFP_MdIgbj3
Decrypted BBS: Hello, Stream Cipher!
Decrypted LCG: Hello, Stream Cipher!
```
