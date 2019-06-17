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
This solution works by backtracking and recursion
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
