---
layout: post
date: 2020-10-10
title: Statistical join and merge of uncertain dataframes
categories: biz
published: false
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

A first attempt to make this idea more concrete is based on the calculation of the (corrected) Cramer V' statistics.

### Cramer V statistics
Taken from [Wikipedia](https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V)

$\phi_c$ is the intercorrelation of two discrete variables and may be used with variables having two or more levels.

$\phi_c$ is a symmetrical measure, it does not matter which variable we place in the columns and which in the rows.
Also, the order of rows/columns doesn't matter, so $\phi_c$ may be used with nominal data types or higher (notably ordered or numerical).

Cramér's V may also be applied to goodness of fit chi-squared models when there is a $1 \times k$ table (in this case $r = 1$).
In this case $k$ is taken as the number of optional outcomes and it functions as a measure of tendency towards a single outcome.

Cramér's V varies from $0$ (corresponding to no association between the variables) to $1$ (complete association) and can reach $1$ only when each variable is completely determined by the other.

$\phi_c^2$ is the mean square canonical correlation between the variables.

In the case of a $2 \times 2$ contingency table Cramér's V is equal to the Phi coefficient.

Note that as chi-squared values tend to increase with the number of cells, the greater the difference between r (rows) and c (columns), the more likely $\phi_c$ will tend to 1 without strong evidence of a meaningful correlation.

$V$ may be viewed as the association between two variables as a percentage of their maximum possible variation. 
$V^2$ is the mean square canonical correlation between the variables.


{%highlight python%}
def cramers_corrected_stat(confusion_matrix):
    """ Calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher, 
        Journal of the Korean Statistical Society 42 (2013): 323-328
    """
    from scipy.stats.contingency import chi2_contingency as chi2_contingency
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2/n
    r,k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min( (kcorr-1), (rcorr-1)))
{%endhighlight%}
