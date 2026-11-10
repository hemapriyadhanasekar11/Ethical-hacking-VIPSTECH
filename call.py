import subprocess
import re
import csv
from datetime import datetime

print("Connecting to Android through ADB...")

command = [
    "adb", "shell", "content", "query",
    "--uri", "content://call_log/calls",
    "--projection",
    "_id:number:name:date:duration:type:numberlabel"
]

result = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Safely decode Android output
output = result.stdout.decode("utf-8", errors="replace")

if result.returncode != 0:
    print("ADB Error:")
    print(result.stderr.decode("utf-8", errors="replace"))
    raise SystemExit

print("Reading call records...")

rows = []

for line in output.splitlines():

    if not line.startswith("Row:"):
        continue

    fields = dict(
        re.findall(r'(\w+)=([^,]*?)(?=,\s*\w+=|$)', line)
    )

    try:
        timestamp = int(fields.get("date", 0))

        call_date = datetime.fromtimestamp(
            timestamp / 1000
        ).strftime("%d-%m-%Y %H:%M:%S")

        rows.append({
            "Contact": fields.get("name", ""),
            "Phone Number": fields.get("number", ""),
            "Date": call_date,
            "Duration (Seconds)": fields.get("duration", ""),
            "Call Type": fields.get("type", ""),
            "Record ID": fields.get("_id", ""),
            "Label": fields.get("numberlabel", "")
        })

    except (ValueError, OSError):
        continue

# Sort by newest timestamp
rows.sort(
    key=lambda x: datetime.strptime(
        x["Date"], "%d-%m-%Y %H:%M:%S"
    ),
    reverse=True
)

# Select latest 100
rows = rows[:100]

if not rows:
    print("No call records found.")
    raise SystemExit

filename = "latest_100_calls.csv"

with open(filename, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)

print("\nSUCCESS!")
print("Total records:", len(rows))
print("Saved file:", filename)
