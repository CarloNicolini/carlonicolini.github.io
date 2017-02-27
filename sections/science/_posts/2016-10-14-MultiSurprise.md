---
layout: post
title: Extending Surprise to multivariate hypergeometric
categories: science
published: false
date: 2016-10-14
---

Surprise is defined as

$$ S = \sum \limits_i ^{m_\zeta} \dfrac{\binom{p_\zeta}{i}  \binom{p-p_\zeta}{m-i} }{\binom{p}{m}}$$

but this counts only *intra-* and *extra-* cluster totals edges and pairs.
One can consider a multivariate distribution, like this that we call **MultiSurprise**

$$S_M = \prod \limits_c \dfrac{\binom{p_c}{m_c}}{\binom{p}{m}}$$

this, once approximated with Kullback-Leibler divergence becomes

$$S_M \approx m D_{KL}(\mathbf{q} \| \left< \mathbf{q}\right>)$$

or in other words:

$$ m D_{KL}(\mathbf{q} \| \left< \mathbf{q}\right>) = m \sum_c \dfrac{m_c}{m} \log\left(\dfrac{m_c/m}{p_c/p} \right)$$

and we call this measure Asymptotical MultiSurprise.
Whether this measure works, I don't know...for sure it's working in the ring of cliques example though.

This is very similar to the stochastic block model introduced by Newman and Karrer, that instead has the sum of pairs of blocks (rather than just on the diagonal as MultiSurprise):

$$\mathcal{L}(G) = \sum \limits_{rs} \dfrac{m_{rs}}{2m}\log\left( \dfrac{m_{rs}}{n_r n_s/n^2}\right)$$

because in this model on undirected graphs pairs of blocks are counted, then the $$2$$ factor, so if one considers only community structure of blocks and on undirected graphs:

$$\mathcal{L}(G | g) = \sum \limits_{r} \dfrac{m_{r}}{m}\log\left( \dfrac{m_{r}}{p_r}\right)$$

If one continues to read the Karrer and Newman paper, then the stubs are considered instead of vertex pairs, and the degree-corrected stochastic block model is considered, that reads:

$$
\mathcal{L} = \sum \limits_{rs} \dfrac{m_{rs}}{2m} \log \left( \dfrac{m_{rs}/2m}{(k_r/2m)(k_s/2m)}\right)
$$

coming back with the reasoning, consider only $$r==s$$, then this becomes focused on communities:

$$
\mathcal{L}_C = \sum \limits_{r} \dfrac{m_{r}}{m} \log \left( \dfrac{m_{rs}/2m}{(k_r/2m)^2}\right)
$$

multiply by $$m$$:

$$
m \mathcal{L}_C = mD_{KL}(\mathbf{q} \| \left< \mathbf{q}\right>)
$$

where here $$\mathbf{q}=(m_{11}/m, m_{12}/m, \ldots, m_{cc}/m)$$ and 
$$\left< \mathbf{q} \right >=(m_{11}/m, m_{12}/m, \ldots, m_{cc}/m)$$ and 

therefore its original distribution is:

$$S_{CM} = \prod \limits_c \dfrac{\binom{p_c}{m_c}}{\binom{p}{m}}$$

Notes on asymptotical surprise
========

The G-test (in fact a likelihood ratio) has the form 

$$
G = 2 \sum_i O_i \log( O_i/E_i)
$$

where $O_i$ is the observed count in a cell, $E_i$ is the expected count under the null hypothesis and the sum is taken over all non-empty cells.

It's related to Kullback-Leilbler divergence when the empirical and theoretical frequencies $$o_i$$ and $$e_i$$ are taken instead of the counts:

$$
G = 2 \sum_i O_i \log(O_i/E_i) = 2 N \sum_i o_o \log(o_i/e_i) = 2N D_{KL}(o\vbar e)
$$
with $$N$$ denoting the total number of observations.

it's also related to mutual information, in fact, if one expresses $$ N= \sum_{ij} O_{ij}$$

$$\pi_{ij} = O_{ij}/N $$
$$\pi_{i \cdot } = \sum_j O_{ij}/N$$

$$\pi_{\cdot j}=\sum_i O_{ij}/N$$

then $$G$$ can be expressed in several alternative forms:

$$
G=2\cdot N\cdot \sum _{ij}{\pi _{ij}\left(\ln(\pi _{ij})-\ln(\pi _{i\cdot })-\ln(\pi _{\cdot j})\right)},
$$


$$G = 2 ⋅ N ⋅ [ H ( r ) + H ( c ) − H ( r , c ) ] , {\displaystyle G=2\cdot N\cdot \left[H(r)+H(c)-H(r,c)\right],} G=2\cdot N\cdot \left[H(r)+H(c)-H(r,c)\right]
$$


$$G = 2 ⋅ N ⋅ M I ( r , c ) , {\displaystyle G=2\cdot N\cdot MI(r,c)\,,} G=2\cdot N\cdot MI(r,c)
$$

MAIL GARLASCHELLI
========

Caro Diego,

Dopo la chiaccherata con te, tornato in Italia, ho ripensato al discorso di come adattare la Surprise al configuration model, perchè se ne valesse la pena avremmo una funzione costo molto potente.

Iniziamo con un po’ di notazione:
- $$G$$ grafo undirected, unweighted, no self-loops, no multiedges.
- $$n$$ numero di nodi del grafo.
- $$m$$ numero di lati del grafo.
- $$C$$ è il numero di comunità (o blocchi).
- $$c$$ è indice di comunità (o blocco).
- $$p$$ numero di coppie di vertici del grafo $$p=\binom{n}{2}$$.
- $$n_c$$ numero di nodi nella comunità $$c$$.
- $$m_c$$ numero di lati nella comunità $$c$$.
- $$p_c$$ numero di coppie di vertici nella comunità $$c$$.
- $$m_\zeta$$ numero totale di lati intracluster, $$m_\zeta=\sum_c m_c$$.
- $$p_\zeta$$ numero totale di coppie intracluster, $$p_\zeta=\sum_c p_c$$.
- $$p-p_\zeta$$ numero totale di coppie extracluster.
- $$m-m_\zeta$$ numero totale di lati extracluster.

Partiamo dalla definizione originale di Surprise che nella sua formulazione originale è basata sulla distribuzione cumulativa inversa ipergeometrica [[Aldecoa 2011](#Aldecoa2011)],

$$
S = -\log \left( \sum_{i=m_\zeta}^m  \dfrac{\binom{p_\zeta}{i}\binom{p-p_\zeta}{m-i}}{\binom{p}{m}} \right)
$$

Il null model implicito su cui è basata la Surprise è il modello $$G_{nm}$$ (e non Erdos-Renyi $$G_{np}$$) perchè il numero di lati è fissato a $$m$$ (è una versione microcanonica dell'insieme $$G_{np}$$ in fondo).
La cardinalità dell'insieme $$G_{nm}$$ con esattamente $$n$$ nodi ed $$m$$ lati viene rappresentata al denominatore della Surprise dal fattore

$$\binom{p}{m}^{-1}$$

ovvero esso è la cardinalità dell’insieme di tutti i possibili grafi con esattamente $$m$$ lati e $$p=\binom{n}{2}$$ coppie di lati, o se vuoi vederla diversamente, $$m$$ coppie di vertici connesse da un lato e $$p$$ coppie di vertici totali. 
A quanto ne so io comunque i due insiemi $$G_{nm}$$ (Gilbert) e $$G_{np}$$ (Erdos-Renyi) sono simili per $$n$$ grande.

Ora per semplificarci la vita consideriamo solamente il termine dominante di $$S$$ tenendo solo il primo termine della sommatoria $$i=m_\zeta$$ ed indichiamo il risultato con $$S_D$$. Otteniamo quindi:

$$
S \approx S_{D} = -\log \left( \dfrac{\binom{p_\zeta}{m_\zeta}\binom{p-p_\zeta}{m-m_\zeta}}{\binom{p}{m}} \right)
$$

e questo è anche quello che fa Traag nel suo paper [[Traag 2015](#Traag2015)] dove ricava la Asymptotical Surprise.

In questa formulazione discreta, Surprise ti dice qual'è la probabilità che, pescando $$m$$ palle da un'urna contenente $$p$$ palle, di cui $$p_\zeta$$ bianche e $$p-p_\zeta$$ nere, tu abbia in mano *esattamente* $$m_\zeta$$ palle bianche.

Questa descrizione dal punto di vista statistico è un Fisher test esatto, che ti dice quanto confidentemente si può rigettare l'ipotesi nulla che la densità intracluster density $$m_\zeta/p_\zeta$$ sia uguale alla densità del grafo $$m/p$$. Teniamolo in mente per dopo.

Notiamo ora che in questa formulazione noi stiamo considerando solamente due tipi di popolazioni, cioè la popolazione delle coppie intracluster e quella delle coppie extracluster.

Questo fatto si riflette nella formulazione asintotica della Surprise, la Asymptotical Surprise che fa uso della divergenza di Kullback-Leibler binaria sulle frequenze relative osservata ed aspettata della popolazione intracluster e della popolazione extracluster.

$$
S_A = m D_{KL}(q \| \left< q\right>) 
$$

dove in questo caso $$D_{KL}(x \| y)=x \log(x/y) + (1-x) \log( (1-x)/(1-y) )$$.

Parlando con te mi avevi fatto notare che questo ha anche un altro parallelo in statistica, il likelihood-ratio. Spulciando qua e là ho scoperto che la statistica nota come G-test prende esattamente la forma che ci piace e cioè, date $$N$$ osservazioni, di cui $$O_i$$ è il numero di conteggi osservati, $$E_i$$ il numero di conteggi aspettati dati un certo modello nullo, allora il valore $$G$$ si scrive come:

$$
G=2 \sum_i O_i \log \left(\dfrac{O_i}{E_i} \right)
$$

e questa statistica $$G$$ è intimamente collegata alla divergenza KL perchè

$$G=2 \sum_i O_i \log(\dfrac{O_i}{E_i}) = 2N \sum_i o_i \log(\dfrac{o_i}{e_i})$$

dove, le frequenze relative osservate ed aspettate sono $$o_i$$ ed $$e_i$$.
Questo è interessante di per se e lo useremo come fatto utile fra un po', ma torniamo un secondo alla Surprise.

Come detto prima, la Surprise ha due proprietà principali. La prima è che la popolazione delle biglie nell'urna è di due tipi: intracluster ed extracluster. Da questo deriva il fatto che si modella con una distribuzione ipergeometrica, approssimata da binomiale, riconducibile a KL binaria.
Se si considera invece un estensione ipergeometrica multivariata $$S_M$$, definita come:

$$
S_{M} = -\log \left( \prod_{rs} \dfrac{\binom{n_r n_s}{m_{rs}} } {\binom{p}{m}} \right)
$$

allora questo mette in evidenza che la definizione originale è una sorta di marginalizzazione (forse non è il termine esatto) su questa versione multivariata.
Quest'ultima definizione di Surprise che è stata introdotta da Traag nel lavoro sulla Asymptotical Surprise (nell'ultima parte del lavoro), ha anch'essa una versione asintotica (indicata qui come $$S_{MA}$$) che si scrive come:

$$
S_{MA} = \sum_{rs} m_{rs} \log \left( \dfrac{m_{rs}}{n_r n_s} \right)
$$

Ora, questa *likelihood* è una divergenza KL ed era stata già proposta da Newman in un lavoro sui stochastic block models [[Karrer 2011](#Karrer20122)]. In quel lavoro era stato notato che questa $$S_{MA}$$ tendeva a raggruppare nella stessa comunità i nodi con degree alto, poichè come è evidente non tiene in conto la degree sequence, infatti nel modello $$G_{nm}$$ non vi è assolutamente nessuna menzione esplicita dei degree, la rete è considerata uniforme (in media).

Newman allora aveva provato a sostituire al posto del numero di nodi dei blocchi $$n_r$$ e $$n_s$$, le somme dei degree dei nodi dei blocchi $$r$$ ed $$s$$, indicati con $$K_r$$ e $$K_s$$, ottenendo quello che lui ha chiamato degree-corrected stochastic block model, che qui indico con $$\mathcal{L}_{DCSBM}$$: 

$$
\mathcal{L}_{DCSBM} = \sum_{rs} m_{rs} \log \left( \dfrac{m_{rs}}{K_r K_s} \right)
$$

Incorporando la degree-sequence, implicitamente in questa funzione vengono assegnate probabilità più alte ai lati i cui endpoints hanno degree alto e questo dà la possibilità di fittare reti con una maggiore likelihood.
In particolare, aggiungendo e moltiplicando termini costanti, si puó riscrivere $$\mathcal{L}_{DCSBM}$$ in una forma basata sulla divergenza KL come una likelihood normalizzata:

$$
\mathcal{L}_{DCSBM} = \sum_{rs} \frac{m_{rs}}{2m} \log \left( \dfrac{m_{rs}/2m}{(K_r/2m) (K_s/2m)} \right)
$$

Ragionando su questo ultimo passaggio, il messaggio che contiene è che qui si passa dal considerare le **coppie** di vertici a considerare gli **stubs**.

Infatti questo con un po' di intuizione corrisponderebbe ad un modello ad urna senza rimpiazzo (o con rimpiazzo non è importante se la rete è grande) con un totale di $$c^2/2$$ possibili tipi di palle (il fattore 2 perchè consideriamo il numero di lati dal blocco $$r$$ al blocco $$s$$ uguale al numero di lati dal blocco $$s$$ al blocco $$r$$, cioè il sopragrafo dei blocchi è undirected). Risulterebbe una cosa del genere:

$$
S_{CM} = -\log \left( \prod_{rs}  \dfrac{\binom{K_r K_s}{m_{rs}}}{\textrm{const}} \right) \approx S_{DCSBM}$$

dove $$\textrm{const}$$ è una costante di normalizzazione che dopo averci ragionato per parallelismo con la definizione di Surprise data prima, dovrebbe essere data dal numero di possibili grafi che possono esistere nel configuration model con degree sequence $$\{k_1, \ldots ,k_n\}$$.
Da argomenti combinatoriali [[Radicchi 2010](#Radicchi2010)] risulta che la cardinalità $$| \Omega_{CM}|$$ del configuration model data tale degree sequence, cioè il numero totale di possibili rewirings date la degree sequence, si calcola con il coefficiente multinomiale:

$$
| \Omega_{CM} | = \binom{2m}{k_1, \ldots k_n} = \dfrac{(2m)!}{\prod \limits_i^n (k_i)!}
$$

Questo vorrebbe dire che, riconsiderando tutto quanto detto finora, possiamo ottenere una forma di Surprise adattata al configuration model che in definitiva sarebbe data da:

$$
S_{CM} = -\log \left( \prod_{rs} \dfrac{ \binom{K_r K_s}{m_{rs}}}{\binom{2m}{k_1, \ldots k_n}} \right)
$$

In questa definizione risulta che stiamo comparando il numero di combinazioni possibili una volta stabilita una partizione (termine al numeratore) con la cardinalità totale del configuration model al denominatore. In altre parole, stiamo valutando con quale grado di confidenza possiamo rigettare l'ipotesi nulla che 


Proviamo a farci un esempio pratico, consideriamo quanto varrebbe per un grafo composto da due cliques di 5 nodi unite da un lato e partizionato con le due cliques come due comunità separate $$A$$ e $$B$$.
Facendo due conti $$K_A = K_B = 20$$, $$m_{AA}=10$$, $$m_{AB}=1$$, $$m_{BB}=10$$, $$m=21$$, $$k=[5,5,5,5,6,6,5,5,5,5]$$.
Mettiamo nella formula:

$$
S_{CM} = -\log \left( \frac{\binom{K_A K_A}{m_{AA}} \binom{K_A K_B}{m_{AB}} \binom{K_B K_A}{m_{BA}} \binom{K_B K_B}{m_{BB}} }{\binom{42}{5,5,5,5,6,6,5,5,5,5} } \right) 
$$

$$
= -\log \left( \frac{\binom{26^2}{10} \binom{26^2}{1} \binom{26^2}{1} \binom{26^2}{10} }{\binom{42}{5,5,5,5,6,6,5,5,5,5} } \right) 
$$

$$
= - \left (49.991 + 6.516 + 6.516 + 49.991 - 104.902 \right ) = - 8.11
$$
ma questo essendo negativo ci dice che la formula è sbagliata, in quanto dovremmo ottenere un numero positivo perchè l'argomento del logaritmo sia una probabilità in $$[0,1]$$.

Usiamo allora la forma

$$
S_{CM} = -\log \left( \prod_{rs} \dfrac{ \binom{K_r K_s}{m_{rs}}}{\binom{4m^2}{2m}} \right)
$$

ci risulta allora:

$$
S_{CM} = -\log \left( \frac{\binom{K_A K_A}{m_{AA}} \binom{K_A K_B}{m_{AB}} \binom{K_B K_A}{m_{BA}} \binom{K_B K_B}{m_{BB}} }{\binom{4 \times 21^2}{42} } \right) \approx 94.32
$$

che come cosa ha già più senso. Mi resta peró inspiegabile il perchè del fattore al denominatore $$\binom{4m^2}{2m}$$.

$$
\mathcal{L} = 2 \frac{m_{AA}}{2m}\log \left[ \frac{(m_{AA}/2m)}{(K_A/2m)(K_A/2m)} \right] + 
2\frac{m_{AB}}{2m}\log \left[ \frac{(m_{AB}/2m)}{(K_A/2m)(K_B/2m)} \right] 
$$

## Referenze
- <a name="Aldecoa2011"></a>Aldecoa R., Marin I. "Deciphering Network Community Structure by Surprise", Plos One, (2011)
- <a name="Traag2015"></a> Traag V.A, Aldecoa R., Delvenne J.C. "Detecting communities using Asymptotical Surprise", PRE, (2015)
- <a name="Karrer2011"></a>Karrer B., Newman M.E.J. "Stochastic blockmodels and community structure in networks", PRE, 2011
- <a name="Radicchi2010"></a>Radicchi F., Lancichinetti A., Ramasco J. "Combinatorial approach to modularity" PRE 82, 026102 (2010).