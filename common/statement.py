from common.transaction import Transaction
from common.transaction import TransactionType
from common.transaction import to_transaction
import tables.transaction_history


class Statement:
    def __init__(self, transactions: [Transaction]):
        self.transactions = transactions

    def get_total_profit_repr(self) -> str:
        return f'Total profit estimated: {sum(t.get_profit() for t in self.transactions)}'

    def get_handover_profit_repr(self) -> str:
        settled_transactions = [t for t in self.transactions if t.is_linked()]
        cost = sum(t.get_transaction_price() for t in settled_transactions if t.get_type() == TransactionType.BOUGHT)
        feedback = sum(t.get_transaction_price() for t in settled_transactions if t.get_type() == TransactionType.SOLD)
        profit = sum(t.get_profit() for t in settled_transactions)
        return f'Profit already handover: {feedback} + {cost} = {profit}, rate: {profit * 100 / -cost:.2f}%'

    def get_in_stock_profit_repr(self) -> str:
        in_stock_transactions = [t for t in self.transactions if not t.is_linked()]
        cost = sum(t.get_transaction_price() for t in in_stock_transactions)
        feedback = sum(t._get_estimate_handover_price() for t in in_stock_transactions)
        profit = sum(t.get_profit() for t in in_stock_transactions)
        return f'Profit in stock: {feedback} + {cost} = {profit}, rate: {profit * 100 / -cost:.2f}%'

    def get_win_rate_repr(self) -> str:
        settled_transactions = [t for t in self.transactions if t.is_linked() if t.get_type() == TransactionType.SOLD]
        win = sum(1 for _ in settled_transactions if _.get_profit() > 0)
        return f'Win rate: {win} / {len(settled_transactions)} = {win * 100 / len(settled_transactions)}%'


def to_statement(transaction_records: [tables.transaction_history.TransactionHistory], latest_price: {str: float}):
    transactions = [to_transaction(t, latest_price.get(t.sid)) for t in transaction_records]
    for i in range(0, len(transactions)):
        if transactions[i].get_type() == TransactionType.SOLD:
            for j in range(i + 1, len(transactions)):
                capacity = transactions[i].capacity
                if transactions[j].get_type() == TransactionType.BOUGHT and transactions[i].sid == transactions[j].sid:
                    capacity -= transactions[j].capacity
                    transactions[i].add_linked_transaction(transactions[j])
                    transactions[j].add_linked_transaction(transactions[i])
                    if capacity == 0:
                        break
    return Statement(transactions)
