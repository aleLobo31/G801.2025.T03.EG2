"""Module """
import re
import json
from pathlib import Path
from datetime import datetime

from .transfer_request import TransferRequest
from .account_management_exception import  AccountManagementException

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str):
        """Return True if the IBAN received is valid spanish IBAN, or false in other case"""
        if not isinstance(iban, str) or len(iban) != 24 or iban[:2] != 'ES' or not iban[2:].isdigit(): return False

        iban = iban[4:] + iban[:4]
        numeric_iban = ''

        for char in iban:
            if not char.isalpha():
                numeric_iban += char
            else:
                numeric_iban += (str(ord(char) - 55))

        if int(numeric_iban) % 97 == 1:
            return True
        return False

    def transfer_request(self, from_iban: str, to_iban: str, concept: str, transfer_type: str, date: str, amount: int):
        """Return Transfer Code if the request is valid"""

        """Check whether from_iban is valid"""
        if not self.validate_iban(from_iban):
            return False

        """Check whether to_iban is valid"""
        if not self.validate_iban(to_iban) or from_iban == to_iban:
            return False

        """Check whether concept is valid"""
        concept_len = len(concept)
        regex = r"[A-Za-z]+ [A-Za-z]+"
        if not isinstance(concept, str) or concept_len < 10 or concept_len > 30 or re.search(concept, regex):
            return False

        """Check whether transfer_type is valid"""
        valid_types = {"ORDINARY", "URGENT", "INMEDIATE"}
        if not isinstance(transfer_type, str) or transfer_type not in valid_types:
            return False

        """Check whether date is valid"""
        try:
            transfer_date = datetime.strptime(date, "%d/%m/%Y").date()
            order_date = datetime.strptime(date, "%d/%m/%Y").date()
            #order_date = datetime.today().date()
            if transfer_date > order_date:
                return  False
        except TypeError:
            return False
        except ValueError:
            return False

        """Check whether amount is valid"""
        if not isinstance(amount, float) or (amount * 100) % 1 >= 0.0001 or amount < 10.00 or amount > 10000.00:
            return  False

        """Create TransferRequest Object to get the signature of the transaction"""
        tr = TransferRequest(from_iban, transfer_type, to_iban, concept, date, amount)
        print(tr)

        """Get Transfer Code associated with this transaction"""
        transfer_code = tr.transfer_code

        """Read the existing transfers if all_transfers.json exists if not create an empty array"""
        file_path = Path.home() / "PycharmProjects/G801.2025.T03.EG2/src/unittest/data/all_transfers.json"
        try:
            with open(file_path, encoding="utf-8", mode="r") as f:
                transfers = json.load(f)
        except FileNotFoundError:
            transfers = []
        except json.JSONDecodeError:
            print("Decode Error")
            return False

        """Check if the new transfer already exists in all_transfers.json"""
        for transfer in transfers:
            if transfer["transfer_code"] == transfer_code:
                print("Repeated Tx")
                return False

        """If the transfer does not exist, append it in all_transfers.json"""
        transfers.append(tr.to_json())
        try:
            with open(file_path, encoding="utf-8", mode="w") as f:
                json.dump(transfers, f, indent=2)
        except FileNotFoundError:
            print("FileNotFound")
            return False

        """If everything has worked return the transfer_code of the transaction"""
        return  transfer_code