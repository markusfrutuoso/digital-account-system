import time
import csv
import io


class Account:
    def __init__(self, id, balance=0.0, credit_limit=0):
        if balance < 0:
            raise ValueError
        if credit_limit < 0:
            raise ValueError
        self.id = id
        self.balance = balance
        self.credit_limit = credit_limit
        self.history_transaction = []

    def validate_debit(self, amount):
        total = self.balance + self.credit_limit
        if amount > total or amount<=0:
            raise ValueError
        return 

    def record_history_transaction(self, transaction_type, amount, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.history_transaction.append({
            "transaction_type": transaction_type,
            "amount": amount,
            "timestamp": timestamp,
        })

    def deposit(self, amount, timestamp=None):
        if amount <= 0:
            raise ValueError
        self.balance += amount
        self.record_history_transaction("deposit", amount, timestamp)

    def withdraw(self, amount, timestamp=None):
        self.validate_debit(amount)
        self.balance -= amount
        self.record_history_transaction("withdraw", amount, timestamp)

    def get_statement(self):
        return [
        transaction.copy()
        for transaction in self.history_transaction
    ]

    def get_total_deposits(self):
        return sum(
            deposits["amount"]
            for deposits in self.history_transaction
            if deposits["transaction_type"] == "deposit"
            )

    def get_total_withdraws(self):
        return sum(
            withdraws["amount"]
            for withdraws in self.history_transaction
            if withdraws["transaction_type"] == "withdraw"
            )

    def export_bank_statement(self):
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")

        writer.writerow(["transaction_type", "amount", "timestamp"])

        for transaction in self.history_transaction:
            writer.writerow([
                transaction["transaction_type"],
                transaction["amount"],
                transaction["timestamp"],
            ])
        return output.getvalue()

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_acc(self, account_id, balance = 0.0, credit_limit = 0):
        if account_id in self.accounts:
            raise ValueError
        account = Account(account_id, balance, credit_limit)
        self.accounts[account_id] = account
        return account
    
    def get_by_id(self, account_id):
        if account_id not in self.accounts:
            raise ValueError

        return self.accounts[account_id]

    def transfer(self, id_from, id_to, amount, timestamp=None):
        if id_from == id_to:
            raise ValueError
        acc_from = self.get_by_id(id_from)
        acc_to = self.get_by_id(id_to)
        acc_from.validate_debit(amount)
        if timestamp is None:
            timestamp = time.time()
        acc_from.balance -= amount
        acc_to.balance += amount

        acc_from.record_history_transaction("transfer_out", amount, timestamp)
        acc_to.record_history_transaction("transfer_in", amount, timestamp)

    def contas_no_limite(self):
        return [
            account.id
            for account in self.accounts.values()
            if account.balance < 0
        ]

        