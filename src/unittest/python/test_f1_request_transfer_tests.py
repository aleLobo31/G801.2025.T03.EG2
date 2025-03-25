"""REQUEST TRANSFER TESTS"""
import os
import json
from json import JSONDecodeError
from pathlib import Path
import unittest
from freezegun import freeze_time

from uc3m_money import AccountManagementException
from uc3m_money.account_manager import AccountManager

class MyTestCase(unittest.TestCase):
    """Unittest Class"""
    @classmethod
    def setUpClass(cls):
        """Opens JSON"""
        all_transfers_path = Path.home() / "PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"
        if all_transfers_path.exists():
            os.remove(all_transfers_path)  # Delete the file if it exists

        file_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/f1_test_valid_case.json"
        try:
            with open(file_path, encoding="UTF-8", mode="r") as f:
                test_data_transfer_request = json.load(f)
        except FileNotFoundError as e:
            raise AccountManagementException("Wrong file path") from e
        except json.JSONDecodeError:
            test_data_transfer_request = []
        cls.__test_data_transfer_request = test_data_transfer_request

        # Set a list with valid test cases
        cls.__valid_test_cases = ["TC1", "TC13", "TC14", "TC15", "TC21", "TC22", "TC25", "TC29", "TC30", "TC31"]
        cls.__special_test_cases = ["TC28", "TC38"]

    @freeze_time("2024-07-01")
    def test_f1_ok_cases(self):
        """METHOD FOR VALID CASES"""
        am = AccountManager()
        for index, input_data in enumerate(self.__test_data_transfer_request):
            test_id = "TC"+ str(index + 1)
            if test_id in self.__valid_test_cases:
                with self.subTest(test_id):
                    transfer_code = am.transfer_request(input_data["from_iban"], input_data["to_iban"],
                                                        input_data["concept"], input_data["transfer_type"],
                                                        input_data["date_transfer"], str(input_data["amount"]))
                    self.assertEqual(transfer_code, input_data["expected_result"])

                    file_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"
                    try:
                        with open(file_path, encoding="UTF-8", mode="r") as f:
                            all_transfers = json.load(f)
                    except FileNotFoundError as e:
                        raise AccountManagementException("Wrong file path") from e
                    except json.JSONDecodeError:
                        all_transfers = []

                    transfer_found = False
                    for transfer in all_transfers:
                        if transfer["transfer_code"] == transfer_code:
                            transfer_found = True
                    self.assertTrue(transfer_found)

    def test_f1_ko_cases(self):
        """METHOD FOR INVALID CASES"""
        am = AccountManager()

        all_transfers_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"
        try:
            with open(all_transfers_path, mode="r", encoding="utf-8") as i:
                init_file = json.load(i)
        except FileNotFoundError:
            init_file = []
        except JSONDecodeError:
            init_file = []

        for index, input_data in enumerate(self.__test_data_transfer_request):
            test_id = "TC"+ str(index + 1)
            if test_id not in self.__valid_test_cases and test_id not in self.__special_test_cases:
                with self.subTest(test_id):
                    if test_id != "TC32":
                        cast_amount = str(input_data["amount"])
                    else:
                        cast_amount = input_data["amount"]
                    with self.assertRaises(AccountManagementException) as amc:
                        am.transfer_request(input_data["from_iban"], input_data["to_iban"],
                                                            input_data["concept"], input_data["transfer_type"],
                                                            input_data["date_transfer"], cast_amount)
                    self.assertEqual(amc.exception.message, input_data["expected_result"])


                    try:
                        with open(all_transfers_path, mode="r", encoding="utf-8") as f:
                            final_file = json.load(f)
                    except FileNotFoundError:
                        final_file = []
                    except JSONDecodeError:
                        init_file = []

                    self.assertEqual(init_file, final_file)

    @freeze_time("2024-07-01")
    def test_f1_t38_case(self):
        """METHOD INVALID CASE T38"""
        am = AccountManager()
        with self.assertRaises(AccountManagementException) as amc:
            am.transfer_request(self.__test_data_transfer_request[37]["from_iban"],
                                                self.__test_data_transfer_request[37]["to_iban"],
                                                self.__test_data_transfer_request[37]["concept"],
                                                self.__test_data_transfer_request[37]["transfer_type"],
                                                self.__test_data_transfer_request[37]["date_transfer"],
                                                str(self.__test_data_transfer_request[37]["amount"]))
        self.assertEqual(amc.exception.message, self.__test_data_transfer_request[37]["expected_result"])

        file_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"

        transfer_count = 0
        dup_transaction = False
        try:
            with open(file_path, encoding="UTF-8", mode="r") as f:
                all_transfers = json.load(f)
        except FileNotFoundError as e:
            raise AccountManagementException("Wrong file path") from e
        except json.JSONDecodeError:
            all_transfers = []

        for transfer_i in all_transfers:
            for transfer_j in all_transfers:
                if transfer_i["transfer_code"] == transfer_j["transfer_code"]:
                    transfer_count += 1
            if transfer_count > 1:
                dup_transaction = True
            transfer_count = 0
        self.assertFalse(dup_transaction)


if __name__ == '__main__':
    unittest.main()
