---
layout: post
title: 'SAT solver tramite una rete neurale'
description: 'Introduzione  ad una variante del modello NeuroSAT usato nel progetto RYS: letterali, clausole, matrici di incidenza, stati latenti, output e rumore stocastico'
date: 2026-06-11

published: true
permalink: "/sections/science/2026/06/11/Message-Passing-NeuroSAT-Solver.html"
categories:
  - science
  - ai
  - math
---
Il punto più interessante di NeuroSAT {% cite selsam2019neurosat %} non è che una rete neurale possa classificare formule SAT.
La cosa curiosa è il modo in cui ci riesce. Addestrato con un solo bit, soddisfacibile oppure insoddisfacibile, il modello sviluppa una dinamica interna da cui spesso si può estrarre un assegnamento vero e proprio.

Questa osservazione cambia il modo di guardare un risolutore neurale.
Una formula SAT smette di essere una stringa logica e diventa un sistema dinamico: letterali e clausole hanno stati latenti, si scambiano messaggi, attraversano una fase di assestamento, poi alcuni stati si separano abbastanza da codificare una soluzione discreta.

Il codice in `sat_message_passing.py` vive in questa famiglia.
Riprende l'idea di NeuroSAT, ma la adatta al progetto RYS.
Ogni round di message passing è esposto come un layer ordinario in `model.model.layers`, così può essere ripetuto, misurato con CKA e trattato come una piccola ricorrenza controllata.

La notazione del paper NeuroSAT aiuta a raccontare il modello in modo più pulito. Partiamo da lì.

## La notazione di NeuroSAT

Una formula CNF è una congiunzione di clausole. Ogni clausola è una disgiunzione di letterali:

$$
\Phi = \bigwedge_{a=1}^{m} c_a
$$

Per una formula 3-SAT, ogni clausola contiene tre letterali:

$$
c_a = \ell_{a,1} \vee \ell_{a,2} \vee \ell_{a,3}
$$

Un letterale è una variabile o la sua negazione. Se ci sono $$n$$ variabili, la rappresentazione di NeuroSAT usa $$2n$$ nodi-letterale:

$$
x_1, \neg x_1, x_2, \neg x_2, \dots, x_n, \neg x_n
$$

A ogni round $$t$$, NeuroSAT mantiene due matrici di stato:

$$
L_t \in \mathbb{R}^{2n \times d}
$$

$$
C_t \in \mathbb{R}^{m \times d}
$$

La matrice $$L_t$$ contiene un vettore per ogni letterale. La matrice $$C_t$$ contiene un vettore per ogni clausola. Il legame tra i due insiemi è codificato da una matrice di incidenza:

$$
M \in \{0,1\}^{2n \times m}
$$

con:

$$
M_{i,a}=1
\quad \text{se il letterale } i \text{ compare nella clausola } a
$$

Questa notazione è bella perché separa tre oggetti: lo stato dei letterali, lo stato delle clausole, la geometria del problema. I pesi della rete non dipendono dal numero di variabili o clausole. La dimensione del problema entra solo attraverso $$M$$ e attraverso le somme sui vicini.

Un round di NeuroSAT può essere letto così:

$$
C_{t+1} = \operatorname{Update}_C(C_t, M^\top \operatorname{Msg}_L(L_t))
$$

$$
L_{t+1} = \operatorname{Update}_L(L_t, \operatorname{Flip}(L_t), M \operatorname{Msg}_C(C_{t+1}))
$$

`Flip` è l'operatore che scambia ogni letterale con il suo complementare: $$x_i$$ con $$\neg x_i$$. Serve a rendere esplicita la simmetria di negazione. Il nostro codice usa una rappresentazione leggermente diversa, quindi questo operatore non compare come matrice dedicata. Il ruolo del segno viene assorbito dagli embedding `literal_sign` e `message_sign`.

## La variante nel codice RYS

In `sat_message_passing.py`, la matrice $$L_t$$ con $$2n$$ letterali viene sostituita da una matrice di variabili:

$$
V_t \in \mathbb{R}^{n \times d}
$$

e una matrice di clausole:

$$
K_t \in \mathbb{R}^{m \times d}
$$

Il segno del letterale viene passato come dato separato. In pratica, il nodo è la variabile; il segno modifica il messaggio lungo l'arco. La formula:

$$
(x_1 \vee \neg x_2 \vee x_3)
\wedge
(\neg x_1 \vee x_2 \vee \neg x_3)
$$

entra nel modello con tre tensori:

```python
clause_variable_ids = torch.tensor([[
    [1, 2, 3],
    [1, 2, 3],
]])

clause_sign_ids = torch.tensor([[
    [1, 2, 1],  # x1, not x2, x3
    [2, 1, 2],  # not x1, x2, not x3
]])

clause_mask = torch.tensor([
    [1, 1],
])
```

La convenzione è questa: nei segni, `1` indica un letterale positivo, `2` un letterale negato, `0` padding. Gli indici delle variabili sono uno-based nell'input, per cui `1` indica $$x_1$$. Il codice li converte subito in indici zero-based:

```python
var_idx = (clause_variable_ids - 1).clamp_min(0)
slot_valid = (clause_variable_ids > 0).to(clause_variable_ids.dtype)
slot_valid = slot_valid * clause_mask.unsqueeze(-1)
```

Sul nostro esempio:

```python
var_idx = torch.tensor([[
    [0, 1, 2],
    [0, 1, 2],
]])
```

La matrice $$M$$ del paper NeuroSAT qui non viene materializzata come matrice sparsa. È implicita in `var_idx`. Le operazioni `gather` e `scatter_add` fanno il lavoro che, nella notazione del paper, viene scritto come moltiplicazione per $$M^\top$$ e $$M$$.

Questo è il primo cambio narrativo utile: invece di pensare al modello come a una rete che “legge tensori”, conviene vederlo come una rete che implementa due moltiplicazioni sparse mascherate. Prima aggrega variabili dentro le clausole. Poi redistribuisce clausole verso variabili.

## Padding: clausole che esistono solo per il batch

I batch contengono formule di dimensioni diverse. Per allineare i tensori, alcune clausole vengono riempite con zeri:

```python
clause_variable_ids = torch.tensor([[
    [1, 2, 3],
    [0, 0, 0],
]])

clause_sign_ids = torch.tensor([[
    [1, 2, 1],
    [0, 0, 0],
]])

clause_mask = torch.tensor([
    [1, 0],
])
```

La seconda clausola è fittizia. Dopo la costruzione del contesto:

```python
slot_valid = torch.tensor([[
    [1., 1., 1.],
    [0., 0., 0.],
]])
```

Gli archi della clausola fittizia vengono spenti. La rete può così processare formule di lunghezza diversa senza far entrare il padding nel ragionamento.

## Lo stato iniziale

Il backbone costruisce gli stati iniziali così:

```python
var_states = self.var_init.view(1, 1, d).expand(batch, self.config.max_vars, d)
clause_states = self.clause_init.view(1, 1, d).expand(batch, n_clauses, d)
hidden = torch.cat([var_states, clause_states], dim=1).contiguous()
```

Tutte le variabili partono dallo stesso vettore appreso. Tutte le clausole partono da un altro vettore appreso. Questa scelta preserva l'equivarianza per permutazione: rinominare le variabili o riordinare le clausole non introduce identità artificiali.

Esiste una modalità `var_id_embeddings`, dove ogni variabile riceve un embedding distinto. È una scelta più espressiva, però abbandona la simmetria pura della rappresentazione. Per un testbed RYS, la simmetria è preziosa: se il modello generalizza a formule più grandi, vogliamo che lo faccia usando la struttura del grafo, non la memoria degli indici.

Il tensore `hidden` concatena variabili e clausole:

$$
H_t = [V_t, K_t]
$$

Questo dettaglio serve per compatibilità con RYS. Ogni round deve comportarsi come un layer che riceve `hidden` e restituisce `hidden`.

## Primo mezzo round: da variabili a clausole

Il primo passaggio corrisponde, nella notazione NeuroSAT, a qualcosa del tipo:

$$
M^\top \operatorname{Msg}_L(L_t)
$$

Nel codice RYS diventa un `gather` sugli stati delle variabili:

```python
var_for_msg = self.var_norm(var_states) if self.pre_norm else var_states
flat_idx = ctx.var_idx.reshape(batch, n_clauses * arity, 1).expand(batch, n_clauses * arity, d)
gathered = torch.gather(var_for_msg, 1, flat_idx).reshape(batch, n_clauses, arity, d)
```

`gathered` ha forma:

```python
(batch, n_clauses, arity, d)
```

Per ogni clausola contiene i tre vettori delle variabili che vi compaiono. A questo punto il modello aggiunge il segno:

```python
literals = self.literal_in(gathered) + self.literal_sign(ctx.sign_ids)
literals = literals * ctx.slot_valid.unsqueeze(-1)
clause_message = literals.sum(dim=2)
```

Con una formula breve:

$$
M_K = \sum_{\text{slot della clausola}} \operatorname{Msg}_V(V_t, \text{segno})
$$

Il pedice $$K$$ indica che il messaggio è destinato alle clausole. La somma sui tre slot è l'aggregazione locale. L'embedding di segno permette alla stessa variabile di produrre messaggi diversi quando appare come $$x_i$$ o come $$\neg x_i$$.

La clausola aggiorna il proprio stato concatenando lo stato corrente e il messaggio appena ricevuto:

```python
clause_in = self.clause_norm(clause_states) if self.pre_norm else clause_states
clause_states = clause_states + self.clause_update(
    torch.cat([clause_in, clause_message], dim=-1)
)
clause_states = clause_states * ctx.clause_mask.unsqueeze(-1)
```

In forma compatta:

$$
K_{t+1} = K_t + F_K(\operatorname{norm}(K_t), M_K)
$$

Le clausole sono un buffer di calcolo. Accumulano ciò che le variabili dicono, lo trasformano, poi rimandano indietro un segnale.

## Secondo mezzo round: da clausole a variabili

Il secondo passaggio è l'analogo di:

$$
M \operatorname{Msg}_C(C_{t+1})
$$

Il codice produce un segnale per clausola, lo copia sui tre slot, aggiunge il segno e lo somma sulle variabili incidenti:

```python
clause_signal = self.clause_out(self.clause_norm(clause_states) if self.pre_norm else clause_states)
per_slot = clause_signal.unsqueeze(2) + self.message_sign(ctx.sign_ids)
per_slot = per_slot * ctx.slot_valid.unsqueeze(-1)

var_message = torch.zeros(batch, n_vars, d, device=hidden.device, dtype=hidden.dtype)
scatter_idx = ctx.var_idx.reshape(batch, n_clauses * arity, 1).expand(batch, n_clauses * arity, d)
var_message = var_message.scatter_add(
    1,
    scatter_idx,
    per_slot.reshape(batch, n_clauses * arity, d),
)
```

`scatter_add` è la moltiplicazione per la matrice di incidenza, scritta in forma indicizzata. Se una variabile appare in molte clausole, riceve la somma dei segnali provenienti da tutte quelle clausole:

$$
M_V = \sum_{\text{clausole che toccano la variabile}} \operatorname{Msg}_K(K_{t+1}, \text{segno})
$$

Ora la variabile può aggiornarsi:

```python
delta = self.var_update(torch.cat([var_for_msg, var_message], dim=-1))
var_states = var_states + delta
```

In notazione breve:

$$
V_{t+1} = V_t + F_V(\operatorname{norm}(V_t), M_V)
$$

Il round completo è quindi:

$$
K_{t+1} = K_t + F_K(\operatorname{norm}(K_t), M_K)
$$

$$
V_{t+1} = V_t + F_V(\operatorname{norm}(V_t), M_V)
$$

con $$M_K$$ costruito aggregando dalle variabili alle clausole, e $$M_V$$ costruito aggregando dalle clausole alle variabili.

## Differenza rispetto a NeuroSAT

NeuroSAT mantiene un nodo per ogni letterale e usa `Flip` per collegare ogni letterale al suo complemento. Il codice RYS mantiene un nodo per ogni variabile e passa la polarità sugli archi.

Detto in modo operativo:

$$
\text{NeuroSAT: } L_t \in \mathbb{R}^{2n \times d}
$$

$$
\text{RYS SAT: } V_t \in \mathbb{R}^{n \times d} \quad \text{più embedding di segno}
$$

Questa scelta rende il modello più compatto. La perdita principale è che il rapporto tra $$x_i$$ e $$\neg x_i$$ non vive in due nodi separati con un operatore `Flip`; viene mediato dai messaggi di segno. Per l'obiettivo del codice, cioè produrre direttamente un assegnamento per variabile e studiare le traiettorie residue con RYS, questa forma è più comoda.

## Pre-norm e traiettoria residua

Il flag `pre_norm` ha un ruolo più importante di quanto sembri. In modalità pre-norm, il modello legge una versione normalizzata dello stato, ma aggiorna lo stato originale con un'aggiunta:

$$
V_{t+1} = V_t + \Delta V_t
$$

Dopo molti round:

$$
V_T = V_0 + \sum_t \Delta V_t
$$

Questa forma telescopica è il ponte con RYS. Ripetere una finestra di round significa applicare altri passi dello stesso sistema dinamico. La geometria CKA e la decomposizione $$\rho/\phi$$ vengono lette su questa traiettoria residua, prima della normalizzazione finale.

Il codice conserva gli stati intermedi proprio per questo:

```python
if return_hidden_states:
    trace.append(hidden[:, : self.config.max_vars].clone())
```

La traccia contiene solo la parte variabile del flusso residuo. Le clausole servono alla computazione locale, mentre l'assegnamento finale vive sulle variabili.

## Dallo stato latente all'assegnamento

Dopo l'ultimo round, il modello normalizza gli stati delle variabili e applica una testa lineare:

```python
var_states = self.norm(hidden[:, : self.config.max_vars])
logits = self.assignment_head(var_states)
```

La forma dell'output è:

$$
\text{logits} \in \mathbb{R}^{n \times 2}
$$

Per ogni variabile, la prima colonna è il punteggio per $$0$$ e la seconda per $$1$$. L'assegnamento discreto si ottiene prendendo l'argmax. Se chiediamo `return_round_logits`, la stessa testa viene applicata agli stati intermedi:

```python
round_logits = [self.assignment_head(self.model.norm(states)) for states in trace]
```

Questo permette di osservare il processo lungo il tempo. È un punto vicino allo spirito del paper NeuroSAT: la soluzione può emergere dalle attivazioni prima di essere letta come decisione finale.

## Il rumore GRAM-style

Il modello può aggiungere una componente stocastica agli aggiornamenti delle variabili:

```python
mu = self.mu_head(delta)
log_sigma = self.log_sigma_head(delta).clamp(self._log_sigma_min, self._log_sigma_max)
delta = delta + mu
if self.sample:
    delta = delta + torch.exp(log_sigma) * torch.randn_like(delta)
```

La parte deterministica produce $$\Delta V$$. Il ramo stocastico impara una deriva $$\mu$$ e una scala $$\sigma$$:

$$
\Delta V \leftarrow \Delta V + \mu + \sigma \odot \eta
$$

$$
\eta \sim \mathcal{N}(0,I)
$$

L'idea viene dal filone GRAM {% cite baek2026gram %}: in un problema combinatorio con molte soluzioni, una singola traiettoria deterministica può finire in una zona media dello spazio. Le formule SAT soddisfacibili ammettono spesso molti assegnamenti. Due soluzioni valide possono spingere una variabile in direzioni opposte durante l'addestramento. La media tra assegnamenti discreti è un oggetto ambiguo.

Per esempio:

$$
(1,0,0)
\quad \text{e} \quad
(0,1,1)
$$

hanno media:

$$
(0.5,0.5,0.5)
$$

Quel vettore non è un assegnamento booleano. Dopo l'arrotondamento può diventare una configurazione che viola la formula. Il rumore appreso permette di campionare più traiettorie sulla stessa istanza: alcune possono convergere verso una soluzione, altre verso una soluzione diversa.

Qui appare un secondo asse di calcolo. RYS aumenta la profondità: più round lungo una traiettoria. Il campionamento aumenta la larghezza: più traiettorie sulla stessa formula. Con un verificatore SAT possiamo misurare entrambe:

$$
\text{valid@}N =
\mathbb{1}[\text{almeno uno dei } N \text{ campioni soddisfa } \Phi]
$$

e possiamo misurare anche la copertura delle soluzioni distinte trovate.

La parte delicata è la varianza. Se l'addestramento non spinge abbastanza verso l'esplorazione, $$\sigma$$ scende verso zero e il modello torna quasi deterministico. Per questo il codice raccoglie `mean_log_sigma`:

```python
if self.noise_sink is not None:
    self.noise_sink.append(log_sigma.mean())
```

Questo valore può essere usato come diagnostica o come termine di regolarizzazione.

## Il filo logico

La notazione di NeuroSAT rende più ordinata la storia. Prima ci sono letterali e clausole, poi una matrice di incidenza $$M$$, poi due aggregazioni sparse: $$M^\top$$ porta messaggi verso le clausole, $$M$$ li riporta verso i letterali. Il nostro codice implementa la stessa grammatica con una rappresentazione più compatta: variabili al posto dei letterali espliciti, embedding di segno sugli archi, `gather` e `scatter_add` al posto della matrice $$M$$.

Da qui si capisce anche perché il modello è adatto a RYS. Ogni round è un passo di una dinamica ricorrente. Le variabili accumulano spostamenti residui, le clausole funzionano da memoria locale del vincolo, l'output legge la traiettoria finale. La versione stocastica aggiunge una piccola ricerca probabilistica sopra questa dinamica. Se il determinismo tende a collassare verso una soluzione media, il campionamento prova a separare traiettorie compatibili diverse.

Il risultato è un risolutore SAT piccolo, leggibile e manipolabile. Non compete con un SAT solver moderno. Serve a studiare una domanda diversa: che forma prende un algoritmo di ricerca quando lo impariamo come dinamica latente e poi lo facciamo girare più a lungo?

---

## Riferimenti

{% bibliography --cited %}
