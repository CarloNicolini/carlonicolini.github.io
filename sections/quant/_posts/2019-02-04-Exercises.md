---
layout: post
title: Exercises for quantitative interviews
date: 2019-02-04
categories: quant
published: false
---

Exercise 1
----------

One morning in Springfield, it started snowing at heavy but constant rate. Homer Simpson had just started his own snowplow business. His snowplot started out at 08:00 AM and at 09:00 AM it had gone 2 miles. By 10:00 AM it had gone 3 miles.
Assuming that the snowplow removes a constant volume of snow per hour, determine the time at which it started snowing.

#### Solution


Exercise 2
----------
$a$ and $b$ are randomly chosen real numbers in the interval $[0,1]$,
that is both $a$ and $b$ are standard uniform random variables.
Find the probability that the quadratic equation $x^2+ax+b= 0$ has real solutions.

### Solution
The equation $x^2 + A x + B=0$ has real solutions if its determinant is positive or zero.
The determinant of a second order equation $ax^2 + bx + c=0$ is found as $\Delta = b^2 - 4ac$.
So in our case we have $\Delta = A^2 - 4B$.
We know that both $A$ and $B$ are $\sim U[0,1]$.
[Follow this guide](https://www.probabilitycourse.com/chapter4/4_1_3_functions_continuous_var.php)
1. We first find the pdf of the variable $Y=A^2$. We note that $R_Y=[0,1]$. As usual, we start with the CDF.
For $y \in [0,1]$, we have:

\begin{align}
F_Y(y) &= P(Y \leq y) \\\
&=P(X^2 \leq y) \\\
&=P(-\sqrt{y} \leq X \leq \sqrt{y}) \\\
&=\frac{\sqrt{y} -(-\sqrt{y}}{1-(-\sqrt{y})} \\\
&=\sqrt{y} 
\end{align}
since $X \sim U[0,1]$. Thus, the CDF of $Y$ is given by

\begin{equation}
F_Y(y) = \begin{cases} 0 & \text{ for } y \leq 0  \\\ \sqrt{y} & \text{ for } 0\leq y \leq 1 \\\ 1 & \textrm{ for } y \geq 1 \end{cases}
\end{equation}
Note that the CDF is a continuous function of $Y$, so $Y$ is a continuous random variable.


#### Exercise 3
Solve the equation:

\begin{equation}
\sqrt{x+\sqrt{x+{\sqrt{x+\sqrt{x+\sqrt{x...}}}}}} =x
\end{equation}

### Solution
Take the squares we get:
\begin{equation}
{x+\sqrt{x+{\sqrt{x+\sqrt{x+\sqrt{x...}}}}}} =x^2
\end{equation}
and the infinite square appears in the left hand side. However we know that it evaluates to $x$, hence we get $x+x=x^2$, and the solutions are $x_1=0$ and $x_2=2$.

#### Exercise 4
Solve the infinite tetration
\begin{equation}
x^{x^{x^{x^{x^{...}}}}} = 2
\end{equation}

#### Solution
The solution is simple to obtain.
Since the tetration is infinite, we have that the left exponent $(\cdot)^{x^{x^{x^{...}}}}$ is equal to 2. Hence $x^2=2$, and the solution is $x=\sqrt{2}$.

###
N-queens problem

{% highlight python %}
def n_queens(n, board=[]):
    if n == len(board):
        return 1

    count = 0
    for col in range(n):
        board.append(col)
        if is_valid(board):
            count += n_queens(n, board)
        board.pop()
    return count

def is_valid(board):
    current_queen_row, current_queen_col = len(board) - 1, board[-1]
    # Check if any queens can attack the last queen.
    for row, col in enumerate(board[:-1]):
        diff = abs(current_queen_col - col)
        if diff == 0 or diff == current_queen_row - row:
            return False
    return True
{% endhighlight %}
