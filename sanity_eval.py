from model import State

s = State()

tests = [
    (1, "Offensive 1"),
    (2, "Defensive 1"),
    (7, "Offensive 2"),
    (8, "Defensive 2")
]

for fid, name in tests:
    s.function = fid
    print(name, "->", s.utility(1))
