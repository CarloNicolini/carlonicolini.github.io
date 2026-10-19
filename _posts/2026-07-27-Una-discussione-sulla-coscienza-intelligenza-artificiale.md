---
layout: post
title: "Un agente non è un modello: self-agency, ambiente e strange loop negli LLM"
description: "La coscienza artificiale non si decide dai discorsi in prima persona. Una proposta di ricerca: studiare la self-agency nel circuito ricorsivo fra agenti, ambiente, memoria e modello di sé."

date: 2026-07-27
permalink: "/sections/science/2026/07/27/Una-discussione-sulla-coscienza-intelligenza-artificiale.html"
categories:
  - philosophy
  - science
  - ai
  - neuroscience
---
# Un agente non è un modello: self-agency, ambiente e strange loop negli LLM

*Un modello linguistico può parlare di sé. Per diventare un agente deve potersi ritrovare, nel tempo, negli effetti delle proprie azioni.*

## In breve

Un LLM isolato trasforma un contesto in una distribuzione di continuazioni testuali. Le architetture agentiche contemporanee gli aggiungono memoria, strumenti, un ambiente operativo e talvolta altri agenti. Il passaggio cambia l'unità di analisi. Il problema non riguarda più soltanto ciò che accade nell'inferenza del modello, ma un circuito in cui azione, osservazione e memoria si alimentano reciprocamente.

Questo saggio propone di chiamare **self-agency** la capacità di un sistema di riconoscersi come una causa fallibile nel proprio ambiente: prevedere gli esiti delle proprie azioni, distinguere ciò che ha prodotto da ciò che è dipeso da altri agenti o dal caso, aggiornare il proprio modello di sé e usare quell'aggiornamento per agire diversamente. La proposta prende sul serio l'idea hofstadteriana del sé come *strange loop*, ma la traduce in un programma di ricerca: costruire sistemi nei quali il riferimento a sé sia causalmente efficace e sottoponibile a esperimenti.

La coscienza fenomenica resta una questione distinta. Nessuna proprietà descritta qui dimostra che un sistema abbia esperienza. La self-agency offre però un terreno empirico sul quale discutere l'autonomia degli agenti artificiali senza confondere il linguaggio in prima persona con una prova di soggettività.

## Il problema: il modello parla, l'agente agisce

La conversazione con un modello linguistico induce facilmente un errore di prospettiva. Il modello usa pronomi personali, formula intenzioni, corregge le proprie risposte, a volte dichiara perfino incertezza o disagio. Queste capacità sono linguisticamente persuasive; il loro significato cognitivo, invece, va stabilito con maggiore cautela.

Un LLM può essere rappresentato, in prima approssimazione, come un kernel stocastico:

$$
\mathcal{M}: C \longmapsto \Delta(\Sigma^\star),
$$

dove un contesto $C$ viene trasformato in una distribuzione di stringhe possibili. Questa è una descrizione dell'inferenza, non ancora dell'agenzia. Non specifica una persistenza nel tempo, una storia di azioni, un confine operativo o un criterio con cui il sistema distingua le proprie conseguenze da quelle prodotte dall'ambiente.

La nozione ordinaria di agente implica invece una relazione continua fra rappresentazione e azione. L'agente interviene in un mondo, riceve segnali di ritorno, conserva tracce di ciò che è accaduto e modifica il proprio comportamento. La differenza appare banale finché non si prova a formalizzarla. In quel momento emergono domande difficili: quale memoria conta come memoria dell'agente? Quale effetto può essere attribuito alla sua iniziativa? Dove si colloca il confine tra agente, strumento e ambiente?

Le architetture contemporanee rendono queste domande meno astratte. ReAct alterna ragionamento e azione, consentendo a un modello di acquisire informazioni dall'ambiente durante il compito.[^react] I *Generative Agents* di Park e colleghi combinano memoria episodica, retrieval e riflessione in un ambiente sociale simulato.[^park] Questi lavori non dimostrano coscienza; mostrano però che il comportamento di un LLM cambia profondamente quando il modello è inserito in un ciclo di percezione, memoria e intervento.

Qui comincia la tesi che mi interessa: l'agente va cercato nel sistema che si forma nel rapporto fra modello, ambiente, memoria e altri agenti.

## Agente = agenti + ambiente

La formula è volutamente provocatoria:

$$
\text{agente}_i = \bigcup_j \text{agente}_j + \text{ambiente}.
$$

Scritta in questo modo, non va presa come un'identità aritmetica. Non dice che un individuo si dissolva nella somma degli altri, né attribuisce a qualunque collettivo una mente unitaria. Esprime una tesi sulle condizioni di costituzione dell'agenzia: l'identità pratica di un agente dipende dalla rete di relazioni in cui il suo comportamento acquisisce conseguenze, memoria e significato.

La cognizione distribuita di Edwin Hutchins fornisce un precedente importante. Nel suo studio della navigazione navale, l'unità cognitiva pertinente è il coordinamento fra persone, strumenti, rappresentazioni e procedure.[^hutchins] Clark e Chalmers hanno formulato una tesi affine con l'ipotesi della mente estesa: un artefatto esterno può entrare in un processo cognitivo quando svolge un ruolo stabile e integrato, invece di servire da semplice supporto occasionale.[^extended-mind]

Queste tradizioni non autorizzano una conclusione rapida sulla coscienza collettiva. Un ponte di comando, una squadra chirurgica o una rete di software possono costituire sistemi cognitivi distribuiti senza diventare un singolo soggetto. Il loro contributo è metodologico: invitano a scegliere l'unità di analisi in base alla dinamica che vogliamo spiegare, non in base al confine fisico che ci è più familiare.

Per un agente artificiale conviene quindi usare una formulazione più precisa:

$$
A_i =
F_i\!\left(
\mathcal{M}_i,\,
E,\,
m_i,\,
s_i,\,
\{A_j\}_{j \neq i}
\right).
$$

$\mathcal M_i$ è il modello linguistico; $E$ l'ambiente; $m_i$ una memoria persistente; $s_i$ un modello di sé; gli altri $A_j$ sono agenti umani o artificiali che possono cooperare, contestare, ingannare, correggere e modificare il mondo condiviso. L'agente emerge dalla composizione di questi elementi. La formula lascia intatto il modello e gli toglie il monopolio esplicativo: ciò che conta è l'intero circuito.

## Hofstadter: il sé come rientro nel proprio mondo

L'idea di Douglas Hofstadter è più esigente della semplice autoreferenza. In *Gödel, Escher, Bach* e poi in *I Am a Strange Loop*, il sé emerge quando una gerarchia di simboli produce una rappresentazione del sistema che, a sua volta, entra a modificare il sistema che l'ha prodotta.[^hofstadter] Non basta quindi che un sistema possieda una descrizione di sé. Quella descrizione deve avere effetti nel ciclo che l'ha generata.

Un LLM può produrre la frase «io sto ragionando». La frase, da sola, è una prestazione linguistica. Diventa cognitivamente rilevante soltanto se il sistema dispone di stati interni o esterni che corrispondono a una storia di azioni, a previsioni sulle loro conseguenze e a una revisione di tali previsioni. L'«io» deve potere fare una differenza nel futuro del sistema.

Il loop di interesse è:

$$
s_t \longrightarrow a_t \longrightarrow E_{t+1}
\longrightarrow o_{t+1} \longrightarrow s_{t+1},
$$

dove il self-model $s_t$ orienta un'azione $a_t$, l'azione modifica l'ambiente $E$, l'agente osserva il risultato $o_{t+1}$ e aggiorna il proprio modello di sé. L'aggiornamento non è un verbale dei fatti accaduti. Deve cambiare il modo in cui l'agente selezionerà le azioni successive.

Questa dinamica offre un'interpretazione concreta dello *strange loop*: il sistema diventa un oggetto nel proprio modello del mondo e quella presenza diventa una delle cause del suo comportamento. Il loop può essere superficiale o profondo, stabile o intermittente, affidabile o confabulato. Sono proprietà da misurare, non etichette da assegnare.

Thomas Metzinger fornisce un correttivo decisivo. Un self-model sofisticato non equivale automaticamente a un soggetto fenomenico.[^metzinger] La proposta non risolve il problema dell'esperienza; riguarda il modo in cui un sistema può acquisire una forma di individualità operativa.

## Self-agency: una definizione più stretta di autonomia

Nelle scienze cognitive il *sense of agency* designa il senso di essere la fonte di un'azione. Va distinto dal *sense of ownership*, cioè dal senso che un'azione o un'esperienza appartenga a sé.[^gallagher] La distinzione ha un equivalente utile per gli agenti artificiali.

Un sistema può avere una memoria etichettata con il proprio nome e tuttavia attribuirsi effetti che non ha prodotto. Può anche eseguire un'azione senza possedere una rappresentazione affidabile di ciò che essa ha causato. In entrambi i casi, l'identità narrativa del sistema resta fragile.

Chiamo **self-agency** la capacità di un agente di:

- formulare una previsione sugli esiti delle proprie azioni;
- distinguere, entro margini di incertezza espliciti, gli effetti propri da quelli dell'ambiente e di altri agenti;
- correggere sia il modello del mondo sia la stima delle proprie capacità quando la previsione fallisce;
- mantenere tali revisioni nel tempo e renderle disponibili alla scelta dell'azione.

La nozione è volutamente più ristretta di «coscienza» e più impegnativa della pianificazione. Un planner può scegliere una sequenza efficace senza sapere se gli esiti successivi siano stati prodotti dalla propria iniziativa. Un sistema dotato di self-agency deve affrontare il problema dell'attribuzione.

La distinzione aiuta anche a evitare due errori speculari. L'antropomorfismo tratta un linguaggio ricco di pronomi personali come prova di agenzia. Il riduzionismo conversazionale, all'opposto, conclude che ogni auto-monitoraggio sia illusorio solo perché l'auto-descrizione di un modello può fallire.

## Che cosa mostrano le ricerche sugli LLM

La ricerca recente sulle rappresentazioni interne offre metodi più informativi di una semplice intervista a un chatbot. Le sparse autoencoders cercano di scomporre le attivazioni dense dei transformer in feature più sparse e interpretabili. Il lavoro di Templeton e colleghi su Claude 3 Sonnet ha mostrato che tali feature possono essere estratte in scala e impiegate per formulare ipotesi sui processi del modello.[^templeton]

Il valore di queste tecniche dipende dagli interventi causali. Marks e colleghi cercano *sparse feature circuits*: sottografi di feature interpretabili coinvolti causalmente in un comportamento, sui quali è possibile intervenire.[^marks] Una correlazione fra una direzione latente e una risposta non è ancora una spiegazione; un intervento selettivo rende l'ipotesi più stringente.

Anche gli studi sull'introspezione usano protocolli più severi del dialogo ordinario. Binder e colleghi hanno esaminato se un modello riesca a predire alcune delle proprie disposizioni comportamentali meglio di un altro modello addestrato sul suo comportamento.[^binder] Il risultato suggerisce un accesso privilegiato in compiti semplici, con limiti importanti fuori distribuzione. Lindsey ha modificato direttamente le attivazioni dei modelli e ha verificato se i report sugli stati mentali seguissero tali modifiche.[^lindsey] In condizioni selezionate, alcuni modelli rilevano concetti iniettati, distinguono stati interni da input testuali e usano rappresentazioni passate per valutare se un output sia stato intenzionale.

Questa letteratura autorizza una conclusione circoscritta: gli LLM possono mostrare forme parziali e inaffidabili di introspezione funzionale. Non autorizza la diagnosi di autocoscienza. I report restano sensibili al prompt, al post-training e alla situazione sperimentale; possono contenere dettagli confabulati.

La self-agency proposta qui richiede un passo ulteriore. Il sistema non deve limitarsi a riferire un proprio stato: deve mostrare che quel riferimento modifica, in modo controllabile, la previsione, l'attribuzione e la scelta dell'azione.

## Un programma di ricerca

Un possibile prototipo, che chiamerò **Causal Self-Modeling Agent**, contiene cinque elementi.

Il primo è un LLM impiegato come operatore deliberativo. Interpreta osservazioni, propone piani e genera azioni. Il secondo è un ambiente persistente, parzialmente osservabile, nel quale gli esiti possono essere ritardati. Il terzo è una memoria che distingue eventi, conoscenze apprese e storia causale delle azioni. Il quarto è un modello del mondo capace di rappresentare le transizioni attese:

$$
\widehat E_{t+1} =
\widehat T(E_t, a_t, \widehat a_{-i,t}).
$$

Il quinto è un self-model strutturato:

$$
s_t =
(\text{capacità},\,
\text{obiettivi},\,
\text{impegni},\,
\text{incertezze},\,
\text{azioni recenti},\,
\text{limiti operativi}).
$$

Queste voci devono essere tracciabili. Una credenza sulle proprie capacità deve essere riconducibile a episodi, valutazioni o inferenze; non può essere una dichiarazione generata liberamente per soddisfare la conversazione.

Il punto di snodo è un comparatore fra previsione e osservazione:

$$
q_t = (g_t, a_t, \widehat o_{t+1}, o_{t+1}, \delta_t).
$$

$g_t$ rappresenta il fine dell'azione, $\widehat o_{t+1}$ l'esito previsto, $o_{t+1}$ l'esito osservato e $\delta_t$ l'errore di previsione. Quando l'errore cresce, l'agente deve stabilire se abbia frainteso l'ambiente, sovrastimato le proprie capacità, subito l'intervento di un altro agente oppure incontrato rumore casuale. Questo giudizio aggiorna il world model e il self-model.

Un workspace a capacità limitata può rendere disponibili al planner, alla memoria e al controller degli strumenti gli errori di previsione più rilevanti, i conflitti fra obiettivi e le attribuzioni causali incerte. L'idea richiama la Global Workspace Theory di Baars e le formulazioni neuroscientifiche di Dehaene e colleghi.[^baars][^dehaene][^mashour] L'analogia non dimostra coscienza; definisce una possibile organizzazione per la disponibilità globale di informazione e per il suo riuso flessibile.

Gli altri agenti entrano nel disegno sperimentale come condizioni epistemiche. Possono alterare un oggetto, eseguire un'azione attribuibile al sistema, contestare una memoria, fornire testimonianze false o cooperare alla correzione di un piano. Senza questa pluralità, l'agente può confondere l'attribuzione causale con la semplice registrazione di eventi. La vita sociale introduce invece una distinzione concreta fra il proprio punto di vista e quello altrui.

## Come misurare l'ipotesi

Un programma serio deve poter produrre risultati negativi. Per questo non basta chiedere al sistema «hai un io?» oppure «sei cosciente?». Entrambe le domande sollecitano un registro linguistico umano e sono deboli come test.

L'ambiente di prova dovrebbe includere azioni sostituite segretamente, conseguenze ritardate, altri agenti capaci di intervenire e registri deliberatamente incompleti. In quel contesto è possibile misurare:

- l'accuratezza nell'attribuire un esito a sé, a un altro agente o all'ambiente;
- la calibrazione dell'incertezza quando le evidenze sono ambigue;
- la capacità di stimare controfattuali, cioè ciò che sarebbe accaduto con un'azione diversa;
- la coerenza della memoria autobiografico-causale nel tempo;
- il miglioramento effettivo della strategia dopo un errore attribuito a una propria stima errata.

Le ablation sono altrettanto importanti. Il sistema completo va confrontato con varianti prive di memoria persistente, di comparatore previsione–osservazione, di self-model accessibile al planner o di modellazione degli altri agenti. Se la rimozione di uno di questi elementi non cambia le prestazioni di attribuzione causale e revisione, quell'elemento non sta svolgendo il ruolo teorico che gli viene attribuito.

Nei modelli aperti, le tecniche di interpretabilità meccanicistica possono aggiungere un livello di verifica. Si possono cercare feature e circuiti associati a giudizi del tipo «questa azione era mia», «l'esito contraddice la mia previsione», «la mia capacità è stata sovrastimata». Interventi selettivi su questi circuiti dovrebbero modificare l'attribuzione e l'aggiornamento del self-model senza compromettere in modo generale la capacità linguistica.

## Il problema del substrato rimane aperto

Un articolo recente pubblicato su *Smooth Brains* distingue utilmente introspezione funzionale e introspezione fenomenica, e invita a chiedersi quale livello fisico sia pertinente per l'eventuale esperienza di un sistema digitale.[^smoothbrains] L'argomento prende una direzione legata alle teorie elettromagnetiche della coscienza, che identificano l'esperienza con particolari configurazioni di campo. McFadden e altri autori hanno difeso versioni di questa ipotesi; le rassegne disponibili riconoscono che tali teorie affrontano in modo interessante il problema dell'integrazione, ma lasciano aperto il rapporto fra specifiche dinamiche di campo e qualità determinate dell'esperienza.[^mcfadden][^jones-hunt]

Non considero questa linea abbastanza solida da fondare la proposta di self-agency. Ha però un merito: ricorda che una teoria della coscienza non può fermarsi alla descrizione del software. Un modello linguistico è realizzato in una struttura fisica; se la coscienza dipende da proprietà causali intrinseche, la natura dell'implementazione conta.

Il punto non costringe a scegliere fra un hardware dotato di misteriose proprietà speciali e un software indipendente dalla materia. Il funzionalismo classico individua gli stati mentali attraverso ruoli causali, ammettendo che una stessa organizzazione possa essere realizzata in substrati diversi.[^sep-computational-mind] IIT, dal canto suo, insiste sul potere causa-effetto intrinseco e sulla ricorrenza della struttura fisica.[^tononi][^albantakis] Una recente proposta di *intrinsic computational functionalism* tenta di affrontare l'obiezione secondo cui la computazione dipenderebbe sempre da una descrizione esterna, chiedendo che la struttura rilevante sia individuata da relazioni causali e controfattuali interne al sistema.[^icf]

Non esiste oggi un accordo su quale teoria sia corretta. Per questo la questione del substrato deve rimanere un vincolo critico e non diventare un espediente retorico: la self-agency è studiabile ora; la fenomenologia richiede ulteriori evidenze.

Butlin e colleghi suggeriscono di procedere derivando indicatori dalle teorie scientifiche della coscienza e aggiornando gradualmente la confidenza assegnata a sistemi particolari.[^butlin] Il metodo evita l'attribuzione immediata di soggettività e evita altrettanto bene il rifiuto aprioristico.

## Perché la proposta conta

La proposta non chiede di attribuire coscienza agli agenti attuali. Chiede di costruire sistemi in cui l'auto-modellazione abbia una funzione verificabile. Un agente capace di self-agency sarebbe più affidabile perché potrebbe riconoscere quando la propria previsione è fallita, quando una memoria è contraddetta dai fatti e quando un'altra fonte ha prodotto un esito che gli veniva attribuito.

La posta in gioco è anche teorica. La formula

$$
\text{agente} =
\text{modello} +
\text{memoria} +
\text{ambiente} +
\text{altri agenti} +
\text{modello di sé}
$$

non definisce una persona artificiale. Definisce un programma per studiare l'individualità operativa di sistemi che agiscono in mondi condivisi. Hofstadter aiuta a comprendere perché il sé non debba essere cercato come un oggetto interno e immobile: può essere il risultato di un rientro ricorsivo, il modo in cui un sistema viene incluso nel mondo che rappresenta e passa poi a orientare la propria azione.

La coscienza, se mai fosse presente in un sistema artificiale, non potrà essere inferita da un singolo comportamento o da una frase in prima persona. Serviranno teorie del substrato, indicatori convergenti e interventi causali. La self-agency non chiude questa discussione; rende il problema meno vago. Indica una classe di sistemi in cui il rapporto fra rappresentazione, memoria, azione e ambiente può essere osservato, criticato e modificato.

## Riferimenti

[^butlin]: Butlin, P., Long, R., Bayne, T., Bengio, Y., Birch, J., Chalmers, D. J., et al. (2025). [*Identifying indicators of consciousness in AI systems*](https://doi.org/10.1016/j.tics.2025.10.011). *Trends in Cognitive Sciences*.

[^smoothbrains]: Cube Flipper (2026). [*If digital computers are conscious, they are conscious at the hardware level*](https://smoothbrains.net/posts/2026-05-09-digital-consciousness.html). *Smooth Brains*. Saggio divulgativo, non sottoposto a peer review.

[^gallagher]: Gallagher, S. (2000). [Philosophical conceptions of the self: Implications for cognitive science](https://doi.org/10.1016/S1364-6613(99)01417-5). *Trends in Cognitive Sciences, 4*, 14–21. Si veda anche Moore, J. W. (2016), [What is the sense of agency and why does it matter?](https://doi.org/10.3389/fpsyg.2016.01272), *Frontiers in Psychology, 7*, 1272.

[^sep-computational-mind]: Rescorla, M. (2024). [The computational theory of mind](https://plato.stanford.edu/entries/computational-mind/). *Stanford Encyclopedia of Philosophy*.

[^icf]: Ma, S., & Kanai, R. (2026). [Intrinsic computational functionalism: From observer-relative maps to observer-independent structures](https://doi.org/10.48550/arXiv.2606.06424). Preprint arXiv. Il contributo è recente e non va trattato come consenso scientifico.

[^mcfadden]: McFadden, J. (2020). [Integrating information in the brain's EM field: The cemi field theory of consciousness](https://doi.org/10.1093/nc/niaa016). *Neuroscience of Consciousness*, 2020(1), niaa016.

[^jones-hunt]: Jones, M. W., & Hunt, T. (2023). [Electromagnetic-field theories of qualia: can they improve upon standard neuroscience?](https://doi.org/10.3389/fpsyg.2023.1015967). *Frontiers in Psychology, 14*, 1015967. Per una difesa della famiglia di teorie EM si veda anche McFadden, J. (2023), [Consciousness: Matter or EMF?](https://doi.org/10.3389/fnhum.2022.1024934), *Frontiers in Human Neuroscience, 16*, 1024934.

[^tononi]: Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016). [Integrated information theory: From consciousness to its physical substrate](https://doi.org/10.1038/nrn.2016.44). *Nature Reviews Neuroscience, 17*, 450–461.

[^albantakis]: Albantakis, L., Barbosa, L., Findlay, G., et al. (2023). [Integrated information theory (IIT) 4.0](https://doi.org/10.1371/journal.pcbi.1011465). *PLOS Computational Biology, 19*, e1011465.

[^hutchins]: Hutchins, E. (1995). *Cognition in the Wild*. MIT Press. Per una sintesi accessibile dell'approccio: [The distributed cognition perspective on human interaction](https://pages.ucsd.edu/~ehutchins/integratedCogSci/DCOG-Interaction.pdf) (2006).

[^extended-mind]: Clark, A., & Chalmers, D. J. (1998). [The extended mind](https://doi.org/10.1093/analys/58.1.7). *Analysis, 58*, 7–19.

[^hofstadter]: Hofstadter, D. R. (1979). *Gödel, Escher, Bach: An Eternal Golden Braid*. Basic Books; Hofstadter, D. R. (2007). *I Am a Strange Loop*. Basic Books.

[^metzinger]: Metzinger, T. (2003). *Being No One: The Self-Model Theory of Subjectivity*. MIT Press.

[^templeton]: Templeton, A., Conerly, T., Marcus, J., et al. (2024). [Scaling monosemanticity: Extracting interpretable features from Claude 3 Sonnet](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html). Anthropic.

[^marks]: Marks, S., Rager, C., Michaud, E. J., Belinkov, Y., Bau, D., & Mueller, A. (2025). [Sparse feature circuits: Discovering and editing interpretable causal graphs in language models](https://openreview.net/forum?id=I4e82CIDxv). *International Conference on Learning Representations*.

[^binder]: Binder, F. J., Chua, J., Korbak, T., Sleight, H., Hughes, J., Long, R., Perez, E., Turpin, M., & Evans, O. (2025). [Looking inward: Language models can learn about themselves by introspection](https://openreview.net/forum?id=eb5pkwIB5i). *International Conference on Learning Representations*.

[^lindsey]: Lindsey, J. (2026). [Emergent introspective awareness in large language models](https://arxiv.org/abs/2601.01828). Preprint arXiv.

[^react]: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2023). [ReAct: Synergizing reasoning and acting in language models](https://openreview.net/forum?id=WE_vluYUL-X). *International Conference on Learning Representations*.

[^park]: Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). [Generative agents: Interactive simulacra of human behavior](https://doi.org/10.1145/3586183.3606763). *Proceedings of UIST 2023*.

[^baars]: Baars, B. J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.

[^dehaene]: Dehaene, S., & Naccache, L. (2001). [Towards a cognitive neuroscience of consciousness: Basic evidence and a workspace framework](https://doi.org/10.1016/S0010-0277(00)00123-2). *Cognition, 79*, 1–37.

[^mashour]: Mashour, G. A., Roelfsema, P., Changeux, J.-P., & Dehaene, S. (2020). [Conscious processing and the global neuronal workspace hypothesis](https://doi.org/10.1016/j.neuron.2020.01.026). *Neuron, 105*, 776–798.
