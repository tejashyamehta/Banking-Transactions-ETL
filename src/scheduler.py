import schedule, time, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable

def run_gen():
    print("Generating transactions...")
    subprocess.run([PY, str(ROOT / "src" / "generate_transactions.py"), "--n", "1000"], check=True)

def run_etl():
    print("Running ETL...")
    subprocess.run([PY, str(ROOT / "src" / "etl_pipeline.py")], check=True)

if __name__ == "__main__":
    run_gen(); run_etl()
    schedule.every(1).minutes.do(run_gen)
    schedule.every(1).minutes.do(run_etl)
    print("Scheduler started. Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")
