import subprocess
import re
import csv
from datetime import datetime

print("Connecting to Android through ADB...")

command = [
    "adb", "shell", "content", "query",
    "--uri", "content://sms",
    "--projection",
    "_id:address:person:date:body:type:read"
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

print("Reading SMS records...")

rows = []

for line in output.splitlines():

    if not line.startswith("Row:"):
        continue

    fields = dict(
        re.findall(r'(\w+)=([^,]*?)(?=,\s*\w+=|$)', line)
    )

    try:
        timestamp = int(fields.get("date", 0))

        sms_date = datetime.fromtimestamp(
            timestamp / 1000
        ).strftime("%d-%m-%Y %H:%M:%S")

        sms_type = fields.get("type", "")

        if sms_type == "1":
            message_type = "Inbox"
        elif sms_type == "2":
            message_type = "Sent"
        else:
            message_type = sms_type

        rows.append({
            "Contact ID": fields.get("person", ""),
            "Phone Number": fields.get("address", ""),
            "Date": sms_date,
            "Message": fields.get("body", ""),
            "SMS Type": message_type,
            "Read Status": fields.get("read", ""),
            "Record ID": fields.get("_id", ""),
            "Timestamp": timestamp
        })

    except (ValueError, OSError):
        continue

# Sort by newest timestamp
rows.sort(
    key=lambda x: x["Timestamp"],
    reverse=True
)

# Select latest 100 SMS
rows = rows[:100]

if not rows:
    print("No SMS records found.")
    raise SystemExit

filename = "latest_100_sms.csv"

with open(filename, "w", newline="", encoding="utf-8-sig") as file:

    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)

print("\nSUCCESS!")
print("Total SMS records:", len(rows))
print("Saved file:", filename)
