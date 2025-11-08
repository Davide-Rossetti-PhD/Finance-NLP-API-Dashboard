import random
import uuid
import datetime
import csv
from faker import Faker

fake = Faker("en_GB")  # puoi usare "it_IT" per nomi italiani

CATEGORIES = {
    "Food": ["McDonald's", "Subway", "Starbucks", "Pizza Express", "Just Eat"],
    "Groceries": ["Tesco", "Sainsbury's", "Lidl", "Aldi", "Waitrose"],
    "Transport": ["Uber", "Trainline", "Shell", "BP Petrol", "Transport for London"],
    "Shopping": ["Amazon", "Zara", "H&M", "IKEA", "Apple Store"],
    "Entertainment": ["Netflix", "Spotify", "Cineworld", "PlayStation Store"],
    "Utilities": ["British Gas", "Thames Water", "EE Mobile", "Octopus Energy"],
    "Health": ["Boots Pharmacy", "NHS Prescription", "PureGym", "Vision Express"],
    "Travel": ["Ryanair", "Booking.com", "Airbnb", "EasyJet"],
    "Income": ["Salary ACME Ltd", "Freelance Payment", "Tax Refund"],
    "Other": ["PayPal", "TransferWise", "Bank Fee"],
}

def generate_transaction():
    category = random.choice(list(CATEGORIES.keys()))
    merchant = random.choice(CATEGORIES[category])
    amount = round(random.uniform(5.0, 300.0), 2)
    if category != "Income":
        amount *= -1  # negative = expense
    date = fake.date_between(start_date="-12M", end_date="today")
    currency = random.choice(["EUR", "GBP", "USD"])
    city = fake.city()
    country = fake.country()

    return {
        "id": str(uuid.uuid4()),
        "date": date.isoformat(),
        "description": f"{merchant} {city}",
        "amount": amount,
        "currency": currency,
        "merchant": merchant,
        "category": category,
        "city": city,
        "country": country,
    }

def generate_dataset(n=1000, filename = "Data/synthetic_transactions.csv"
):
    Faker.seed(42)
    random.seed(42)
    rows = [generate_transaction() for _ in range(n)]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Generated {n} synthetic transactions → {filename}")

if __name__ == "__main__":
    generate_dataset(1000)
