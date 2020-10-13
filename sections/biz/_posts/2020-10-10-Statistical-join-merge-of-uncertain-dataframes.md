---
layout: post
date: 2020-10-10
title: Statistical join and merge of uncertain dataframes
categories: biz
---

In these days I've faced what I believe is a very commomn problem for data scientists in the business industry.
When dealing with large databases it often happen that one has to find a common set of keys (or indices) to perform some join operations.
Those operations may be inner join, outer join or left/right join, depending on the application.
In any of these cases it is necessary to identify which columns may act as the right "pivot" to perform these operations.

What happens in reality is that very often there are no well-prepared "pivot" columns with univocal and unambiguous identifier in common between columns.
Often one has has to deal with uncertainty in some of the column values, for example with time-like values, some delay between systems contibuting to writing on databases may lead to erroneous effect when using time as a pivot, not to talk about the problems related to daylight saving shifts or different timezones.

A good system that could be deployed is one that "automatically" tries to learn from the data which column "talk" more between each other among the two (or more) databases, using some metric of similarity (with quantitative values) or better things like "mutual information" when dealing with categorical variables which may also contain typos or different encodings.

Take for example two databases, one where the country is encoded in italian, lowercase with three letters, the other where the country is encoded in english with two uppercase letters.
Clearly, here one needs domain knowledge to learn the 1:1 (when possible) matching between these two columns.
Moreover, imagine that, at least theoretically, the two datasets 

A business idea is to realize a system that could "learn" the right matching, identifying rows in the two databases which are plausible to be a match.

