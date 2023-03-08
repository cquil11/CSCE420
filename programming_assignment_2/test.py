import re

pattern = r"^(O{3}|X{3}).{3}(O{3}|X{3})$"

string = "O...O...O"
match = re.search(pattern, string)

if match:
    print("Match found!")
else:
    print("Match not found.")