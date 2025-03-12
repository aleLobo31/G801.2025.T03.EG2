import unittest
from pathlib import Path
import json
from json import JSONDecodeError

from uc3m_money.account_manager import AccountManager
from uc3m_money import AccountManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

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


if __name__ == '__main__':
    unittest.main()
