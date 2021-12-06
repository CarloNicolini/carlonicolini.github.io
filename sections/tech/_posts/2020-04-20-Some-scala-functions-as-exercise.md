---
title: Some scala functions as exercise
section: tech
date: 2020-04-20
layout: post
---

Here are some very basic function with self-explanatory name, to be coded in Scala for a super beginner.
Some of them are very inefficient, pay attention to use them, they are only for demonstration.

## 1. Find the last element of a list

{%highlight scala %}
def last[T](xs : List[T]) : T = xs match
{
	case x :: Nil => x by defition the last element has Nil after
	case h::t => last(t)
	case _ => throw new NoSuchElementException
}
{% endhighlight %}


## 2. Find the first element of a list

{%highlight scala %}
def first[T](xs : List[T]) : T = xs match
{
	case head :: tail => head
	case _ => throw new NoSuchElementException
}
{% endhighlight %}

## 3. Find the last but one

{%highlight scala %}
def lastButOne[T](xs : List[T]) : T = xs match
{
	case x :: y :: Nil => x
	case h :: t => lastButOne(xs)
	case _ => throw new NoSuchElementException
}
{% endhighlight %}

## 4. Find the k-th element of a list

{%highlight scala %}
def kthElement[T](xs : List[T], k : Int) : T =
{
	def _kth(xs : List[T], acc : Int) : T=
	{
		if (k==acc) xs.head else _kth(xs.tail, acc + 1)
	}
	_kth(xs, 0)
}
{% endhighlight %}


## 5. Find the number of elements of a List

{%highlight scala %}
def length[T](xs : List[T]) : Int =
{
	def acc(xs : List[T], i : Int) : Int = xs match {
		case Nil => i
		case h::t => acc(xs.tail, i+1)
	}
	acc(xs, 0)
}
{% endhighlight %}

## 6. Reverse a list

### Simple solution:

{%highlight scala %}	
def reverse[T](xs : List[T]) : List[T] =
{
	xs apply xs.length to 1 by -1
}
{% endhighlight %}

### Procedural solution:

{% highlight scala %}
def reverse[T](xs : List[T]) : List[T] =
{
	def _reverse[T](res : List[T], rem : List[T] ) : List[T] = rem match {
		case Nil => res
		case h::t => _reverse(h::res, tail)
		case _ => throw new NoSuchElementException
	}
	_reverse(xs, )
}

{% endhighlight %}

{% highlight scala %}
def reverse[T](xs : List[T]) : List[T] =
{
	xs.foldLeft(){(h,t)=>(t::h)}
}
{% endhighlight %}

## 7. Find out wheter a list is palindrome

{%highlight scala %}
def isPalindrome[T](xs : List[T]) : Boolean =
{
	xs == reverse(xs)
}
{% endhighlight %}

## 8. Flatten a nested list structure

{% highlight scala %}
	def flatten(xs: List[_]): List[Any] = xs match
	{
		case Nil => Nil
		case (head: List[_]) :: tail => flatten(head) ::: flatten(tail)
		case head :: tail => head :: flatten(tail)
	}
{% endhighlight %}

## 9. Eliminate consecutive duplicates of list elements

{% highlight scala %}
	def filterDuplicates[T](xs : List[T]) : List[T] = xs match
	{
		case Nil => Nil
		case h::List() => List(h)
		case head::tail if (head == tail.head) => filterDuplicates(tail)
		case h::tail => h::filterDuplicates(tail)
	}
{% endhighlight %}

## 10. Pack consecutive duplicates of list elements into sublists

{%highlight scala %}
	def pack[T](xs : List[T]) : List[T] = xs match {
		case Nil => Nil stop condition

		case _ => throw new NoSuchElementException
	}
{% endhighlight %}
