import unittest
import hashlib
import json
from pathlib import Path

from uc3m_money import AccountManagementException
from uc3m_money.account_manager import AccountManager

class TestDepositIntoAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lines = []
        try:
            with open("../data/f2_test_case.json", encoding="UTF-8", mode="r") as file:
                lines = json.load(file)
        except FileNotFoundError as e:
            raise AccountManagementException("File not found")
        cls.__all_f2_test_cases = lines
        print(lines)
        return True

    def get_store_hash(self):
        try:
            with open("../data/deposit_values.json", encoding="UTF-8", mode="r") as f:
                file_hash = hashlib.md5(f.__str__().encode()).hexdigest()
        except FileNotFoundError:
            file_hash = ""
        return file_hash

    def test_f2_ok(self):
        for index, input_data in enumerate(self.__all_f2_test_cases):
            test_id = "TC" + str(index + 1)
            if test_id in ["TC1", "TC62"]:
                with self.subTest(test_id):
                    with open("../data/tmp_test_data.json", encoding="UTF-8", mode="w") as file:
                        file.write(json.dumps(input_data))
                am = AccountManager()
                deposit_signature = am.deposit_into_account("../data/tmp_test_data.json")
                self.assertEqual("sadfdsf", deposit_signature)

    def test_f2_ko(self):
        for index, input_data in enumerate(self.__all_f2_test_cases):
            test_id = "TC" + str(index + 1)
            print(test_id)
            print(input_data)
            if test_id not in ["TC1", "TC62"]:
                with self.subTest(test_id):
                    with open("../data/tmp_test_data.json", encoding="UTF-8", mode="w") as file:
                        file.write(json.dumps(input_data))

                deposit_hash_ini = self.get_store_hash()
                with self.assertRaises(AccountManagementException) as result:
                    am = AccountManager()
                    deposit_signature = am.deposit_into_account("../data/tmp_test_data.json")
                self.assertEqual(result.exception.message, "KO (JsonDecodeError)")
                deposit_hash_end = self.get_store_hash()
                self.assertEqual(deposit_hash_end, deposit_hash_ini)


if __name__ == '__main__':
    unittest.main()