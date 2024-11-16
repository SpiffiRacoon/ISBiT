import os

folder = "/data/"

filename = "sequence_tester1"

paths = [
    "../data/sequence_tester1.csv",  
    "../../src/data/sequence_tester1.csv",
    f"../{folder}{filename}.csv"  
]


for path in paths:
    abs_path = os.path.abspath(path)
    exists = os.path.isfile(abs_path)
    print(f"Checking path: {path}")
    print(f"  Absolute path: {abs_path}")
    print(f"  File exists: {exists}")
    print("-" * 40)

print(f"Current working directory: {os.getcwd()}")
