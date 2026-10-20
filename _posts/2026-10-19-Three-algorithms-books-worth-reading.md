---
layout: post
title: "Three algorithms books worth keeping close"
description: "A short appreciation of Kochenderfer and colleagues' beautifully written books on optimization, decision making, and validation."
date: 2026-10-19
published: false
permalink: "/sections/science/2026/10/19/Three-algorithms-books-worth-reading.html"
categories:
  - science
  - math
---

Some technical books make you want to sit down with a pencil and actually work through an algorithm. Mykel J. Kochenderfer and his coauthors have written three fantastic examples: *Algorithms for Optimization*, *Algorithms for Decision Making*, and *Algorithms for Validation*. I have copies of all three, and they deserve a place on the reading list of anyone who enjoys the mathematics of building useful computational systems.

What I particularly appreciate is the care in the explanations. Equations have room to breathe; figures help explain what the methods are doing; compact Julia implementations make the jump from an idea to an experiment feel manageable. These are substantial books, but the writing makes them inviting.

<div markdown="0" style="display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; margin: 2rem 0;">
  <a href="https://algorithmsbook.com/optimization/" style="flex: 0 1 180px;"><img src="{{ '/assets/media/algorithms-books/afo-800.jpg' | relative_url }}" alt="Algorithms for Optimization, second edition, book cover" style="width: 100%; height: auto;" loading="lazy"></a>
  <a href="https://algorithmsbook.com/decisionmaking/" style="flex: 0 1 180px;"><img src="{{ '/assets/media/algorithms-books/afdm-800.jpg' | relative_url }}" alt="Algorithms for Decision Making book cover" style="width: 100%; height: auto;" loading="lazy"></a>
  <a href="https://algorithmsbook.com/validation/" style="flex: 0 1 180px;"><img src="{{ '/assets/media/algorithms-books/afv-800.jpg' | relative_url }}" alt="Algorithms for Validation book cover" style="width: 100%; height: auto;" loading="lazy"></a>
</div>

*Cover images from the authors' [official website](https://algorithmsbook.com/), which also provides free PDFs. The optimization cover shown here is for the second edition.*

[**Algorithms for Optimization**](https://algorithmsbook.com/optimization/), with Tim A. Wheeler, is a wonderful starting point. It connects familiar descent methods to problems with constraints, expensive evaluations, and competing objectives. Suppose each evaluation of a design requires a slow simulation: the chapters on surrogate models and optimization explain how a cheaper approximation can help choose the next experiment. That is a compelling reason to learn the mathematics. The illustrations and executable algorithms make the choices between methods easier to understand.

[**Algorithms for Decision Making**](https://algorithmsbook.com/decisionmaking/), with Tim A. Wheeler and Kyle H. Wray, expands the picture to actions whose consequences unfold over time. Think of a robot navigating with noisy sensors: choosing a route depends on what it believes about its location, as well as where it wants to go. The progression from probabilistic reasoning to sequential decisions and belief-state planning gives those ideas a coherent home. I especially like having these connections explained within one consistent treatment.

The third volume, [**Algorithms for Validation**](https://algorithmsbook.com/validation/), with Sydney M. Katz, Anthony L. Corso, and Robert J. Moss, tackles a question that deserves much more attention: how do we find out where a system fails? Searching for a disturbance that makes a controller violate a safety requirement is one concrete example. Its treatment of falsification and failure-probability estimation also makes clear why finding a bad case and measuring how often failure occurs require different tools.

Together, these books offer an unusually well-written education in computational problem solving. They demand some mathematical effort, and repay it with explanations you can turn into code. I would happily recommend starting with whichever question is closest to your work, then following the connections into the other two.
