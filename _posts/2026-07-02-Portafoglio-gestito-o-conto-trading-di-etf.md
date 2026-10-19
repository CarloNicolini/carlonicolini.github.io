---
layout: post
title: Portafoglio gestito con tassazione annuale o buy and hold? Simulazione Montecarlo
description: Confronto matematico e Monte Carlo tra la Gestione Patrimoniale Moneyfarm (tassazione annuale sul risultato di gestione) e un conto trading buy-and-hold che replica lo stesso profilo di rischio, con aliquota del 26% sulle plusvalenze.
date: 2026-07-02

published: true
permalink: "/sections/science/2026/07/02/Portafoglio-gestito-o-conto-trading-di-etf.html"
categories:
  - science
  - finance
---
## La domanda

Se investi in Italia con ETF, una scelta che spesso passa in secondo piano è **quando** paghi le imposte sulle plusvalenze. Non è un dettaglio contabile: il momento della tassazione modifica la base su cui compongono gli interessi composti.

Moneyfarm offre due strade principali:

- la **Gestione Patrimoniale (GP)**, in regime di *risparmio gestito*: il risultato complessivo del portafoglio viene tassato ogni anno (tipicamente a fine dicembre), con compensazione delle minusvalenze nei quattro anni successivi;
- il **Conto Trading**, in regime *amministrato*: ogni singolo strumento ha rilevanza fiscale propria; se compri ETF e li tieni senza vendere, la plusvalenza matura solo alla vendita.

La domanda che mi sono posto è semplice da formulare e difficile da rispondere a intuito:

> A parità di rendimento atteso e volatilità, conviene essere tassati **ogni anno** sul risultato di gestione, oppure **rinviare** l'imposta fino alla vendita finale?

In questo post rispondo in due modi: con un **modello matematico chiuso** nel caso deterministico, e con **simulazioni Monte Carlo** in numpy su migliaia di scenari stocastici. Il codice interattivo (plotly + ipywidgets) è nel notebook [`TaxDeferralMonteCarlo.ipynb`](https://github.com/carlonicolini/moneyfarm-cli/blob/main/notebooks/TaxDeferralMonteCarlo.ipynb).

---

## I due regimi in pratica: Moneyfarm e il conto trading

### Gestione Patrimoniale Moneyfarm

La GP opera nel **regime del risparmio gestito**. Moneyfarm agisce da **sostituto d'imposta**: calcola e addebita l'imposta sul *risultato di gestione* maturato nell'anno solare, non sulle singole vendite di ETF. I ribilanciamenti tattici e strategici **non generano plusvalenze fiscali strumento per strumento** — contano solo il saldo complessivo a fine anno.

Punti salienti (dalla [documentazione fiscale di Moneyfarm](https://blog.moneyfarm.com/it/angolo-consulenza/come-funziona-la-tassazione-della-gestione-patrimoniale-moneyfarm/)):

- aliquota sostitutiva fino al **26%** sulle plusvalenze (con riduzione al **12,5%** per la quota derivante da titoli di Stato in white list);
- **minusvalenze compensabili** con plusvalenze future nei **quattro anni successivi**, all'interno della stessa gestione;
- tassazione anche in caso di disinvestimento parziale o totale;
- nessuna commissione da parte degli emittenti ETF: Moneyfarm guadagna solo dal costo del servizio di gestione.

Nel modello semplificato di questo post, la GP corrisponde al **portafoglio A**: tassazione annuale con riporto delle perdite.

### Conto Trading: replicare il portafoglio in buy and hold

Il Conto Trading di Moneyfarm segue il **regime amministrato**: ogni ETF ha una propria posizione fiscale. Se compri una combinazione di ETF che replica approssimativamente il profilo di rischio della GP (stesso livello di azioni/obbligazioni, stessa area geografica) e **non vendi** per ribilanciare, la plusvalenza si cristallizza solo al momento della vendita.

Questo scenario corrisponde al **portafoglio B** del modello: capitali che compoundano senza prelievo fiscale intermedio, con un'unica imposta al tempo $$T$$ sulla plusvalenza netta.

> **Nota importante.** Se nel conto trading vendi per ribilanciare — come fa automaticamente la GP — torni a pagare imposte su ogni vendita in utile. Il vantaggio del differimento vale per una strategia **buy and hold** che accetta una deriva rispetto al benchmark gestito. Qui isoliamo l'effetto fiscale, non il tracking error o il valore aggiunto della gestione attiva.

Moneyfarm stessa, analizzando i portafogli classici dal 2012 al 2025, osserva che l'impatto fiscale medio annuo è **sostanzialmente equivalente** nei due regimi se si chiude tutto a fine periodo — ma il regime gestito diventa più conveniente per profili conservativi e per il livello di rischio 7, dove i cambi di ETF sono più frequenti ([fonte](https://blog.moneyfarm.com/it/angolo-consulenza/qual-e-il-regime-fiscale-piu-adatto-a-chi-investe-la-nostra-analisi/)). Il nostro esperimento complementare isola invece il caso *buy and hold puro* nel conto trading, che è il benchmark naturale per il differimento fiscale.

---

## Il modello matematico

Entrambi i portafogli partono da un capitale $$V_0$$ e seguono lo **stesso percorso di rendimenti** annui $$r_1, \dots, r_T$$. L'aliquota sulle plusvalenze è $$\tau = 0{,}26$$.

### Portafoglio A — tassazione annuale con riporto perdite

Sia $$CF_t$$ il monte minusvalenze riportabili ($$CF_0 = 0$$). Il guadagno lordo nell'anno $$t$$ è $$G_t = V_{t-1}\, r_t$$.

$$
\begin{aligned}
\text{se } G_t < 0:&\quad CF_t = CF_{t-1} + |G_t|,\quad \text{tassabile}_t = 0 \\
\text{se } G_t > 0:&\quad o_t = \min(G_t,\, CF_{t-1}),\quad
  \text{tassabile}_t = G_t - o_t,\quad CF_t = CF_{t-1} - o_t
\end{aligned}
$$

$$
V_t = V_{t-1}(1 + r_t) - \tau\,\text{tassabile}_t
$$

### Portafoglio B — tassazione differita

Il capitale compounda senza imposte intermedie; al tempo $$T$$ si paga una sola volta:

$$
V_t^{\text{pre}} = V_{t-1}^{\text{pre}}(1 + r_t),\qquad
V_T = V_T^{\text{pre}} - \tau\,\max\bigl(V_T^{\text{pre}} - V_0,\,0\bigr)
$$

### Caso deterministico: rendimento costante $$r > 0$$

Senza anni in perdita, il riporto resta vuoto e le formule chiuse sono:

$$
\boxed{\;V_T^A = V_0\bigl(1 + (1-\tau)\,r\bigr)^T\;}
\qquad
\boxed{\;V_T^B = V_0\bigl((1-\tau)(1+r)^T + \tau\bigr)\;}
$$

Il rapporto tra i due patrimoni finali è:

$$
\frac{V_T^B}{V_T^A} = (1-\tau)\left[\frac{1+r}{1+(1-\tau)\,r}\right]^T
$$

Con $$r = 7\%$$, $$\tau = 26\%$$ e $$V_0 = 10\,000$$ €, a $$T = 20$$ anni si ottiene $$V_{20}^A \approx 27\,458$$ € contro $$V_{20}^B \approx 31\,236$$ €: un premio del **13,8%** a favore del differimento, *prima* di considerare la volatilità.

<figure>
<img src="/assets/postfigures/tax_regime_deterministic_premium.png" alt="Confronto deterministico tra patrimonio finale con tassazione annuale e differita, e premio percentuale del differimento">
<figcaption>
<strong>Figura 1: Il premio del differimento cresce con l'orizzonte.</strong>
Nel caso deterministico ($$r = 7\%$$, $$\tau = 26\%$$), il patrimonio finale del portafoglio buy and hold (B, blu) supera progressivamente quello con tassazione annuale (A, rosso). La linea verde tratteggiata mostra il premio percentuale $$V_T^B / V_T^A - 1$$: a 20 anni è circa il 14%, a 40 anni supera il 50%.
</figcaption>
</figure>

**Interpretazione.** La tassazione annuale introduce un *tax drag*: ogni anno una frazione del rendimento positivo esce dal portafoglio e non partecipa più alla capitalizzazione composta. Il differimento, invece, lascia l'intera base investita fino alla vendita e paga l'imposta una sola volta.

### Dove la tassazione annuale può recuperare terreno

Volatilità e riporto perdite spingono nella direzione opposta. Con tassazione annuale, gli anni negativi **cristallizzano minusvalenze** nel pool $$CF$$, che proteggono i guadagni futuri. Nel regime differito le perdite si compensano con i guadagni **una sola volta**, alla fine. Se la volatilità è alta e l'orizzonte breve, il vantaggio del loss harvesting può superare il tax drag.

È esattamente ciò che le simulazioni Monte Carlo quantificano nel passo successivo.

---

## Simulazioni Monte Carlo

### Modello stocastico

I rendimenti annui seguono un **geometric Brownian motion** in forma discreta:

$$
\log(1 + r_t) \sim \mathcal{N}(\mu, \sigma^2)
$$

con $$\mu = 7\%$$ (rendimento atteso annuo) e $$\sigma = 15\%$$ (volatilità annua), valori plausibili per un portafoglio azionario diversificato. Generiamo $$N = 50\,000$$ scenari indipendenti su $$T = 20$$ anni e applichiamo le regole fiscali A e B allo **stesso** percorso di rendimenti, così il confronto è pulito.

### Distribuzione del patrimonio finale

<figure>
<img src="/assets/postfigures/tax_regime_terminal_wealth.png" alt="Distribuzione del patrimonio finale dopo 20 anni per i due regimi fiscali">
<figcaption>
<strong>Figura 2: Il differimento sposta l'intera distribuzione verso l'alto.</strong>
Densità kernel del patrimonio finale a $$T = 20$$ anni ($$\mu = 7\%$$, $$\sigma = 15\%$$, $$N = 50\,000$$). Le linee tratteggiate indicano le mediane: circa 28.500 € (A) vs 32.600 € (B). La coda sinistra del portafoglio annuale è leggermente più pesante perché il tax drag riduce anche la capacità di recupero dopo gli anni negativi.
</figcaption>
</figure>

I risultati numerici per i parametri di base:

| metrica | gestione annuale (A) | buy and hold (B) |
|---|---|---|
| patrimonio medio | 32.505 € | 40.054 € |
| premio medio | — | +23,2% |
| $$\mathbb{P}(B > A)$$ | — | **99,8%** |
| differenza mediana | — | +4.161 € |

A parità di sorteggio di mercato, il differimento vince in quasi tutti gli scenari.

### Traiettorie nel tempo

<figure>
<img src="/assets/postfigures/tax_regime_wealth_paths.png" alt="Traiettorie mediane e banda interquartile del patrimonio nel tempo per i due regimi">
<figcaption>
<strong>Figura 3: Il divario si apre già nei primi anni e non si chiude.</strong>
Mediana (linea continua) e banda interquartile (area ombreggiata) del patrimonio nel tempo. Il portafoglio differito (blu) separa progressivamente quello con tassazione annuale (rosso): il tax drag è cumulativo, non un effetto che si annulla aspettando.
</figcaption>
</figure>

### Griglia di scenari: volatilità × orizzonte

Per mappare il *crossover* tra i due regimi, abbiamo fatto scorrere la volatilità $$\sigma \in [0\%, 40\%]$$ e l'orizzonte $$T \in [1, 30]$$ anni su $$N = 10\,000$$ simulazioni per cella.

<figure>
<img src="/assets/postfigures/tax_regime_heatmaps.png" alt="Heatmap del vantaggio atteso e della probabilità che il differimento batta la tassazione annuale">
<figcaption>
<strong>Figura 4: Dove vince il differimento e dove la tassazione annuale può competere.</strong>
A sinistra, il vantaggio atteso $$\mathbb{E}[V_B - V_A]$$ in euro (rosso = differimento migliore). A destra, la probabilità $$\mathbb{P}(V_B > V_A)$$. Per orizzonti superiori a 10 anni e volatilità tipica di un portafoglio diversificato ($$\sigma \lesssim 20\%$$), il differimento domina. Solo con volatilità molto alta e orizzonti brevi (angolo in alto a sinistra) la compensazione annuale delle perdite riduce il divario.
</figcaption>
</figure>

---

## Cosa significa per la scelta tra GP e Conto Trading

Il quadro che emerge dal modello — coerente con l'intuizione finanziaria classica sul *tax drag* — è il seguente.

**Il differimento fiscale del buy and hold è un vantaggio strutturale** per chi investe a lungo termine con un portafoglio diversificato. Con $$\mu \approx 7\%$$, $$\sigma \approx 15\%$$ e un orizzonte di 20 anni, il premio atteso supera il 20% del patrimonio finale, e la probabilità che il conto trading batta la GP sul solo fronte fiscale è vicina al 100%.

**La Gestione Patrimoniale ha però altri meriti** che questo modello non cattura:

- **ribilanciamento automatico** senza dover decidere quando vendere;
- **gestione fiscale integrata** (compensazione minusvalenze tra strumenti diversi, impossibile nel regime amministrato tra ETF e fondi);
- **semplicità operativa** (nessuna dichiarazione dei redditi per gli investimenti in GP);
- per profili ad alta rotazione, Moneyfarm stessa documenta un vantaggio fiscale del regime gestito rispetto all'amministrato con ribilanciamenti frequenti.

**Il Conto Trading in buy and hold** conviene fiscalmente se:

- accetti una deriva rispetto al benchmark gestito (nessun ribilanciamento);
- hai un orizzonte lungo (10+ anni);
- non incassi dividendi rilevanti (non modellati qui);
- sei disposto a gestire autonomamente la composizione del portafoglio.

### Limiti del modello

Questo è uno studio **didattico**, non una consulenza fiscale:

- aliquota piatta al 26%, senza distinzione titoli di Stato / corporate bond;
- nessun costo di gestione Moneyfarm, commissioni di acquisto ETF, spread;
- nessun dividendo o cedola (tassati annualmente in entrambi i regimi);
- rendimenti i.i.d. gaussiani in log-space, senza autocorrelazione o regimi di mercato;
- il portafoglio B non ribilancia mai: appena si vende per ribilanciare nel conto trading, si torna verso il regime A.

---

## Conclusione

La matematica del caso deterministico e le simulazioni Monte Carlo raccontano la stessa storia: **rinviare la tassazione sulle plusvalenze è un vantaggio composto che cresce con l'orizzonte temporale**. Per un investitore italiano che replica un portafoglio Moneyfarm in ETF sul Conto Trading e li tiene senza vendere, il risparmio fiscale atteso su 20 anni è dell'ordine di diverse migliaia di euro su 10.000 € investiti.

La Gestione Patrimoniale resta la scelta ragionevole per chi vuole delegare ribilanciamento, ottimizzazione fiscale *intra-gestione* e semplicità operativa — ma va consapevole che la liquidazione annuale delle imposte ha un costo opportunità misurabile. La domanda non è "quale regime è sempre migliore", ma **quanto vale per te** la gestione attiva rispetto al premio fiscale del buy and hold.

Il notebook interattivo con plotly e slider per esplorare $$\mu$$, $$\sigma$$, $$T$$ e $$\tau$$ è disponibile nel repository [moneyfarm-cli](https://github.com/carlonicolini/moneyfarm-cli).

---

*Disclaimer: questo articolo ha finalità illustrative e non costituisce consulenza finanziaria o fiscale. Gli investimenti in strumenti finanziari comportano rischi, inclusa la possibilità di perdere il capitale investito.*
