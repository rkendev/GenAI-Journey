import math
from pathlib import Path

import pandas as pd

CSV = Path(__file__).parents[2] / "eval_data" / "queries.csv"


def load(split: float = 1.0, random_state: int = 42) -> pd.DataFrame:
    df = pd.read_csv(CSV)
    if 0 < split < 1:
        n = max(1, math.ceil(len(df) * split))  # ← ensures at least one row
        df = df.sample(n=n, random_state=random_state)
    return df.reset_index(drop=True)
