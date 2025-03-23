import unittest
from pathlib import Path
import json
from json import JSONDecodeError

from uc3m_money import AccountManager
from uc3m_money import  AccountManagementException

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def test_f3_tc1_ok(self):
        iban = "ES8658342044541216872704"
        am = AccountManager()
        self.assertTrue(am.calculate_balance(iban))

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                balance_iban = json.load(f)
        except FileNotFoundError:
            balance_iban = {}
        except JSONDecodeError:
            balance_iban = {}

        # TO - DO Hacer más limpio el código de comprobación de las keys.
        try:
            v1 = balance_iban["IBAN"]
            v2 = balance_iban["date"]
            v3 = balance_iban["balance"]
        except KeyError:
            self.assertFalse(True)

    def test_f3_tc2_ko(self):
        iban = "ES8658342044541216872704"
        am = AccountManager()
        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban)
        self.assertEqual(amc.exception.message, "Error: all_transactions file not found")

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                balance_iban = json.load(f)
        except FileNotFoundError:
                file_not_found = True
        except JSONDecodeError:
            balance_iban = {}
        self.assertTrue(file_not_found)

    def test_f3_tc3_ko(self):
        iban = "ES8658342044541216872704"
        am = AccountManager()
        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban)
        self.assertEqual(amc.exception.message, "Error: all_transactions is not a valid JSON file")

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                balance_iban = json.load(f)
        except FileNotFoundError:
                file_not_found = True
        except JSONDecodeError:
            balance_iban = {}
        self.assertTrue(file_not_found)

if __name__ == '__main__':
    unittest.main()
