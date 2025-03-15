import json
from pathlib import Path
from freezegun import freeze_time
import unittest

from uc3m_money import AccountManagementException
from uc3m_money.account_manager import AccountManager

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''Opens JSON'''
        try:
            with open("../data/f1_test_valid_case.json", encoding="UTF-8", mode="r") as f:
                test_data_transfer_request = json.load(f)
        except FileNotFoundError:
            raise AccountManagementException("Wrong file path")
        except json.JSONDecodeError:
            test_data_transfer_request = []
        cls.__test_data_transfer_request = test_data_transfer_request

    @freeze_time("2024-07-01")
    def test_f1_OK_cases(self):
        am = AccountManager()
        for index, input_data in enumerate(self.__test_data_transfer_request):
            test_id = "TC"+ str(index + 1)
            if test_id in ["TC1"]:
                with self.subTest(test_id):
                    transfer_code = am.transfer_request(input_data["from_iban"], input_data["to_iban"],
                                                        input_data["concept"], input_data["transfer_type"],
                                                        input_data["date_transfer"], input_data["amount"])
                    self.assertEqual(transfer_code, input_data["expected_result"])

                    file_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"
                    try:
                        with open(file_path, encoding="UTF-8", mode="r") as f:
                            all_transfers = json.load(f)
                    except FileNotFoundError:
                        raise AccountManagementException("Wrong file path")
                    except json.JSONDecodeError:
                        all_transfers = []

                    transfer_found = False
                    for transfer in all_transfers:
                        if transfer["transfer_code"] == transfer_code:
                            transfer_found = True
                    self.assertTrue(transfer_found)

    def test_f1_KO_cases(self):
        am = AccountManager()
        for index, input_data in enumerate(self.__test_data_transfer_request):
            test_id = "TC"+ str(index + 1)
            if test_id not in ["TC1"]:
                with self.subTest(test_id):
                    with self.assertRaises(AccountManagementException) as amc:
                        transfer_code = am.transfer_request(input_data["from_iban"], input_data["to_iban"],
                                                            input_data["concept"], input_data["transfer_type"],
                                                            input_data["date_transfer"], input_data["amount"])
                    self.assertEqual(amc.exception.message, input_data["expected_result"])

                    file_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"

                    transfer_found = True
                    try:
                        with open(file_path, encoding="UTF-8", mode="r") as f:
                            all_transfers = json.load(f)
                    except FileNotFoundError:
                        transfer_found = False
                    except json.JSONDecodeError:
                        all_transfers = []
                    self.assertFalse(transfer_found)



if __name__ == '__main__':
    unittest.main()
