import os


for i in range(1, 11):
    if not os.path.exists(f"speaker{i}"):
        os.mkdir(f"speaker{i}")
# for i in range(1, 11):
#     if not os.path.exists(f"zh/speaker{i}"):
#         os.mkdir(f"zh/speaker{i}")
