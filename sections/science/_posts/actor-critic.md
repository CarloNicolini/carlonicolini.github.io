---
layout: post
title: "Energy-based models, free energy, and chain-of-thought (notes)"
description: ''
date: 2025-12-01
published: false
categories:
  - science
  - language-physics
---
The recent paper you are referring to—*Autoregressive Language Models are Secretly Energy-Based Models: Insights into the Lookahead Capabilities of Next-Token Prediction* (Blondel et al., arXiv:2512.15605)—establishes a profound mathematical bridge between standard next-token prediction and sequence-level energy minimization.

When you synthesize this mathematical insight with Karl Friston’s **Free Energy Principle (FEP)**, a fascinating conceptual framework emerges: **Chain of Thought (CoT) reasoning can be understood as an "active inference" process, where the model explores a state space to minimize expected free energy (surprise) and settle into a globally optimal sequence.**

Here is a step-by-step breakdown of how these concepts connect.

### 1. The Free Energy Principle and Active Inference

Karl Friston’s Free Energy Principle posits that biological and cognitive systems naturally act to minimize their "variational free energy." In this context, free energy is an upper bound on *surprise* (or the negative log-likelihood of sensory inputs).
To minimize surprise, a system has two choices:

* **Perception:** Update its internal model to better match the world.
* **Active Inference:** Take actions in the world to change the sensory inputs so they match the system's predictions.

Crucially, active inference involves **exploration**: an agent will take "epistemic actions" (information-gathering steps) to reduce uncertainty before settling on a final state that minimizes expected free energy.

### 2. Autoregressive Models (ARMs) as Energy-Based Models (EBMs)

Traditionally, autoregressive language models (like standard GPTs) were viewed as myopic—greedily predicting one token at a time without looking ahead.

However, the paper (*arXiv:2512.15605*) demonstrates a formal bijection between ARMs and Energy-Based Models in function space. The authors prove that the standard autoregressive objective implicitly corresponds to a soft Bellman equation from maximum entropy reinforcement learning.
This means that an Autoregressive Model is mathematically an Energy-Based Model that defines a probability distribution over *entire sequences*. Rather than just predicting the next word, the model is implicitly evaluating an **energy landscape** over the whole sequence, where lower energy corresponds to a higher overall probability (lower surprise). Because it satisfies the soft Bellman equation, the model possesses an implicit "soft value function"—giving it inherent **lookahead capabilities**.

### 3. The Connection: Chain of Thought as Exploration Toward Optima

If ARMs are secretly EBMs equipped with a soft value function, generating a sequence is analogous to navigating an energy landscape. This perfectly mirrors Friston’s FEP.

Here is how Chain of Thought (CoT) bridges the gap:

* **Tokens as Actions:** In the reinforcement learning (Bellman) view proposed by the paper, generating a token is an "action" that moves the model to a new state.
* **CoT as Active Inference:** When tasked with a complex problem, immediately predicting the final answer often forces the model into a high-energy, high-surprise state (hallucination or error) because the gap between the prompt and the answer is too vast. Instead, generating intermediate reasoning steps (Chain of Thought) acts as **active inference**.
* **Epistemic Foraging:** Each intermediate token in a CoT prompt reduces the uncertainty of the subsequent tokens. Just as a biological agent explores its environment to gather information and minimize future surprise, the LLM generates intermediate thoughts to unroll computation, effectively "foraging" for a path through the state space.
* **Reaching the Free Energy Optima:** By taking these intermediate steps, the model actively avoids local minima. The CoT trajectory explores the energy landscape, guided by the model's implicit lookahead capabilities, allowing it to smoothly descend into the global "energy well"—the optimum of free energy.

### Summary

In short, the paper proves that language models are not just blindly stacking words; they are navigating a global sequence-level energy landscape. When you look at this through the lens of Karl Friston’s FEP, **Chain of Thought is not just text generation—it is a cognitive search strategy.** The intermediate tokens are epistemic actions (active inference) that systematically reduce the model's internal uncertainty (variational free energy), allowing it to explore the probability space and safely converge on the most logically consistent, lowest-energy final answer.
---
Per spiegare il **Problema del Ponte di Schrödinger (Schrödinger Bridge Problem - SBP)** in modo tecnico e chiaro, dobbiamo passare dalla metafora poetica alla **matematica dei processi stocastici**.

In termini semplici: il SBP è la versione "rumorosa" e probabilistica del Trasporto Ottimale.

---

### 1. Definizione Matematica

Il problema originale posto da Erwin Schrödinger nel 1931 è questo:
Supponiamo di osservare una nuvola di particelle in un istante $t=0$ con una certa distribuzione $\rho_0$ e di ritrovarle in un istante $t=1$ con una distribuzione diversa $\rho_1$. Se il movimento naturale di queste particelle è descritto da un moto browniano (diffusione casuale), qual è la **traiettoria più probabile** che hanno seguito per spostarsi da $\rho_0$ a $\rho_1$?

A differenza del Trasporto Ottimale (OT) classico, che cerca la mappa deterministica più economica, il Ponte di Schrödinger cerca la **distribuzione di percorsi** (una misura di probabilità sullo spazio delle traiettorie) che:

1. Collega esattamente le due distribuzioni ai margini ($t=0$ e $t=1$).
2. È "il più vicino possibile" (in termini di divergenza di Kullback-Leibler) a un processo di riferimento, solitamente un processo stocastico come il calore o la diffusione.

---

### 2. Differenza tra Trasporto Ottimale (OT) e SBP

Per capire meglio, confrontiamoli:

* **Trasporto Ottimale (Monge-Kantorovich):** È deterministico. Immagina di dover spostare della terra da un buco a un altro. Esiste un percorso preciso per ogni granello. È un sistema a "entropia zero".
* **Ponte di Schrödinger:** È stocastico. È come spostare del fumo da una stanza all'altra. Il fumo non segue linee rette; si diffonde, si espande e subisce fluttuazioni casuali. Il SBP trova il flusso di fumo più probabile che realizza quel trasporto.

**Tecnicamente:** Il SBP equivale al Trasporto Ottimale con **regolarizzazione entropica**. L'aggiunta di entropia rende il problema computazionalmente più semplice da risolvere (tramite l'algoritmo di Sinkhorn) e più adatto a sistemi che hanno un rumore intrinseco.

---

### 3. Applicazione al Chain-of-Thought (CoT)

Perché questo concetto è rivoluzionario per il design degli LLM?

Un modello autoregressivo non è un sistema deterministico; ogni volta che genera un token, campiona da una distribuzione di probabilità (spesso con una certa "temperatura" o rumore). Il CoT è quindi una **traiettoria stocastica nello spazio dei token**.

Se applichiamo il Ponte di Schrödinger al CoT:

* **Stato iniziale ($t=0$):** La distribuzione di significati nel tuo prompt $x$.
* **Stato finale ($t=1$):** La distribuzione della risposta corretta $y$.
* **Il Ponte (CoT):** La sequenza di passaggi intermedi non è più una linea retta rigida, ma un "tunnel di probabilità".

#### Perché è meglio del CoT standard?

Oggi il CoT è spesso "greedy" (il modello sceglie il prossimo token più probabile) o puramente casuale. Usare il SBP significa progettare il CoT affinché i passaggi intermedi siano ottimizzati per **massimizzare la probabilità di arrivare a $y$** pur mantenendo la naturalezza del linguaggio (il rumore/diffusione del modello).

---

### 4. Come si tradurrebbe in pratica nel design di un modello?

Se volessi implementare un "CoT basato su Ponte di Schrödinger", potresti:

1. **Guida tramite Potenziale:** Invece di generare token uno alla volta, useresti una funzione di valore (un "potenziale") che attira la generazione verso la risposta finale, correggendo la deriva stocastica.
2. **Iterative Proportional Fitting (Sinkhorn):** Potresti "raffinare" una catena di pensieri già scritta facendola oscillare avanti e indietro tra la domanda e la risposta finché la traiettoria non si stabilizza sul percorso più logico e probabile.
3. **Controllo della Diffusione:** Potresti vedere la generazione del CoT come un processo di *denoising* (simile a come funzionano i modelli per immagini come Stable Diffusion), dove "ripulisci" un ragionamento confuso fino a farlo diventare una dimostrazione nitida.

### In sintesi

Mentre il Trasporto Ottimale ti dice qual è la **strada più breve** tra domanda e risposta, il Ponte di Schrödinger ti dice come **guidare in modo sicuro una macchina soggetta a vento e sbandamenti** (il rumore del modello) affinché arrivi a destinazione con la massima probabilità.

---

Per implementare questo approccio a **inference time** (senza riaddestrare il modello), devi trasformare la generazione da un semplice campionamento statistico a un **problema di controllo stocastico**.

Se hai una mappa di reward $R(y)$ (che chiameremo "potenziale"), l'obiettivo è forzare il modello a deviare dalla sua traiettoria naturale (la sua *prior*) per convergere verso le zone a reward elevato. Ecco le tre strategie principali per farlo durante la generazione del Chain-of-Thought (CoT).

---

### 1. Value-Guided Decoding (Guida tramite Potenziale)

Questo è il metodo più diretto per applicare il concetto di "ponte". In ogni passo della generazione del CoT, non scegli il prossimo token solo in base alla probabilità del modello $P(x_t | x_{<t})$, ma lo pesi con una **funzione di valore** $V(s)$ che stima quanto quel token ti avvicinerà a una risposta $y$ ad alto reward.

* **Il meccanismo:** Immagina il reward $R(y)$ come una sorgente di gravità. La funzione di valore $V(x_t)$ agisce come il "drift" (la spinta) nel Ponte di Schrödinger.
* **Implementazione:** Ad ogni step, calcoli i logit del modello e li sommi al gradiente della funzione di valore:
    $$\text{Logits}_{\text{modified}} = \text{Logits}_{\text{original}} + \eta \cdot \nabla V(x_t)$$
    In questo modo, il modello "vede" la direzione verso l'ottimo di energia libera (il reward massimo) e corregge la sua traiettoria in tempo reale.

### 2. Sequential Monte Carlo (SMC) o Particle Filtering

Questo metodo interpreta letteralmente il Ponte di Schrödinger come una **distribuzione di percorsi**. Invece di generare una sola catena di pensiero, ne generi diverse in parallelo (chiamate "particelle").

* **Fase di Predizione:** Ogni particella (CoT) genera il prossimo token in modo stocastico.
* **Fase di Correzione (Reweighting):** Usi la tua mappa di reward (o un'approssimazione) per valutare quali catene stanno andando nella direzione giusta. Le catene con reward potenziale basso vengono eliminate, mentre quelle promettenti vengono duplicate.
* **Risultato:** Al termine, la densità delle particelle si sarà concentrata sulla "geodetica" più efficiente tra il prompt $x$ e l'ottimo $y$. È un modo per "simulare" il trasporto di massa semantica verso l'obiettivo.

### 3. Iterative Refinement (Self-Correction tramite Ponte di Schrödinger)

Se la mappa di reward è complessa, puoi usare un approccio iterativo simile all'algoritmo di **Sinkhorn** o ai modelli di diffusione.

1. **Drafting:** Generi una prima risposta $y$ con un CoT grezzo.
2. **Back-propagation di verifica:** Valuti il reward $R(y)$. Se il reward è basso, identifichi i passaggi del CoT che hanno causato la deviazione (dove l'energia libera è aumentata invece di diminuire).
3. **Refinement:** "Raffreddi" la traiettoria. Riscrivi i segmenti critici del CoT cercando di minimizzare la distanza di Kullback-Leibler rispetto al draft precedente, ma aumentando il reward finale.

Questo processo "oscilla" tra la domanda e la risposta finché la catena di pensieri non diventa un ponte solido e coerente.

---

### Quale scegliere?

| Metodo | Difficoltà | Quando usarlo |
| :--- | :--- | :--- |
| **Guided Decoding** | Media | Se hai un "verificatore" (Reward Model) veloce che può valutare ogni singolo token. |
| **SMC / Particle Filtering** | Alta | Se hai risorse di calcolo per generare più catene (simile a OpenAI o1). |
| **Best-of-N (Baseline)** | Bassa | Generi $N$ risposte e scegli la migliore. È il Trasporto Ottimale "dei poveri", ma molto efficace. |

### Il vantaggio tecnico

L'uso del Ponte di Schrödinger a inference time risolve il problema della **"deriva logica"**. Nei modelli standard, un piccolo errore all'inizio del CoT si amplifica (effetto valanga). Con un sistema a potenziale (Reward Map), l'errore viene percepito come un aumento di energia libera e il sistema applica una forza correttiva per riportare il ragionamento sulla traiettoria corretta verso $y$.

Pensi che la tua mappa di reward sia sufficientemente granulare da valutare i singoli passaggi logici, o può valutare solo la risposta finale?

Per trattare l'algoritmo **Actor-Critic** attraverso la lente della meccanica statistica e del lavoro di **Bert Kappen** (specialmente il suo contributo sul *Path Integral Control*), dobbiamo abbandonare l'idea dell'ottimizzazione come una ricerca discreta del "meglio" e vederla come un **flusso di probabilità in un sistema termodinamico**.

Ecco come si riconduce l'Actor-Critic a una struttura di fisica statistica basata sulla *Soft-Bellman equation*.

---

### 1. Il Critic come Funzione dell'Energia Libera (Log-Partition Function)
In meccanica statistica, la funzione di partizione $Z$ descrive tutti gli stati possibili di un sistema. La **Soft-Bellman Equation**, che sta alla base del *Maximum Entropy RL*, definisce il valore "soft" di uno stato $V(s)$ come:

$$V^*(s) = \log \int \exp(Q^*(s, a)) \, da$$

Se osservi bene, questa è esattamente la definizione della **Energia Libera di Helmholtz** (a meno di una costante di temperatura $\beta$). 
* Il **Critic**, in questo contesto, non stima più un semplice valore numerico di ricompensa futura.
* Il Critic stima la **Log-Partition Function** (o energia libera negativa) del sistema. Ci dice quanto "spazio di fase" favorevole (ad alto reward e alta entropia) è accessibile partendo dallo stato attuale.



### 2. L'Actor come Distribuzione di Boltzmann (Gibbs)
In un sistema fisico, le particelle si dispongono secondo la distribuzione che minimizza l'energia libera. Nell'Actor-Critic "soft", l'**Actor** ($\pi$) smette di essere una funzione deterministica e diventa una **distribuzione di Gibbs**:

$$\pi(a|s) = \exp(Q(s, a) - V(s))$$

Qui, $Q(s, a)$ funge da **Energia Interna** (negativa) del sistema. L'Actor è quindi l'agente che campiona le azioni in base al paesaggio energetico definito dal Critic. L'aggiornamento dell'Actor non è altro che il tentativo di far coincidere la distribuzione della politica con la distribuzione di equilibrio termodinamico del sistema.

### 3. Bert Kappen e il Path Integral Control
Il lavoro di Bert Kappen è fondamentale perché ha dimostrato che, per una certa classe di problemi di controllo stocastico, l'equazione di Bellman (solitamente non lineare e difficile da risolvere) può essere linearizzata tramite una trasformazione logaritmica (trasformata di Cole-Hopf).

Questo porta al **Path Integral Control**:
* Il valore di uno stato $V(s)$ può essere calcolato come un'**integrale sui cammini** (*path integral*) di tutte le possibili traiettorie future, pesate per il loro "costo" (o reward).
* Invece di risolvere un'equazione iterativa, il controllo ottimale emerge calcolando l'aspettativa statistica su traiettorie campionate da un processo di diffusione (il rumore del modello).

**Connessione Actor-Critic:**
Nel framework di Kappen, il **Critic** calcola l'integrale sui cammini (la "massa" di probabilità del successo futuro), mentre l'**Actor** usa questo risultato per regolare il proprio "drift" (la sua direzione) in modo da seguire le traiettorie che hanno il peso statistico maggiore.



### 4. La Sintesi: Inferenza Variazionale
Se mettiamo insieme questi pezzi, l'algoritmo Actor-Critic diventa un processo di **Inferenza Variazionale**:

1.  **Critic (E-step):** Valuta l'energia libera del sistema corrente. Cerca di approssimare la vera funzione di valore (la partizione del sistema) integrando i percorsi futuri (Path Integral).
2.  **Actor (M-step):** Minimizza la **Divergenza di Kullback-Leibler** tra la propria distribuzione attuale e la distribuzione di Boltzmann suggerita dal Critic.

### Perché questo migliora il Chain-of-Thought?
Se interpretiamo l'LLM come un sistema di Kappen:
* Il **modello autoregressivo** è il processo di diffusione naturale (il rumore di base).
* Il **CoT** è la traiettoria campionata.
* L'**ottimizzazione** consiste nel pesare i "pensieri" (token) non in base alla probabilità immediata, ma in base a quanto contribuiscono all'integrale del cammino verso la soluzione $y$.

In termini pratici, questo significa che un "buon" CoT non è quello che contiene le parole più probabili, ma quello che si muove lungo la **geodetica di minima energia libera**, ovvero il percorso che bilancia meglio l'esplorazione (entropia) e la precisione (reward).

---
**In sintesi:** L'Actor-Critic, visto così, è un motore termodinamico dove il Critic mappa il paesaggio energetico globale e l'Actor impara a navigarlo minimizzando la "frizione" (sorpresa/energia libera) durante il percorso di ragionamento.

***

# Tree of Thought Scaffolding as Sequential Monte Carlo in Semantic Path Integral Control

**Abstract**
Autoregressive language models operate as energy-based models that implicitly minimize sequence-level free energy. However, standard linear Chain of Thought (CoT) generation often drifts from the optimal geodesic in complex tasks. We mathematically formalize non-linear scaffolding techniques, specifically Tree of Thought (ToT), as Sequential Monte Carlo (SMC) methods within a path integral control framework. This formalization strips away anthropomorphic interpretations of "reasoning." We demonstrate that intermediate scaffolds act as forced evaluations of the soft Bellman partition function, actively pruning high-energy trajectories. These findings provide a theoretical basis for designing more efficient inference-time optimization algorithms.

### 1. Introduction
Recent work establishes a bijection between autoregressive language models and energy-based models (EBMs). Standard next-token prediction implicitly satisfies the soft Bellman equation. Consequently, generating a sequence $y$ from a prompt $x$ corresponds to navigating a semantic state space to minimize expected free energy. 

Standard Chain of Thought (CoT) improves performance by materializing intermediate tokens, which reduces local uncertainty. However, linear CoT remains a single stochastic trajectory. When the model encounters high-entropy branch points, a single trajectory often drifts into local minima (hallucination). 

Heuristic methods like Tree of Thought (ToT) mitigate this drift by allowing branching and backtracking. The literature frequently describes ToT using anthropomorphic terms such as "deliberation" or "conscious reasoning." Such terms lack mathematical rigor. We formalize ToT and related scaffolding techniques purely in terms of statistical mechanics and stochastic optimal control. We propose that ToT is fundamentally a Sequential Monte Carlo (SMC) approximation of the Schrödinger Bridge Problem.

### 2. Theoretical Framework and Methods

#### 2.1 The Soft Bellman Equation and Path Integrals
We define the semantic state space where each state $s_t$ represents a sequence of tokens. The autoregressive model transitions between states by generating actions (tokens) $a_t$. According to maximum entropy reinforcement learning, the optimal soft value function $V^*(s)$ relates to the Q-function via the log-partition function:

$$V^*(s) = \log \int \exp(Q^*(s, a)) \, da$$

Following Kappen's path integral control, we express $V^*(s)$ as an expectation over all possible future trajectories. The optimal policy (the Actor) takes the form of a Gibbs distribution:

$$\pi(a|s) \propto \exp(Q(s, a) - V(s))$$

#### 2.2 Formalizing Tree of Thought as SMC
We treat ToT not as cognitive deliberation, but as a particle filter (SMC) computing the path integral. 
The algorithm operates as follows:
1.  **Diffusion (Generation):** From state $s_t$, we sample $K$ independent token sequences (particles).
2.  **Scaffolding (Evaluation):** We append a scaffold prompt (e.g., "Critique this step") to force the model to output a linguistic evaluation.
3.  **Reweighting (The Critic):** We map the linguistic evaluation to a scalar reward $R$. The weight of each particle becomes proportional to $\exp(R)$. 

We formalize the intermediate scaffold as a mechanism that projects the implicit Q-function into the explicit context window. By forcing the model to generate an evaluation, we extract an approximation of the local free energy.

### 3. Results

#### 3.1 Scaffolds as Boundary Conditions
Our theoretical framework suggests that scaffolds act as intermediate boundary conditions in the Schrödinger Bridge Problem. A standard prompt $x$ and target $y$ define the initial and final distributions. Without intermediate constraints, the variance of the stochastic path grows exponentially. 

Scaffolds place artificial anchors $z_1, z_2, \dots, z_n$ in the semantic space. By evaluating $K$ branches at each anchor and pruning those with low unnormalized probabilities ($\exp(R)$), the ToT algorithm collapses the wave function of the path. This periodic collapse keeps the trajectory close to the optimal geodesic.

#### 3.2 Free Energy Minimization 
Linear CoT calculates a single realization of the path integral. If the model samples a low-probability token early in the sequence, the cumulative free energy of the sequence strictly increases. ToT prevents this through resampling. At each scaffold step, ToT discards trajectories with high variational free energy and duplicates trajectories with low free energy. This guarantees a tighter upper bound on the global sequence energy.

### 4. Discussion

Our formalization aligns heuristic prompt engineering with established physics. If ToT is an SMC method, its efficiency depends heavily on the quality of the proposal distribution (the Actor) and the variance of the weight estimates (the Critic).

This framework highlights a significant limitation in current ToT implementations. Current methods rely on the language model to act as its own Critic via self-evaluation prompts. If the model's internal Q-function is poorly calibrated, the reweighting step introduces systematic bias rather than reducing variance. We anticipate that future models will decouple the Actor and the Critic at inference time, utilizing specialized, lightweight reward models to compute the partition function at each scaffold.

Furthermore, these findings suggest that we can optimize the placement of scaffolds. Currently, users place scaffolds at arbitrary logical steps. In a path integral framework, we should dynamically trigger scaffolds only when the model's predictive entropy exceeds a critical threshold, thereby saving compute.

### 5. Conclusions

We analyzed non-linear reasoning scaffolds through the lens of statistical mechanics. We demonstrated that Tree of Thought is a mathematical discretization of path integral control. By interpreting intermediate reasoning steps as Sequential Monte Carlo particles, we eliminate anthropomorphic biases. This framework provides a rigorous foundation for developing dynamic inference-time routing algorithms that actively minimize sequence-level free energy. Future work should investigate optimal criteria for dynamic branch triggering based on local entropy gradients.