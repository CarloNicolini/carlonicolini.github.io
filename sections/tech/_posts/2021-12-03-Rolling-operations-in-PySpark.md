---
title: Rolling operations in PySpark
layout: post
section: tech
published: true
date: 2021-12-03
---

Have you ever wondered how to perform rolling averages in PySpark? This snippet helps you through the process

{% highlight python %}
from typing import Callable, Any, List
from pyspark.sql import Column
from pyspark.sql import DataFrame as SparkDataFrame
def create_rolling_feature(
  df: SparkDataFrame,
  id_cols:List[str]=["GROUP1", "GROUP2"],
  value_col:List[str]="VALUE",
  time_col:str="DATE",
  window_size:int=3,
  agg_func: Callable[[Column,],Any] = F.mean
) -> SparkDataFrame:
  """
  Creates a moving window average
  df: SparkDataFrame
    Spark dataframe to work on
  id_cols: List[str]
    The list of partitionBy columns over which to group the rolling function
  value_col: List[str]
    The name of the columns we want to compute rolling operations over
  time_col: str
    Name of the column representing time. Here we assume we have datetime columns with the possibility of casting to long.
  window_size: int
    The number of rows to consider in the rolling aggregation, by default 3 means that the moving operations is done on the aggregation function over the [current-3, current-2, current-1, current] rows.
  agg_func:
    A PySpark aggregation function. Can be any function that takes a column and returns a scalar, for example `F.mean`, `F.min`, `F.max`
  """
  rolling_col = f"ROLLING_{agg_func.__name__.upper()}_{value_col}_W{window_size}"
  window = Window.partitionBy(*id_cols).orderBy(time_col)
  return (
    df
    .withColumn(
      rolling_col,
        agg_func(F.col(value_col)).over(
          Window.partitionBy(*id_cols).orderBy(F.col(time_col).cast("timestamp").cast("long").asc()).rowsBetween(-window_size,0)
      )
    )
  )

create_rolling_feature(X,agg_func=F.max).display()
{% endhighlight %}