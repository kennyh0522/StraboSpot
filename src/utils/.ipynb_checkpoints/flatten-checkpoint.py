import json
import numpy as np
import pandas as pd

def _to_list(x):
    """Return a Python list for a cell, or None if the cell is null."""
    if isinstance(x, str):
        x = json.loads(x)  # use ast.literal_eval if cells are Python-style reprs
    if isinstance(x, (list, tuple, np.ndarray)):
        return list(x)
    if x is None or pd.isna(x):
        return None
    return [x]

def flatten_list_cols(df, cols, sep="_", null_as_nan=False,
                      min_count=1, max_levels=500):
    """
    One-hot encode list-valued columns into 0/1 columns named f"{col}{sep}{item}".

    min_count  : drop items appearing in fewer than this many rows' lists
    max_levels : raise if a column has more distinct (kept) items than this,
                 so you find out before memory blows up
    null_as_nan: null cells -> NaN (float32); otherwise 0 (uint8)
    """
    n = len(df)
    out_parts = [df.drop(columns=cols)]

    for col in cols:
        series = df[col].astype(object)

        # parse each distinct string only once
        cache = {}
        def parse(x):
            if isinstance(x, str):
                if x not in cache:
                    cache[x] = _to_list(x)
                return cache[x]
            return _to_list(x)

        lists = [parse(x) for x in series]
        null_mask = np.array([l is None for l in lists])
        lengths = np.fromiter((len(l) if l else 0 for l in lists),
                              dtype=np.int64, count=n)

        row_idx = np.repeat(np.arange(n), lengths)
        items = np.array([str(i).strip() for l in lists if l for i in l],
                         dtype=object)

        if len(items) == 0:
            continue

        codes, uniques = pd.factorize(items, sort=True)
        counts = np.bincount(codes, minlength=len(uniques))
        keep = counts >= min_count

        if keep.sum() > max_levels:
            print(
                f"'{col}' has {keep.sum()} distinct items (> max_levels={max_levels}). "
                f"Raise max_levels or min_count, or check this column isn't free text."
            )
            continue

        remap = np.full(len(uniques), -1, dtype=np.int64)
        remap[keep] = np.arange(keep.sum())
        new_codes = remap[codes]
        valid = new_codes >= 0

        mat = np.zeros((n, int(keep.sum())), dtype=np.uint8)
        mat[row_idx[valid], new_codes[valid]] = 1

        if null_as_nan:
            mat = mat.astype(np.float32)
            mat[null_mask] = np.nan

        names = [f"{col}{sep}{u}" for u in uniques[keep]]
        out_parts.append(pd.DataFrame(mat, columns=names, index=df.index))

    return pd.concat(out_parts, axis=1)