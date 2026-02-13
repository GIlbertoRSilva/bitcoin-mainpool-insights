import csv
import json
import time
import os
import requests
from datetime import datetime, timezone

# ==========================
# CONFIGURAÇÃO
# ==========================
FEES_URL = "https://mempool.space/api/v1/fees/recommended"
MEMPOOL_URL = "https://mempool.space/api/v1/mempool"

CSV_PATH = "data/snapshots.csv"
JSONL_PATH = "data/snapshots.jsonl"
ERR_PATH = "data/errors.log"

INTERVAL_SECONDS = (3 * 60 )# 10 minutos

CSV_HEADER = [
    "timestamp_utc",
    "fastestFee",
    "halfHourFee",
    "hourFee",
    "economyFee",
    "minimumFee",
    "mempool_vsize",
    "spread",
    "ratio",
    "fastest_minus_min",
    "urgency_gap",
]

# ==========================
# FUNÇÕES AUXILIARES
# ==========================

def utc_now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def ensure_dir_for(path):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def ensure_csv_header():
    ensure_dir_for(CSV_PATH)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CSV_HEADER)

def append_csv(row):
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([row[h] for h in CSV_HEADER])

def append_jsonl(obj):
    ensure_dir_for(JSONL_PATH)
    with open(JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def log_error(msg):
    ensure_dir_for(ERR_PATH)
    with open(ERR_PATH, "a", encoding="utf-8") as f:
        f.write(f"{utc_now_iso()} | {msg}\n")

def fetch_fees():
    r = requests.get(FEES_URL, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_mempool():
    r = requests.get(MEMPOOL_URL, timeout=15)
    r.raise_for_status()
    return r.json()

# ==========================
# COLETOR PRINCIPAL
# ==========================

def main():
    print("collector started", flush=True)
    ensure_csv_header()
    print(f"interval={INTERVAL_SECONDS}s | Ctrl+C to stop", flush=True)

    while True:
        ts = utc_now_iso()

        try:
            print(f"{ts} | starting requests...", flush=True)

            fees = fetch_fees()
            mempool = fetch_mempool()

            fastest = int(fees["fastestFee"])
            half = int(fees["halfHourFee"])
            hour = int(fees["hourFee"])
            economy = int(fees["economyFee"])
            minimum = int(fees["minimumFee"])

            mempool_vsize = int(mempool["vsize"])

            spread = fastest - hour
            ratio = fastest / max(hour, 1)
            fastest_minus_min = fastest - minimum
            urgency_gap = fastest - half

            row = {
                "timestamp_utc": ts,
                "fastestFee": fastest,
                "halfHourFee": half,
                "hourFee": hour,
                "economyFee": economy,
                "minimumFee": minimum,
                "mempool_vsize": mempool_vsize,
                "spread": spread,
                "ratio": round(ratio, 4),
                "fastest_minus_min": fastest_minus_min,
                "urgency_gap": urgency_gap,
            }

            append_csv(row)
            append_jsonl({"timestamp_utc": ts, **fees, **mempool, **row})

            print(
                f"{ts} | saved | fastest={fastest} half={half} hour={hour} "
                f"mempool_vsize={mempool_vsize} spread={spread} ratio={round(ratio,4)}",
                flush=True,
            )

        except Exception as e:
            log_error(repr(e))
            print(f"{ts} | ERROR: {e}", flush=True)

        next_run = time.time() + INTERVAL_SECONDS
        next_run_iso = datetime.fromtimestamp(next_run, tz=timezone.utc).replace(microsecond=0).isoformat()
        print(f"{utc_now_iso()} | sleeping {INTERVAL_SECONDS}s | next_run_utc={next_run_iso}", flush=True)

        try:
            time.sleep(INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print(f"{utc_now_iso()} | Ctrl+C received. Exiting gracefully.", flush=True)
            return

if __name__ == "__main__":
    main()
