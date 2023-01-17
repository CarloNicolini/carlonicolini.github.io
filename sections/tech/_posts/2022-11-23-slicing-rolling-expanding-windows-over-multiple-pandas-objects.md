---
layout: post
title: Slicing rolling expanding windows over multiple pandas objects
date: 2022-11-23
categories: tech
---

This is a fast way to yield a subset of rows from multiple Pandas dataframes or Series, when one needs to work on a sliding window basis over a predefined minimum and maximum number of rows. This approach is among the fastest available and is based on the `.iloc` accessor of both series and dataframes.

{%highlight scala %}
def rolling_expanding_window(seq, n_min, n_max):
    """
    Emits the elements over a rolling or expanding window of an iterable sequence
    Parameters
    ----------
    seq
    n_min
    n_max

    Returns
    -------

    """
    it = iter(range(len(seq)))  # makes it iterable
    # roll it forward at least warmup steps
    win = deque((next(it, None) for _ in range(n_min)), maxlen=n_max)
    # yield win
    for e in it:
        win.append(e)
        yield win


def sliding_dataframes(*arrays, n_min=0, n_max=None):
    """
    Like scikit-learn train_test_split but with rolling-expanding window
    Parameters
    ----------
    *arrays: one or more pandas dataframes or series that we want to slice over in parallel
    n_min: minimum window size
    n_max: maximum window size
    Returns
    -------
    """

    n_dataframes = len(arrays)
    if n_dataframes == 0:
        raise ValueError("At least one array required as input")

    n_samples = arrays[0].shape[0]
    for df in arrays:
        if not isinstance(df, (pd.DataFrame, pd.Series)) and df is not None:
            raise TypeError("This method only supports pandas dataframes and series")
        if df is not None and df.shape[0] != n_samples:
            raise ValueError("Specify equal length dataframes or series")

    # the first dataframe is the one dictating
    indices = rolling_expanding_window(arrays[0], n_min=n_min, n_max=n_max)
    for index in indices:
        yield list(
            chain.from_iterable(
                (a.iloc[index] if a is not None else None,) for a in arrays
            )
        )
{%endhighlight%}