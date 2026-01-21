I = 1
V = 5
X = 10
L = 50
C = 100
D = 500
M = 1000

s = "III"

split_s = []

total = 0
for rn in s:
    split_s.append(rn)

rn_count = len(split_s)

for i, rn in enumerate(split_s):
    next_char = split_s[i + 1] if i + 1 < len(split_s) else None

    if rn == "M":
        split_s[i] = 1000
    elif rn == "D":
        split_s[i] = 500
    elif rn == "C" and next_char in ("M", "D"):
        split_s[i] = -100
    elif rn == "C":
        split_s[i] = 100
    elif rn == "L":
        split_s[i] = 50
    elif rn == "X" and next_char in ("C", "L"):
        split_s[i] = -10
    elif rn == "X":
        split_s[i] = 10
    elif rn == "V":
        split_s[i] = 5
    elif rn == "I" and next_char in ("X", "V"):
        split_s[i] = -1
    elif rn == "I":
        split_s[i] = 1


for rn in split_s:
    total += rn

print(total)
