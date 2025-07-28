import pandas as pd
from collections import defaultdict
import heapq
import logging
import argparse

logging.basicConfig(level=logging.INFO)

def load_sheet(csv_path):
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        logging.error(f"File '{csv_path}' not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        logging.error(f"File '{csv_path}' is empty or improperly formatted.")
        exit(1)

def validate_columns(df):
    required_columns = {'Amount', 'Paid By', 'Participants'}
    if not required_columns.issubset(df.columns):
        missing = required_columns - set(df.columns)
        logging.error(f"Missing required columns: {', '.join(missing)}")
        exit(1)

def calculate_balances(df):
    net_balances = defaultdict(float)

    for _, row in df.iterrows():
        try:
            payer = row['Paid By'].strip()
            amount = float(row['Amount'])
            shared_with = [person.strip() for person in row['Participants'].split(',') if person.strip()]
            if not shared_with:
                logging.warning(f"Skipping row with no participants: {row}")
                continue

            split_amount = amount / len(shared_with)

            for person in shared_with:
                net_balances[person] -= split_amount
            net_balances[payer] += amount
        except (ValueError, KeyError) as e:
            logging.warning(f"Skipping invalid row: {row} ({e})")

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

def print_balances(balances):
    print("Net Balances:")
    name_width = max(len(person) for person in balances.keys())
    for person, balance in sorted(balances.items()):
        print(f"{person:<{name_width}}: ${balance:.2f}")

def print_settlements(settlements):
    print("\nSettlements:")
    for line in settlements:
        print(line)

def splitwise(csv_path):
    df = load_sheet(csv_path)
    validate_columns(df)
    balances = calculate_balances(df)
    settlements = simplify_debts(balances)

    print_balances(balances)
    print_settlements(settlements)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Splitwise Expense Calculator")
    parser.add_argument("csv_path", help="Path to the CSV file containing expenses")
    args = parser.parse_args()

    splitwise(args.csv_path)