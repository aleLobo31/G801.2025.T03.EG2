"""Module """
import re
import json
from json import JSONDecodeError
from pathlib import Path
from datetime import datetime

from .transfer_request import TransferRequest
from .account_management_exception import  AccountManagementException
from .account_deposit import AccountDeposit

class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str):
        """Return True if the IBAN received is valid spanish IBAN, or false in other case"""
        if not isinstance(iban, str):
            raise AccountManagementException("El IBAN no es un String")

        if len(iban) != 24:
            raise AccountManagementException("El IBAN debe tener 24 caracteres")

        if iban[:2] != 'ES' or not iban[2:].isdigit():
            raise AccountManagementException("El IBAN debe empezar por ES")

        iban = iban[4:] + iban[:4]
        numeric_iban = ''

        for char in iban:
            if not char.isalpha():
                numeric_iban += char
            else:
                numeric_iban += (str(ord(char) - 55))

        if int(numeric_iban) % 97 == 1:
            return True
        else:
            raise AccountManagementException("IBAN no valido")

    @staticmethod
    def validate_amount(amount : str) -> bool:
        """Return True if the amount follows the correct format, or false in other case"""
        regex = r"^EUR [1-9]\d{0,3}\.\d{2}$"
        return bool(re.match(regex, amount))

    def transfer_request(self, from_iban: str, to_iban: str, concept: str, transfer_type: str, date: str, amount: str):
        """Return Transfer Code if the request is valid"""

        """Check whether from_iban is valid"""
        self.validate_iban(from_iban)

        """Check whether to_iban is valid"""
        self.validate_iban(to_iban)
        if from_iban == to_iban:
            raise AccountManagementException("TO IBAN no puede ser igual que FROM IBAN")

        """Check whether concept is valid"""
        if not isinstance(concept, str):
            raise AccountManagementException("El concepto no es un String")
        concept_len = len(concept)
        regex = r"[A-Za-z]+ [A-Za-z]+"
        if concept_len < 10:
            raise AccountManagementException("El concepto debe tener al menos 10 caracteres")
        if concept_len > 30:
            raise AccountManagementException("El concepto debe tener como máximo 30 caracteres")
        if not re.search(regex, concept):
            raise AccountManagementException("El concepto debe tener al menos dos cadenas de letras")

        """Check whether transfer_type is valid"""
        valid_types = {"ORDINARY", "URGENT", "INMEDIATE"}
        if not isinstance(transfer_type, str):
            raise AccountManagementException("El tipo de la transaccion no es un string")
        if transfer_type not in valid_types:
            raise AccountManagementException("El tipo de la transaccion es desconocido")

        """Check whether date is valid"""
        try:
            transfer_date = datetime.strptime(date,"%d/%m/%Y").date()
            order_date = datetime.strptime(date, "%d/%m/%Y").date()
            # order_date = datetime.strptime("30/06/2024", "%d/%m/%Y").date() #TC25
            # order_date = datetime.strptime("02/07/2024", "%d/%m/%Y").date() #TC28
            # order_date = datetime.today().date()
            if transfer_date < order_date:
                raise AccountManagementException("La fecha de la transaccion es anterior a su orden")
        except TypeError:
            raise AccountManagementException("La fecha de la transaccion no es un string")
        except ValueError:
            raise AccountManagementException("La fecha de la transaccion no sigue el formato 'DD/MM/YYYY'")

        """Check whether amount is valid"""
        try:
            cast_amount = float(amount)
            decimal_part = amount.split(".")[1]
        except ValueError:
            raise AccountManagementException("La cantidad debe ser un valor numerico decimal")
        except AttributeError:
            raise AccountManagementException("La cantidad debe ser un string")
        except IndexError:
            raise AccountManagementException("La cantidad debe ser un valor numerico decimal")

        if len(decimal_part) > 2 or (len(decimal_part) == 1 and decimal_part != '0'):
            raise AccountManagementException("La cantidad debe tener dos decimales")
        if cast_amount < 10.00:
            raise AccountManagementException("La cantidad tiene que ser al menos 10,00€")
        if cast_amount > 10000.00:
            raise AccountManagementException("La cantidad no puede superar 10.000,00€")

        """Create TransferRequest Object to get the signature of the transaction"""
        tr = TransferRequest(from_iban, transfer_type, to_iban, concept, date, amount)
        # print(tr)

        """Get Transfer Code associated with this transaction"""
        transfer_code = tr.transfer_code

        """Read the existing transfers if all_transfers.json exists if not create an empty array"""
        file_path = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transfers.json"
        try:
            with open(file_path, encoding="utf-8", mode="r") as f:
                transfers = json.load(f)
        except FileNotFoundError:
            transfers = []
        except json.JSONDecodeError:
            raise AccountManagementException("El JSON provisto no es valido")

        """Check if the new transfer already exists in all_transfers.json"""
        for transfer in transfers:
            if transfer["transfer_code"] == transfer_code:
                raise AccountManagementException("Esta transaccion ya ha sido registrada")

        """If the transfer does not exist, append it in all_transfers.json"""
        transfers.append(tr.to_json())
        try:
            with open(file_path, encoding="utf-8", mode="w") as f:
                json.dump(transfers, f, indent=2)
        except FileNotFoundError:
            raise AccountManagementException("El path especificado es incorrecto")

        """If everything has worked return the transfer_code of the transaction"""
        return  transfer_code

    def deposit_into_account(self, input_file):
        try:
            with open(input_file, encoding="UTF-8", mode="r") as file:
                file_read = json.load(file)
                try:
                    json_file = json.loads(file_read)
                    if "IBAN" not in json_file or "AMOUNT" not in json_file:
                        raise AccountManagementException("KO (JsonDecodeError)")
                except json.JSONDecodeError as e:
                    raise AccountManagementException("KO (JsonDecodeError)")

        except FileNotFoundError as e:
            raise AccountManagementException("KO (File not found)")

        iban = json_file["IBAN"]
        amount = json_file["AMOUNT"]

        try:
            self.validate_iban(iban)
        except AccountManagementException:
            raise AccountManagementException("KO (Invalid IBAN)")

        if not self.validate_amount(amount):
            raise AccountManagementException("KO (Invalid Amount Format)")

        deposit = AccountDeposit(to_iban = iban, deposit_amount = amount)

        signature = deposit.deposit_signature

        deposit_json = deposit.to_json()

        try:
            with open(str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/unittest/data/deposit_values.json", encoding="UTF-8", mode="w") as file:
                file.write(json.dumps(deposit_json))
        except FileNotFoundError as e:
            raise AccountManagementException("KO (File not found)")

        return signature

    def calculate_balance(self, iban):
        """Calcula el saldo final asociado a un iban"""
        # 0. Initalize local variables
        balance_result = 0.0 # 1
        iban_found = False

        # 1. Validate input iban (Se puede dejar así porque ya internamente esta función genera excepciones
        self.validate_iban(iban) # 2

        # 2. Get transactions in all_transactions.json file
        # path_all_transactions = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/all_transactions.json"
        # TC2 path_all_transactions = str(Path.home()) + "/hdkfajfdkl"
        try:
            with open(path_all_transactions, mode="r", encoding="utf-8") as f: #3
                all_transactions = json.load(f) #4
        except FileNotFoundError: # 5
            raise AccountManagementException("Error: all_transactions file not found")
        except JSONDecodeError: # 6
            raise AccountManagementException("Error: all_transactions is not a valid JSON file")

        # 3. Iterate through json content and look for input iban
        for transaction in all_transactions: #7
            if transaction["IBAN"] == iban: #8
                iban_found = True #9
                balance_result = balance_result + float(transaction["amount"])

        # 4. Check IBAN was found or not
        if not iban_found: # 10
            raise AccountManagementException("IBAN not found in all_transactions.json") # 11

        # 5. Store result in json file (1 file per iban)
        path_balance_file = str(Path.home()) + "/PycharmProjects/G801.2025.T03.EG2/src/JsonFiles/balance" + iban + ".json"
        with open(path_balance_file, mode="w", encoding="utf-8") as f: #12
            balance_data = { #13
                "IBAN": iban,
                "date": str(datetime.now()),
                "balance": balance_result
            }
            json.dump(balance_data, f, indent=2)

        # 6. If everything is correct return true
        return True