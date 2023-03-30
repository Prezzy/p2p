import unittest
import json
from sslib import shamir
from patetokens import NistKey
from Crypto.Math._IntegerGMP import IntegerGMP as IntGMP

class TestSS(unittest.TestCase):
    def setUp(self):
        self.key = NistKey.FullKey(['1','2','3'])
        #self.key.generate_key()
        #self.key.split_sk()
        #self.key.gen_ver_pks()

        with open("ver_keys_for_user.txt", "r") as file:
            key_dict = file.read()
            self.key.from_json(json.loads(key_dict))

    def test_key_split(self):
        x_bytes = self.key.x.to_bytes()
        print("X")
        print(x_bytes)
        secrets = shamir.to_hex(shamir.split_secret(x_bytes, 3, 3, prime_mod=self.key.q))

        recovered = shamir.recover_secret(shamir.from_hex(secrets))

        print("recovered")
        print(recovered)

        recovered_gmp = IntGMP.from_bytes(recovered)
        temp = self.key.g.__pow__(recovered_gmp, self.key.p)
        self.assertTrue(self.key.y.__eq__(temp))
        self.assertEqual(x_bytes, recovered)

    def test_key_shares(self):

        key_1 = NistKey.DistributedKey()
        with open("veri_key_1", "r") as file:
            key_dict1 = file.read()
            key_1.from_json(json.loads(key_dict1))


        key_2 = NistKey.DistributedKey()
        with open("veri_key_2", "r") as file:
            key_dict2 = file.read()
            key_2.from_json(json.loads(key_dict2))

        key_3 = NistKey.DistributedKey()
        with open("veri_key_3", "r") as file:
            key_dict3 = file.read()
            key_3.from_json(json.loads(key_dict3))

        indexes_gmp = [IntGMP(1), IntGMP(2), IntGMP(3)]

        coeffs1 = shamir.lagrange_coefficients(IntGMP(0), indexes_gmp, key_1.q)


        coeffs2 = shamir.lagrange_coefficients(IntGMP(0), indexes_gmp, key_2.q)

        coeffs3 = shamir.lagrange_coefficients(IntGMP(0), indexes_gmp, key_3.q)

        print(coeffs1)
        print(coeffs2)
        print(coeffs3)
        print(self.key.x_shares)
        a1 = coeffs1[1].__mul__(key_1.x_share)
        #a1 = coeffs1[1].__mul__(self.key.x_shares['1'])
        a1.inplace_pow(1, key_1.q)
        a2 = coeffs2[2].__mul__(key_2.x_share)
        #a2 = coeffs1[2].__mul__(self.key.x_shares['2'])
        a2.inplace_pow(1, key_1.q)

        a3 = coeffs3[3].__mul__(key_3.x_share)
        a3.inplace_pow(1, key_1.q)

        x_temp = a1.__add__(a2)
        x_temp.inplace_pow(1, key_1.q)

        x_temp.__add__(a3)
        x_temp.inplace_pow(1, key_1.q)

        print("temp x")
        print(x_temp.to_bytes())

        y_temp = self.key.g.__pow__(x_temp, self.key.p)
        self.assertTrue(y_temp.__eq__(self.key.y))


    def test_key_2(self):
        indexes_gmp = [IntGMP(1), IntGMP(2), IntGMP(3)]
        coeffs = shamir.lagrange_coefficients(IntGMP(0), indexes_gmp, self.key.q)

        temp = IntGMP(1)
        for idx in coeffs:
            pk_idx = self.key.group_pks[str(idx)]
            pk_idx.inplace_pow(coeffs[idx],self.key.p)
            temp.__imul__(pk_idx)
            temp.inplace_pow(1, self.key.p)


        print("Hello")
        self.assertTrue(self.key.y.__eq__(temp))



if __name__ == '__main__':
    unittest.main()
