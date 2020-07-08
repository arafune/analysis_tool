#!/usr/bin/env python3

# anime.ascii の振動エネルギーは THz単位らしい。
# でこれを meV単位にしたい。

output: str = ""
with open("anime.ascii", "r") as f:
    for line in f:
        if "metaData" in line:
            energy = float(line[43:-2]) * 4.13567  # THz unit を meVに
            output += line[:43] + "{:.6f}  \\".format(energy) + "\n"
        else:
            output += line
print(output)
# with open("a.a", "w") as f:
#    f.write(x)
