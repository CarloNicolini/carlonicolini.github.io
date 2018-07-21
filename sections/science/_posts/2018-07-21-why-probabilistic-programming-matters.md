---
layout: post
title: Why probabilistic programming matters
categories: science
published: true
use_math: true
date: 2018-05-21

---

I recently stumbled across the idea of probabilistic programming, something I had never heard before.
Indeed with the recent advances in artificial intelligence and machine learning, this field is seeing a very rapid development.
The motivation why I found this research field particularly interesting is its cross-talk with the ideas I developed in one of my last works on inference within the spectral entropy framework.

Specifically, systems like [Tensorflow](tensorflow.org), [Edward](http://edwardlib.org/) are implementing what has been described in the lines that I'm linking in the next section of this post.
I am referring to the article appeared in 2013 at the [following link](https://plus.google.com/+BeauCronin/posts/KpeRdJKR6Z1). All the credits are to the author, Beau Cronin, but I'd like to report his views in this post.

# Why Probabilistic Programming Matters

Last week, DARPA announced a new program to fund research in probabilistic programming languages. While the accompanying news stories gave a certain angle on why this was important, this is a new research area and it's still pretty mysterious to most people who care about machine intelligence.

So: what is probabilistic programming, and why does it matter? Read on for my thoughts.

A probabilistic programming language is a language which includes random events as first-class primitives. When the expressive power of a real programming language is brought to bear on random events, the developer can easily encode sophisticated structured stochastic processes - i.e., probabilistic models of the events that might have occurred in the world to produce a given collection of data or observations.

But just writing down a probability model as a computer program wouldn't be particularly exciting - that's just a matter of syntax. The real power of a probabilistic programming language lies in its compiler or runtime environment (like other languages, probabilistic ones can be either compiled or interpreted). In addition to its usual duties, the compiler or runtime needs to figure out how to perform inference on the program. Inference answers the question: of all of the ways in which a program containing random choices could execute, which of those execution paths provides the best explanation for the data?

Another way of thinking about this: unlike a traditional program, which only runs in the forward directions, a probabilistic program is run in both the forward and backward direction. It runs forward to compute the consequences of the assumptions it contains about the world (i.e., the model space it represents), but it also runs backward from the data to constrain the possible explanations. In practice, many probabilistic programming systems will cleverly interleave these forward and backward operations to efficiently home in on the best explanations.

>A probabilistic programming language is a language which includes random events as first-class primitives.

So, that's probabilistic programming in a nutshell. It's clearly cool, but why does it matter?

Probabilistic programming will unlock narrative explanations of data, one of the holy grails of business analytics and the unsung hero of scientific persuasion. People think in terms of stories - thus the unreasonable power of the anecdote to drive decision-making, well-founded or not. But existing analytics largely fails to provide this kind of story; instead, numbers seemingly appear out of thin air, with little of the causal context that humans prefer when weighing their options.

But probabilistic programs can be written in an explicitly "generative" fashion - i.e., a program directly encodes a space of hypotheses, where each one comprises a candidate explanation of how the world produced the observed data. The specific solutions that are chosen from this space then constitute specific causal and narrative explanations for the data.

The dream here is to combine the best aspects of anecdotal and statistical reasoning - the persuasive power of story-telling, and the predictiveness and generalization abilities of the larger body of data.

Probabilistic programming decouples modeling and inference. Just as modern databases separate querying from indexing and storage, and high-level languages and compilers separate algorithmic issues from hardware execution, probabilistic programming languages provide a crucial abstraction boundary that is missing in existing learning systems.

>Probabilistic programming will unlock narrative explanations of data, one of the holy grails of business analytics and the unsung hero of scientific persuasion. 

While modeling and inference/learning have long been seen as conceptually separate activities, they have been tightly linked in practice. What this means is that the models that are applied to a given problem are very tightly constrained by the need to derive efficient inference schemes - and these schemes are incredibly time-consuming to derive and implement, requiring very specialized skills and expertise. And even small changes to the model can necessitate wholesale rethinking of the inference approach. This is no way to run a railroad.

If probabilistic programming reaches its potential, these two activities will finally be decoupled by a solid abstraction barrier: the programmer will write the program he wants, and then leave it to the compiler or runtime to sort out the inference (though see below for challenges). This should allow the probabilistic programmer to encode and leverage much more of his domain knowledge, utimately leading to much more powerful reasoning and better data-driven decisions.

Probabilistic programming enables more general, abstract reasoning, because these programs can directly encode many levels of reasoning and then perform inference across all of these levels simultaneously. Existing learning systems are largely confined to learning the model parameters that provide the best explanation of the data, but they are unable to reason about whether the model class itself is appropriate.

Probabilistic programs, on the other hand, can reason across all of these levels at the same time: learning model parameters, and also choosing the best models from a given class, and also deciding between entirely different model classes. While there is no silver bullet to modeling bias and the application of inappropriate models, this capability will nevertheless go a long way toward providing the best explanations for data, not only at the quantitative but also the qualitative level.

Finally, I should mention some of the key challenges that researchers will have to solve if probabilistic programming is to have these kinds of impacts:

Creating the compilers and runtimes that automatically generate good inference schemes for arbitrary probabilistic programs is very, very hard. If the discussion above sounds too good to be true, that's because it just might be. Researchers have a lot of work ahead of them if they want to make all of this work in the general setting. The most successful systems to date (BUGS, infer.net, factor.ie) have worked by limiting the expressive power of the language, and thus reducing the complexity of the inference problem.

All abstractions are leaky, and the abstraction between modeling (i.e., writing a probabilistic program) and inference is no different. What this means is that some probabilistic programs will result in much faster inference than others, for reasons that may not be easy for the programmer to understand. In traditional high-level programming languages, these problems are typically solved by profiling and optimization, and probabilistic systems will need to come with the analogous set of tools so that programmers can inspect and solve the performance problems they encounter.

Finally, probabilistic programming requires a different combination of skills from traditional development, on the one hand, and machine learning or statistical inference on the other. I think it would be a shame if these systems, once they were developed, remained at the fringes - used only by the kinds of programmers who are currently drawn to, say, languages like Lisp and Haskell.

While these challenges are indeed great, I have very high hopes for probabilistic programming over the next few years. Some of the very smartest people I've ever known or worked with are involved in these projects, and I think they're going to make a lot of progress.

Note: I have no involvement with any current probabilistic programming research, nor with the DARPA program; at this point, I'm just an interested observer.