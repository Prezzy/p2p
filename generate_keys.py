import os
from jwcrypto import jwk
from sslib import shamir
from patetokens import NistKey
import json


idxs = ['1', '2']

def main():

    token_key = jwk.JWK.generate(kty='RSA', size=2048)

    key = NistKey.FullKey(idxs)
    key.generate_key()
    print(key.x)
    key.split_sk()
    key.gen_ver_pks()

    with open("token_key.txt", "w") as file:
        file.write(token_key.export())

    with open("token_public_key.txt", "w") as file:
        file.write(token_key.export_public())

    with open("ver_keys_for_user.txt", "w") as file:
        file.write(json.dumps(key.export_keys(False)))

    for idx in idxs:
        veri_key = key.export_veri_key(idx)
        print("VERI KEYS")
        print(veri_key)
        with open("veri_key_{}".format(idx), "w") as file:
            file.write(json.dumps(veri_key))

main()
