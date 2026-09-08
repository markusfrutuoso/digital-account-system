import time

class BankAccount:
    def __init__(self, id_account, balance = 0.0):
        if balance < 0:
            raise ValueError
        self.id = id_account
        self.balance = balance
        self.history_transactions = []

    def record_history_transactions(self, type: str, amount: float, timestamp=None):
        if timestamp is None:
            timestamp = time.time()
        self.history_transactions.append({
            "type": type,
            "amount": amount,
            "timestamp": timestamp,
        })

    def deposit(self, amount: float, timestamp=None):
        if amount <= 0:
            raise ValueError
        self.balance += amount
        self.record_history_transactions("deposit", amount, timestamp)
        return True

    def withdraw(self, amount: float, timestamp=None):
        if amount <= 0 or amount > self.balance:
            raise ValueError
        self.balance -= amount
        self.record_history_transactions("withdraw", amount, timestamp)
        return True

    def get_bank_statement(self):
        return self.history_transactions

    def get_total_deposit(self):
        return sum(
            transaction["amount"]
            for transaction in self.history_transactions
            if transaction["type"] == "deposit"
        )

    def get_total_withdraw(self):
        return sum(
            transaction["amount"]
            for transaction in self.history_transactions
            if transaction["type"] == "withdraw"
        )

    def export_bank_statement(self):
        if not self.history_transactions:
            return []
        for statement in self.history_transactions:
            print(statement)
        return True

    def transfer(self, id_secondary, amount):
        if self.balance < amount or amount <= 0:
            raise ValueError
        if self is id_secondary:
            raise ValueError
        self.balance -= amount
        id_secondary.balance += amount
        self.record_history_transactions("transfer", -amount, None)
        id_secondary.record_history_transactions("transfer", amount, None)
        return True

p1 = BankAccount(2, 300)
p2 = BankAccount(3, 300)
p1.deposit(200)
p1.deposit(300)
print(p1.export_bank_statement())
p1.transfer(3, 100)
