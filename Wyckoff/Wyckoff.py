import json

import yaml

wyckoff_wte2: dict[str, list[list[float]]] = {
    "W": [[0, 0.60062, 0.5], [0, 0.03980, 0.01522]],
    "Te": [
        [0, 0.85761, 0.65525],
        [0, 0.64631, 0.11112],
        [0, 0.29845, 0.85983],
        [0, 0.20722, 0.40387],
    ],
}


print(json.dumps(wyckoff_wte2))
print(yaml.dump(wyckoff_wte2))
