---
layout: post
title: Optimization of groupby combinations
date: 2021-01-18
categories: science
published: false
---


# The problem

Suppose you have a pandas dataframe whose some of the columns represent grouping variables and others represent values.
You are given a target number and you want to match the combination of grouping variables such that some aggregate function (typically `sum`) matches the `target_value`.
In the case of sum, this problem is equivalent to the 0/1 knapsack problem and can be relatively simply solved by casting it as an **integer linear program** where variables are bound to be binary,
and an additional tolerance condition is added in terms of a `2 x n` matrix.

For the impatient reader here is the code, first two lines are required to installed the necessary libraries. From shell run these commands:

	conda install -c conda-forge glpk
	conda install cvxopt
	conda install pandas, numpy, typing

This is instead the Python code:
{% highlight python %}
from typing import List, Union, Callable, Iterable, Dict
import numpy as np
import cvxopt
import cvxopt.glpk as glpk
import pandas as pd
def optimize_combinations(
    df: pd.DataFrame,
    groupby_cols: List[str],
    value_col: str,
    target_value: Union[float, int],
    tolerance: Union[float, int],
    agg: Union[Callable, str] = sum,
    lambda_regu: float = 0.0,
    weights: Callable = None,
    filter_values: Dict[str, Iterable[str]] = None
):
    """
    Solves the 0/1 knapsack problem for the selection of dataframe rows whose corresponding value 
    is close enough to a specified target value.
    df: pd.DataFrame. The input dataframe to feed, must have some columns for grouping and another column for value
    groupby_cols: the list of columns to groupby
    target_value: the desidered value to get close to
    tolerance: an absolute deviation around the target value.
    lambda_regu: a regularization term which penalizes solutions choosing with too many elements
    """
    df_grouped = df.groupby(groupby_cols)[value_col].agg(agg).astype(float)
    n = df_grouped.shape[0]
    values = df_grouped.values
    ilp_c = cvxopt.matrix(values)
    ilp_G = cvxopt.matrix(np.vstack([df_grouped.values, -df_grouped.values]))
    h = cvxopt.matrix(np.array([[float(target_value + tolerance)], [float(-target_value + tolerance)]]))
    regularization = cvxopt.matrix(np.ones_like(values) * lambda_regu)
    
    if weights is not None:
        # experimental: a way to insert some business knowledge to the process
        regularization += weights(values)
        
    (status, sol) = cvxopt.glpk.ilp(
        c=-(ilp_c - regularization),  # to maximize
        G=ilp_G,
        h=h,
        I=set(range(n)),
        B=set(range(n))
    )

    if status != 'optimal':
        raise RuntimeError(status)
    
    sol = np.array(sol,dtype='int').flatten()
    df_result = df_grouped[df_grouped.index[np.where(sol)]].to_frame()
    df_result['delta_sol'] = df_result[value_col].sum() - target_value
    
    return {
        'sol': sol,
        'df_grouped': df_grouped,
        'index': df_grouped.index[np.where(sol)],
        'value': df_grouped.values[np.where(sol)].sum(),
        'delta_sol': target_value - df_grouped.values[np.where(sol)].sum(),
        'tolerance': tolerance,
        'result': df_result,
        'index_diff': df_grouped.index.difference(df_grouped.index[np.where(sol)]),
        'result_diff': df_grouped.loc[df_grouped.index.difference(df_grouped.index[np.where(sol)])],
    }
{% endhighlight %}
