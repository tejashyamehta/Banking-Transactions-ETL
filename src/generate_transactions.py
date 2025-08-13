import argparse, random, csv
from pathlib import Path
from datetime import datetime, timedelta, timezone
from faker import Faker

CATEGORIES = [
    ("Grocery", ["BigBazaar", "D-Mart", "FreshMart"]),
    ("Food", ["Zomato", "Swiggy", "Cafe Brew", "TacoTown"]),
    ("Fuel", ["HP", "BPCL", "IOCL"]),
    ("Bills", ["Amazon Pay", "PhonePe", "BharatBill"]),
    ("Electronics", ["Croma", "Reliance Digital", "UniTech"]),
    ("Travel", ["Uber", "Ola", "IRCTC"]),
]

def generate(n=1000, seed=42, out_dir=Path("data/raw")):
    fake = Faker("en_IN")
    Faker.seed(seed); random.seed(seed)
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    filename = out_dir / f"transactions_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    accounts = [f"ACCT{100000+i}" for i in range(200)]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["txn_id","account_id","merchant","merchant_category","amount_inr","currency","ts_utc"])
        base_time = now - timedelta(days=7)
        for i in range(n):
            category, merchants = random.choice(CATEGORIES)
            merchant = random.choice(merchants)
            account = random.choice(accounts)
            amt = round(max(1, random.gauss(1500, 1200)), 2)
            # Randomly create some high values and zeros/negs for anomaly tests
            if random.random() < 0.02:
                amt = round(random.uniform(50000, 150000), 2)
            if random.random() < 0.005:
                amt = round(random.uniform(-500, 0), 2)
            ts = base_time + timedelta(seconds=random.randint(0, 7*24*3600))
            w.writerow([
                f"TXN{now.strftime('%Y%m%d%H%M%S')}{i:06d}",
                account, merchant, category, amt, "INR", ts.isoformat()
            ])
    print(f"Wrote {n} rows to {filename}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000, help="number of rows")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out_dir", type=str, default="data/raw")
    args = ap.parse_args()
    generate(args.n, args.seed, Path(args.out_dir))
