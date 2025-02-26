import json
import unittest

from uc3m_money import AccountManagementException
from uc3m_money.account_manager import AccountManager

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''Opens JSON'''
        try:
            with open('../data/f1_test_from_iban.json', encoding='UTF-8', mode='r') as f:
                test_data_from_iban = json.load(f)
        except FileNotFoundError:
            raise AccountManagementException('Wrong file path')
        except json.JSONDecodeError:
            test_data_from_iban = []
        cls.__test_data_from_iban = test_data_from_iban

    def test_request_transfer_tc1(self):
        for input_data in self.__test_data_from_iban:
            if input_data['id_test'] == "TC1":
                am = AccountManager()
                transfer_code = am.transfer_request(input_data['from_iban'], input_data['to_iban'],
                                                    input_data['concept'], input_data['transfer_type'],
                                                    input_data['date_transfer'], input_data['amount'])
                self.assertEqual(transfer_code, 'La Vida es una Lenteja')


if __name__ == '__main__':
    unittest.main()
