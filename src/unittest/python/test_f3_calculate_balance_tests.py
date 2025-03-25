"""CALCULATE BALANCE TESTS"""
import unittest
from pathlib import Path
import json
from json import JSONDecodeError

from uc3m_money import AccountManager
from uc3m_money import  AccountManagementException

class MyTestCase(unittest.TestCase):
    """Unittest Class"""
    @classmethod
    def setUpClass(cls):
        pass

    def test_f3_tc1_ok(self):
        """PATH 1_2_4_6_7_8_9_11_12_13_F AND LOOP CASE 2"""
        iban = "ES8658342044541216872704"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f3_TC1.json"

        self.assertTrue(am.calculate_balance(iban, path_all_transactions))

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                balance_iban = json.load(f)
        except FileNotFoundError:
            balance_iban = {}
        except JSONDecodeError:
            balance_iban = {}

        try:
            self.assertIn("IBAN", balance_iban)
            self.assertIn("date", balance_iban)
            self.assertIn("balance", balance_iban)
        except KeyError:
            self.fail()

    def test_f3_tc2_ko(self):
        """PATH 1_2_3_F"""
        iban = "ES6211110783482828975098"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/no_transactions.yeison"

        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban, path_all_transactions)
        self.assertEqual(amc.exception.message, "Error: all_transactions file not found")

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            file_not_found = True
        except JSONDecodeError:
            pass
        self.assertTrue(file_not_found)

    def test_f3_tc3_ko(self):
        """PATH 1_2_4_5_F"""
        iban = "ES6211110783482828975098"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f3_TC3.json"

        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban, path_all_transactions)
        self.assertEqual(amc.exception.message, "Error: all_transactions is not a valid JSON file")

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            file_not_found = True
        except JSONDecodeError:
            pass
        self.assertTrue(file_not_found)

    def test_f3_tc4_ko(self):
        """PATH 1_2_4_6_7_9_10_F AND LOOP CASE 3"""
        iban = "ES5520386795111966954674"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f3_TC4.json"

        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban, path_all_transactions)
        self.assertEqual(amc.exception.message, "IBAN not found in all_transactions.json")

        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            file_not_found = True
        except JSONDecodeError:
            pass
        self.assertTrue(file_not_found)

    def test_f3_tc5_ko(self):
        """PATH 1_2_4_6_9_10_F AND LOOP CASE 1"""
        iban = "ES5520386795111966954674"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f3_TC5.json"

        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban, path_all_transactions)
        self.assertEqual(amc.exception.message, "IBAN not found in all_transactions.json")

        path_balance_file = str(
            Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            file_not_found = True
        except JSONDecodeError:
            pass
        self.assertTrue(file_not_found)

    def test_f3_tc6_ko(self):
        """PATH 1_2_4_6_7_9_10_F AND LOOP CASE 4"""
        iban = "ES5520386795111966954674"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f3_TC6.json"

        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban, path_all_transactions)
        self.assertEqual(amc.exception.message, "IBAN not found in all_transactions.json")

        path_balance_file = str(
            Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            file_not_found = True
        except JSONDecodeError:
            pass
        self.assertTrue(file_not_found)

    def test_f3_tc7_ko(self):
        """PATH 1_2_4_6_7_9_10_F AND LOOP CASE 5"""
        iban = "ES5520386795111966954674"
        am = AccountManager()
        path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f3_TC7.json"

        with self.assertRaises(AccountManagementException) as amc:
            am.calculate_balance(iban, path_all_transactions)
        self.assertEqual(amc.exception.message, "IBAN not found in all_transactions.json")

        path_balance_file = str(
            Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        file_not_found = False
        try:
            with open(path_balance_file, mode="r", encoding="utf-8") as f:
                json.load(f)
        except FileNotFoundError:
            file_not_found = True
        except JSONDecodeError:
            pass
        self.assertTrue(file_not_found)

if __name__ == '__main__':
    unittest.main()
