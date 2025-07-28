import pandas as pd
from collections import defaultdict
import heapq

def load_sheet(csv_path):
    return pd.read_csv(csv_path)

def calculate_balances(df):
    net_balances = defaultdict(float)

    for _, row in df.iterrows():
        payer = row['Paid by'].strip()
        amount = float(row['Amount'])
        shared_with = [person.strip() for person in row['Participants'].split(', ')]
        split_amount = amount / len(shared_with)

        for person in shared_with:
            net_balances[person] -= split_amount
        net_balances[payer] += amount

    return net_balances

def simplify_debts(net_balances):
    debtors = []
    creditors = []
    settlements = []

    for person, balance in net_balances.items():
        if round(balance, 2) < 0:
            heapq.heappush(debtors, (balance, person))
        elif round(balance, 2) > 0:
            heapq.heappush(creditors, (-balance, person))

    while debtors and creditors:
        debtor_amount, debtor = heapq.heappop(debtors)
        creditor_amount, creditor = heapq.heappop(creditors)

        amount = min(-debtor_amount, -creditor_amount)
        settlements.append(f"{debtor} pays {creditor} ${amount:.2f}")

        debtor_amount += amount
        creditor_amount += amount

        if round(debtor_amount, 2) < 0:
            heapq.heappush(debtors, (debtor_amount, debtor))
        if round(creditor_amount, 2) < 0:
            heapq.heappush(creditors, (creditor_amount, creditor))

    return settlements

def splitwise(csv_path):
    df = load_sheet(csv_path)
    balances = calculate_balances(df)
    settlements = simplify_debts(balances)

    print("Net Balances:")
    for person, balance in balances.items():
        print(f"{person}: ${balance:.2f}")

    print("\nSettlements:")
    for line in settlements:
        print(line)

if __name__ == "__main__":
    splitwise("adam_bachelor_party_money.csv")
