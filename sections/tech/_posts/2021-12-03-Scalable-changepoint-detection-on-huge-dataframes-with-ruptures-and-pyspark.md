---
layout: post
title: Changepoint detection on huge grouped dataframes with ruptures and PySpark
categories: tech
date: 2021-12-03
---

Here we describe a way to perform scalable changepoint detection on grouped time series data by using PySpark and the rupture library.


{% highlight python %}
from typing import List
import numpy as np
import pandas as pd

from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.types import *
import pyspark.sql.functions as F

import ruptures as rpt

def changepoint_detection(
  df: SparkDataFrame,
  time_col: str,
  value_col: str,
  group_cols: List[str],
  breakpoint_col:str="BREAKPOINTS",
  breakpoint_default:int=0,
  breakpoint_active:int=1,
  kernel_model:str="rbf",
  penalty:float=0.01,
):
  """
  Performs a grouped changepoint detection on individual time series, denoted by the pair (time_col, value_col)
  
  Runs the rupture off line changepoint detection algorithm
  df: SparkDatFrame
    The dataframe to work on
  time_col: str
    The column representing the datetime
  value_col: str
    The name of the series to segment
  group_cols: List[str]
    The grouping variables on to which perform rupture segmentation separately
  breakpoint_default: int (default 0)
    Value when there is not breakpoint
  breakpoint_active: int (default 1)
    Value when there is a breakpoint
  kernel_model: str
    Rupture kernel for the internal segmentation model
  penalty: float
    Regularization penalty, the larger the penalty the less the number of breakpoints
  """
  schema = df.schema
  
  new_schema = StructType(
    [field for field in schema ] + [StructField(name=breakpoint_col, dataType=IntegerType(), nullable=False)]
  )
    
  @F.pandas_udf(returnType=new_schema, functionType=F.PandasUDFType.GROUPED_MAP)
  def changepoint_algorithm(pandas_dataframe: pd.DataFrame):
    A = pandas_dataframe[[time_col, value_col]].sort_values(by=time_col)
    a,b = A[time_col], A[value_col]
    y = pd.Series(data=breakpoint_default, index=a.index)
    
    y.iloc[
      np.array(
        rpt.Pelt(model=kernel_model).fit(
          A[b.name].astype(float).values.reshape(-1,1)
      )
      .predict(pen=penalty) # penalty factor
    ) - 1 # because breakpoint indices are 1 to N
    ] = breakpoint_active
    return pandas_dataframe.assign(**{breakpoint_col: y})
    
  return (
    df
    .groupBy(*group_cols)
    .apply(changepoint_algorithm)
  )

# Example usage of the function, here we order by client and time to check for the results correctness
(
  changepoint_detection(
    df=df_bonifici_mensile,
    time_col="DATE",
    value_col="MEAN",
    group_cols=["GROUP"],
    breakpoint_active=500,
    kernel_model="l2",
    penalty=5E5
  )
  .orderBy("GROUP", "DATE")
  .display()
)
{% endhighlight %}