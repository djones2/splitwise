# Splitwise Expense Calculator

This project is a command-line tool for calculating and settling shared expenses among a group, similar to Splitwise. It reads a CSV file containing expenses, computes each participant's net balance, and suggests the minimal set of payments needed to settle up.

## Features

- Reads expenses from a CSV file.
- Calculates net balances for each participant.
- Suggests settlements to minimize the number of payments.
- Handles missing or malformed data gracefully.

## Requirements

- Python 3.7+
- pandas

## Installation

Install dependencies using pip:

```
pip install pandas
```

## Usage

Run the script from the command line, providing the path to your expenses CSV file:

```
python splitwise.py <expenses>.csv
```

### CSV Format

Your CSV file should include the following columns:

- `Amount`: The total expense amount.
- `Paid By`: The name of the person who paid.
- `Participants`: Comma-separated names of people sharing the expense.
- `Comments`: Notes about the line item.

Example:

```
Amount,Item,Paid by,Participants,Notes
2533.48,Airbnb,Nick,"Avery,Cooper,Daniel,Josh,Matt,Noah",Subtract Coop from night 1
```

## Output

The script prints:

- Net balances for each participant.
- Suggested settlements (who should pay whom and how much).

## License

MIT License

## Author

Daniel Jones