import datetime
import enum

import tables.transaction_history


class TransactionType(enum.Enum):
    BOUGHT = 'bought'
    SOLD = 'sold'


class Transaction:
    def __init__(self, commission_id: str, date: datetime.date, sid: str, capacity: int, unit_price: float,
                 handling_charge: int, tax: int, latest_price: float):
        self.commission_id = commission_id
        self.date = date
        self.sid = sid
        self.capacity = capacity
        self.unit_price = unit_price
        self.handling_charge = handling_charge
        self.tax = tax
        self.latest_price = latest_price
        self.linked_transactions = []

    def get_profit(self) -> int:
        pass

    def add_linked_transaction(self, transaction: 'Transaction'):
        self.linked_transactions.append(transaction)

    def get_type(self) -> TransactionType:
        pass

    def is_linked(self) -> bool:
        return len(self.linked_transactions) > 0

    def get_transaction_price(self) -> int:
        pass


class BoughtTransaction(Transaction):
    def __init__(self, commission_id: str, date: datetime.date, sid: str, capacity: int, unit_price: float,
                 handling_charge: int, tax: int, latest_price: float):
        super(BoughtTransaction, self).__init__(commission_id, date, sid, capacity, unit_price, handling_charge, tax,
                                                latest_price)

    def get_profit(self) -> int:
        return 0 if self.is_linked() else self.get_transaction_price() + self._get_estimate_handover_price()

    def get_transaction_price(self) -> int:
        return -int(self.capacity * self.unit_price + self.handling_charge)

    def _get_estimate_handover_price(self) -> int:
        total_price = int(self.capacity * self.latest_price)
        return total_price - self._calculate_handling_charge(total_price) - self._calculate_tax(total_price)

    def _calculate_handling_charge(self, total_price: int) -> int:
        return int(total_price * 0.001425 * 0.28)

    def _calculate_tax(self, total_price: int) -> int:
        return int(total_price * 0.003)

    def get_type(self) -> TransactionType:
        return TransactionType.BOUGHT


class SoldTransaction(Transaction):
    def __init__(self, commission_id: str, date: datetime.date, sid: str, capacity: int, unit_price: float,
                 handling_charge: int, tax: int, latest_price: float):
        super(SoldTransaction, self).__init__(commission_id, date, sid, capacity, unit_price, handling_charge, tax,
                                              latest_price)

    def get_profit(self) -> int:
        return self.get_transaction_price() + sum(t.get_transaction_price() for t in self.linked_transactions)

    def get_transaction_price(self) -> int:
        return int(self.capacity * self.unit_price) - self.handling_charge - self.tax

    def get_type(self) -> TransactionType:
        return TransactionType.SOLD


def to_transaction(record: tables.transaction_history.TransactionHistory, latest_price):
    if record.type == 1:
        return BoughtTransaction(record.commissionId, record.date, record.sid, record.capacity, record.unitPrice,
                                 record.handlingCharge, record.tax, latest_price)
    else:
        return SoldTransaction(record.commissionId, record.date, record.sid, record.capacity, record.unitPrice,
                               record.handlingCharge, record.tax, latest_price)
