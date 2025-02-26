"""Module """
from .uc3m_money import TransferRequest


class AccountManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban: str):
        """RETURN TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        if len(iban) != 24 or iban[:2] != 'ES' or not iban[2:].isdigit(): return False

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

    def transfer_request(self, from_iban, to_iban, concept, type, date, amount):
        # 1. Validar Entradas
        if(not self.validate_iban(from_iban)):
            return False

        # 2. Instanciar el objeto Transfer Request
        tr = TransferRequest(from_iban, to_iban, concept, type, date, amount)

        # 3.

        # 4.