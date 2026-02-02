# analyzer.py
import sys, csv, json

def load(path):
    with open(path) as f:
        r = csv.DictReader(f)
        return [int(x["event"]) for x in r]

A = load(sys.argv[1])
B = load(sys.argv[2])

div = sum(a!=b for a,b in zip(A,B)) / len(A)

result = {
    "samples": len(A),
    "divergence": div
}

with open(sys.argv[3], "w") as f:
    json.dump(result, f, indent=2)

print("📊 Divergence:", div)
