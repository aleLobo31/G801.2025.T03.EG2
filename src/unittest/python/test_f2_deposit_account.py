import unittest
import hashlib
import json
from freezegun import freeze_time
from datetime import datetime, timezone
from pathlib import Path

from uc3m_money import AccountManagementException
from uc3m_money.account_manager import AccountManager

class TestDepositIntoAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lines = []
        try:
            with open(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f2_test_case.txt", encoding="UTF-8", mode="r") as file:
                for line in file:
                    lines.append(line.strip())
        except FileNotFoundError as e:
            raise AccountManagementException("File not found")
        cls.__all_f2_test_cases = lines
        print(cls.__all_f2_test_cases)
        return True

    def get_store_hash(self):
        try:
            with open(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/deposit_values.json", encoding="UTF-8", mode="r") as f:
                file_hash = hashlib.md5(f.__str__().encode()).hexdigest()
        except FileNotFoundError:
            file_hash = ""
        return file_hash

    def test_f2_ok(self):
        index = 1
        for input_data in self.__all_f2_test_cases:
            test_id = "TC" + str(index)
            index += 1
            if test_id in ["TC1"]:
                print(test_id + "hola")
                with self.subTest(test_id):
                    with open(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/tmp_test_data.json", encoding="UTF-8", mode="w") as file:
                        file.write(json.dumps(input_data))

                frozen_time = datetime.now(timezone.utc)

                with freeze_time(frozen_time):
                    am = AccountManager()
                    deposit_signature = am.deposit_into_account(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/tmp_test_data.json")

                    test_alg = "SHA-256"
                    test_typ = "DEPOSIT"
                    test_iban = "ES9121000418450200051332"
                    test_amount = "EUR 1250.55"
                    test_time = datetime.timestamp(frozen_time)

                    test_json_string = "{alg:" + test_alg + ",typ:" + test_typ + ",iban:" + \
                                        test_iban + ",amount:" + test_amount + \
                                        ",deposit_date:" + str(test_time) + "}"

                    test_deposit_signature = hashlib.sha256(test_json_string.encode()).hexdigest()

                self.assertEqual(test_deposit_signature, deposit_signature)

                with open(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/deposit_values.json", encoding="UTF-8", mode="r") as file:
                    file_read = json.load(file)

                self.assertEqual(test_deposit_signature, file_read["deposit_signature"])

    def test_f2_ko(self):
        index = 1
        for input_data in self.__all_f2_test_cases:
            test_id = "TC" + str(index)
            print(test_id)
            index += 1
            if test_id not in ["TC1"]:
                with self.subTest(test_id):
                    with open(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/tmp_test_data.json", encoding="UTF-8", mode="w") as file:
                        file.write(json.dumps(input_data))

                    deposit_hash_ini = self.get_store_hash()
                    with self.assertRaises(AccountManagementException) as result:
                        am = AccountManager()
                        deposit_signature = am.deposit_into_account(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/tmp_test_data.json")
                    if test_id in ["TC45", "TC46", "TC67", "TC68", "TC69", "TC70", "TC71", "TC72", "TC73", "TC74", "TC75"]:
                        self.assertEqual(result.exception.message, "KO (Invalid IBAN)")
                    elif test_id in ["TC62", "TC63", "TC76", "TC77", "TC78", "TC79", "TC80", "TC81", "TC82", "TC83", "TC84", "TC85", "TC86", "TC87", "TC88", "TC89", "TC90", "TC91", "TC92"]:
                        self.assertEqual(result.exception.message, "KO (Invalid Amount Format)")
                    else:
                        self.assertEqual(result.exception.message, "KO (JsonDecodeError)")

                    deposit_hash_end = self.get_store_hash()
                    self.assertEqual(deposit_hash_end, deposit_hash_ini)

    def test_f2_file_not_found(self):
        with self.assertRaises(AccountManagementException) as result:
            am = AccountManager()
            deposit_signature = am.deposit_into_account("xxxxxxxxxxxxx")

            self.assertEqual(result.exception.message, "KO (File not found)")

if __name__ == '__main__':
    unittest.main()