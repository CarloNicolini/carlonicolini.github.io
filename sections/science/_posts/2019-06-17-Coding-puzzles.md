---
layout: post
title: Coding puzzles
published: false
date: 2019-06-17
---


# 1. Floyd triangle
Program the following thing, called Floyd triangle

    1
    2 3
    4 5 6
    7 8 9 10

and so on..

{% highlight python %}
rows,k=10,1
for i in range(rows):
    print('\n')
    for j in range(0,i):
        print(k," ",end='')
        k=k+1
{% endhighlight %}


# 2. Find third largest element in a given array
Objective: given an array of integers, write an algorithm to find the third largest element in the array.
For example, given a={6,8,1,9,2,1,10}, return 8.

This first approach can be considered cheating (moreover it is O(n log(N)) because of sorting)
{% highlight python %}
a={6,8,1,9,2,1,10}
as=sorted(a)
third_largest = as[-3]
{% endhighlight %}

Otherwise this other approach that is based on 3 variables, initially set as -infinity, and evaluated within if-else sections.
Iterating over the array we keep track of the values and compare with less operations.

{% highlight python %}
a = {6,8,1,9,2,1,10}
def third_largest_element(a):
    min_value = -100000 # a large negative value
    first,second,third = min_value,min_value,min_value
    for current in a:
        if first < current:
            third = second
            second = first
            first = current
        elif second<current:
            third = second
            second = current
        elif third<current:
            third = current
    return third
print(third_largest_element(a))
{% endhighlight %}

The logic here is that the third, second and first largest value are shifting up in the hierarchy, during the loop iteration.
Any other problem involving the $n$-th largest or smallest element can be solved with this method.

# 3. Find duplicate characters in a given string
Objective: Given a string, write an algorithm to find all the duplicate characters in the string and print its count.

Possible solution:
Collect the characters in a dictionary of integers. Iterate through the array. If the character is not in the dictionary, then set its value to one, otherwise and increase the value corresponding to the character

{% highlight python %}
a='hi my name is john'
d={} 
for x in a: 
   if x in d: 
      d[x]=d[x]+1 
   else: 
      d[x]=1 
# then filter all the characters such that d[x]>1
duplicates = { k:v for k,v in d.items() if v>1}
{% endhighlight %}
Ok this was very simple...

# 4 The word break problem
*Objective:* Given an string and a dictionary of words, find out if the input string can be broken into a space-separated sequence of one or more dictionary words.

   dictionary = ["I" , "have", "Jain", "Sumit", "am", "this", "dog"]
   String = "IamSumit"
   Output: "I am Sumit"
   String ="thisisadog"
   Output : String can't be broken

*Solution by backtracking in Python*
This solution works by backtracking and recursion. The logic is the following, as taken from [this site](algorithms.tutorialhorizon.com/the-word-break-problem)

- Navigate the given input string.
- Take a blank string and keep adding one character at a time to it.
- Keep checking if the word exist in the dictionary.
- If word exist in the dictionary then add that word to the answer string and make recursive call to the rest of the string.
- If any of the recursive call returns false then backtrack and remove the word from the answer string and again keep adding the characters to string.
- If all the recursive calls return true that means string has been broken successfully.

The python code to solve the algorithm is the following:

{% highlight python %}
def word_break(string, dic):
    answer = []
    def word_break(string, dic,answer):
        base = ''
        for i,x in enumerate(string):
            base += x
            if base in dic:
                answer.append(base + ' ')
                word_break(string[i+1:], dic, answer)
        return answer
    answer = word_break(string, dic, answer)
    return answer

if __name__=='__main__':
    words = ['I', 'have', 'Carlo', 'John',' ','a', 'is','am', 'this', 'cat']
    string = 'thisisacat'
    result = word_break(string, words)
    print(result)

    string = 'IamCarlo'
    result = word_break(string, words)
    print(result)
{% endhighlight %}
Alternatively this problem can be solved by means of dynamic programming.
Dynamic programming is a technique to solve the recursive problems in more efficient manner.
Many times in recursion we solve the sub-problems repeatedly.
In dynamic programming we store the solution of these sub-problems so that we do not have to solve them again, this is called Memoization.

Dynamic programming and memoization works together. So Most of the problems are solved with two components of dynamic programming (DP)-

*Recursion* - Solve the sub-problems recursively
*Memoization* - Store the solution of these sub-problems so that we do not have to solve them again

To solve our word break problem here we follow these ideas:

- We will use top-down  approach.
- Before we solve it for any string check if we have already solve it.
- We can use another dictionary to store the result of already solved strings.
- Whenever any recursive call returns false, store that string in dictionary.

For example a way to compute the Fibonacci function faster is to use memoization based recursion
{% highlight python %}
def fib_basic(n):
    if n==0 or n==1:
        return 1
    else:
         return fib(n-1)+fib(n-2)
{% endhighlight %}

What if we use a helper array with the values that have already been calculated?
{% highlight python %}
def fib_memoize(n, mem): 
    if n<=0: 
        return 0 
    elif n==1: 
        return n 
    elif n not in mem: 
        mem[n] = fib_memoize(n-1,mem) + fib_memoize(n-2,mem) 
    return mem[n] 
{% endhighlight %}

When we apply the idea of memoization and recursion to the word-break-problem we obtain the following algorithm:

{% highlight python %}
def word_break_dynamic(string, dic):
    ans = []
    mem = []
    def word_break(string, dic, memory, answer):
        if string == '':
            print(answer)
            return True
        elif string in memory: # did we already solve this subproblem?
            return False
        else:
            word = ''
            i = 0
            while i < len(string):
                word += string[i]
                if word in dic:
                    if word_break(string[i+1:], dic, memory, answer + [word] ):
                        return True
                    else:
                        i+=1
                else:
                    i+=1
            memory.append(string)
            return False

    ans = word_break(string, dic, mem, ans)
    return ans
{% endhighlight %}
