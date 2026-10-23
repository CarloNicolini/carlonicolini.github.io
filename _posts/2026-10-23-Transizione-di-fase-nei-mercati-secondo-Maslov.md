---
layout: post
title: "La dacia di Maslov e le transizioni di fase nei mercati"
description: "Sono partito dal racconto di un fisico che vendette casa prima del crollo del 2008. Ho provato a cercare nei dati i segnali di una crisi: il passaggio dalla teoria alla previsione si è rivelato difficile."
date: 2026-10-23
lang: it
published: false
permalink: "/sections/science/2026/10/23/Transizione-di-fase-nei-mercati-secondo-Maslov.html"
categories:
  - science
  - physics
  - finance
---

Nel marzo del 2009 il fisico matematico russo Viktor Maslov raccontò a un giornalista di aver venduto la dacia e un appartamento l'estate precedente, trasferendo il denaro ai figli all'estero. I suoi calcoli, disse, mostravano che l'economia americana aveva superato una soglia critica. La crisi sarebbe arrivata come una valanga.

Il dettaglio della dacia mi è rimasto in testa. Una cosa è pubblicare un modello; mettere in vendita una casa suggerisce una fiducia piuttosto concreta nei propri conti. Per chi si occupa di fisica statistica, poi, la spiegazione ha un fascino particolare: un sistema può cambiare poco mentre accumula tensione, per poi riorganizzarsi bruscamente. Maslov pensava che qualcosa del genere stesse accadendo al debito.

Sono andato a cercare i lavori e l'intervista del 2009 {% cite medvedev2009maslov %}. La cronologia richiede un po' di attenzione. Il racconto della vendita è successivo al crollo di Lehman Brothers; i problemi dei mutui erano già emersi nel 2007. Non ho trovato una previsione pubblica anteriore alla crisi accompagnata dai dati e dal calcolo che avrebbero motivato la vendita. Ho trovato, invece, un modello del 2003 {% cite maslov2003quasistable %} che parlava già di condensazione nei mercati.

Ho provato a seguirne alcune idee con i dati disponibili oggi. Volevo capire se aiutassero anche a riconoscere una crisi prima che cominci.

<figure id="ritratto-maslov" markdown="0" style="max-width: 280px; margin: 2rem auto;">
  <img src="{{ '/assets/media/postfigures/maslov-2026/maslov-ritratto.jpg' | relative_url }}" alt="Ritratto in bianco e nero del fisico matematico Viktor Pavlovich Maslov" width="428" height="654" loading="lazy" style="width: 100%; height: auto;">
  <figcaption>Viktor Pavlovich Maslov (1930–2023). Foto: archivio MIEM, pubblicata da <a href="https://www.hse.ru/our/news/850464253.html">HSE</a>.</figcaption>
</figure>

Maslov è noto per l'indice che porta il suo nome e per i metodi semiclassici, che collegano la meccanica quantistica a quella classica {% cite hse2023maslov %}. La sua *dequantizzazione* porta, attraverso un cambio di scala logaritmico e un limite, all'algebra tropicale: nella versione max-plus la somma diventa il massimo e il prodotto diventa una somma. Questo passaggio è alla base del suo lavoro sull'analisi idempotente {% cite maslov2021tropical %}.

## I numeri che servono

Ho costruito un insieme di serie sugli Stati Uniti e su 16 paesi europei. La parte lenta descrive il credito e i pagamenti necessari a sostenerlo. Dalla [Banca dei Regolamenti Internazionali](https://data.bis.org/topics/CREDIT_GAPS) arrivano il debito privato rispetto al PIL, il suo scostamento dalla tendenza di lungo periodo e i prezzi reali delle case. Il *servizio del debito* misura la quota di reddito assorbita da interessi e rimborsi: aiuta a distinguere un debito gestibile da uno che lascia poco margine. La scelta di questi indicatori segue anche il lavoro della BIS sui segnali anticipatori delle crisi bancarie {% cite drehmann2018early %}.

La parte veloce viene dai mercati. Ho scaricato da LSEG 17 serie, fra indici azionari e fondi settoriali, e integrato i tassi e gli spread di credito con FRED. Gli spread indicano quanto rendimento in più chiedono gli investitori per prestare a debitori più rischiosi. Per confrontare il rischio sovrano europeo ho usato anche dati ECB ed Eurostat.

Queste grandezze rispondono a domande diverse. Il debito racconta quanto è carico il sistema; il costo delle rate dice qualcosa sulla capacità di reggerlo. I prezzi reagiscono più in fretta, spesso quando la tensione è già visibile. Un picco del rapporto debito/PIL durante una recessione può dipendere anche dalla caduta del denominatore. Per chiamarlo segnale anticipatore devo controllare quando era disponibile.

## Il debito e le sue scadenze

Nel modello del 2003 {% cite maslov2003quasistable %}, Maslov considera un risparmiatore che può distribuire il denaro fra molte banche ordinarie oppure concentrarlo in un unico impiego ad alto rendimento, rappresentato da una piramide finanziaria. Per capire da dove venga la fisica, bisogna partire da un dettaglio: tratta le unità di denaro come indistinguibili. Scambiare due banconote dello stesso taglio lascia invariata l'allocazione. È la scelta combinatoria che avvicina il modello alla statistica di Bose.

Supponiamo di avere due unità da distribuire fra due banche ordinarie. Le possibilità sono tre: entrambe nella prima, una per banca, entrambe nella seconda. Se le unità sono *k* e le banche *G*, il numero di distribuzioni diventa un coefficiente binomiale. Nella replica ho massimizzato questa funzione, a meno di un termine costante:

$$
\Omega_G(k)=\binom{k+G-1}{k},
\qquad
F(k)=-\beta\,\Delta\lambda\,k+\log\Omega_G(k),
\qquad 0\leq k\leq N.
$$

Qui *N* è tutto il denaro, diviso in unità uguali; *k* è la parte nelle banche ordinarie, mentre il resto va nella piramide. La differenza di rendimento a favore della piramide è Δλ. Il primo termine rende costoso lasciare denaro nelle banche meno redditizie. Il secondo premia il numero di configurazioni disponibili: il suo logaritmo è l'entropia combinatoria. Maslov assume che questa informazione entri nella scelta del risparmiatore. Già questa è un'ipotesi economica da discutere, benché il conteggio sia esatto.

Il parametro β regola il peso del rendimento rispetto al conteggio. Nel testo del 2003 è legato al valore dell'unità monetaria; nella replica lo faccio variare per esplorare il modello. Quando cresce, l'allocazione ottima si sposta verso la piramide. Il punto di equilibrio interno si trova dove il guadagno marginale di entropia uguaglia βΔλ. Agli estremi ci sono due soglie, oltre le quali la soluzione occupa interamente uno dei due livelli.

Ho riprodotto questo passaggio e verificato il calcolo confrontandolo, per piccoli sistemi, con l'enumerazione delle allocazioni intere. Le soglie cambiano con il numero di banche e con la granularità del denaro. Nel sistema finito vediamo un cambiamento dell'ottimo; per parlare di singolarità termodinamica occorre studiare anche un limite di grandi numeri. Nessuna delle due cose fornisce ancora una soglia in punti di PIL.

### Dove va a finire il debito in eccesso

Nel lavoro del dicembre 2008 {% cite maslov2008economic %}, Maslov porta il ragionamento sul debito. Introduce una velocità di ricircolo: quante volte all'anno una posizione passa attraverso un ciclo di indebitamento e rimborso. Per un prestito della durata di *L* anni usa una velocità schematica pari a 1/*L*. Un mutuo ventennale finisce così fra i livelli lenti; una catena di prestiti che si rinnova rapidamente occupa livelli più alti.

Per vedere la struttura della soglia conviene guardare anche il lavoro matematico con Nazaikinskii {% cite maslovnazaikinskii2008bose %}. Si distribuiscono unità indistinguibili fra livelli, imponendo un vincolo sul numero totale e uno sul loro costo complessivo. Il livello *j* ha *q*<sub>j</sub> compartimenti distinguibili, ciascuno dei quali può contenere più unità. Nella versione matematica, la capacità critica dei livelli superiori assume la forma:

$$
N_c=\sum_{j\geq1}\frac{q_j}{e^{bj}-1},
\qquad
M=\sum_{j\geq1}\frac{j q_j}{e^{bj}-1}.
$$

Il vincolo *M* determina *b* attraverso la seconda equazione. La prima dice quante unità vengono ospitate, nel regime critico, dai livelli superiori. Se il totale supera questa capacità statistica, l'eccesso si raccoglie nel livello più basso: è la condensazione. Qui *M* è un budget matematico, analogo all'energia; per trasferire le formule all'economia bisogna specificare che cosa corrisponda a ciascun livello e ai suoi compartimenti. Il risultato dipende proprio da questa struttura.

Nella costruzione economica Maslov assume una distribuzione di tipo Pareto per le molteplicità dei gruppi e una relazione fra dimensione del debito e velocità, ispirata al modello Baumol–Tobin. Sono ipotesi che determinano la soglia. La sua interpretazione è che il debito in eccesso si accumuli sui livelli lenti, dove i rimborsi richiedono anni, esponendo prima i mutui e poi altri prestiti a lunga durata. Il testo propone questo collegamento con i fallimenti; la dimostrazione combinatoria, da sola, non descrive la catena concreta di insolvenze fra famiglie e banche.

Qui manca un collegamento empirico importante. Per calcolare una soglia economica servirebbero la distribuzione dei debiti e informazioni sulle durate dei contratti. Le serie aggregate che ho raccolto non bastano. La velocità della moneta, che posso scaricare, è a sua volta una grandezza diversa dal ricircolo del debito introdotto nel modello. Il servizio del debito misura invece quanto reddito viene assorbito dai pagamenti. È utile per cercare fragilità, senza permettermi di stimare direttamente quel numero critico.

Maslov parla anche di crescita dell'entropia e della complessità di Kolmogorov: chi scopre una strategia profittevole viene imitato, e il mercato rende più difficile trovare la successiva. È una proposta sul funzionamento dei mercati, formulata nei suoi testi. Nel nostro esperimento non abbiamo misurato la lunghezza del più breve programma capace di descrivere i prezzi, che definirebbe la complessità di Kolmogorov.

Ho quindi tenuto la replica matematica separata dall'esperimento sui mercati. Per quest'ultimo ho scelto osservabili che posso calcolare e sottoporre a un test.

## Quanto si muovono insieme i settori

Un possibile indizio di fragilità è la perdita di indipendenza fra parti del mercato. Quando quasi tutto sale e scende insieme, comprare attività diverse può offrire meno protezione di quanto suggeriscano i loro nomi.

Ho misurato questo movimento comune sui rendimenti di nove fondi settoriali USA, usando una finestra mobile di 252 sedute. Calcolo la matrice delle correlazioni dei rendimenti logaritmici: ogni settore pesa sulla stessa scala, così la maggiore volatilità di uno di essi non basta a farlo dominare. Gli autovalori della matrice misurano quanta varianza appartiene a ciascuna direzione di movimento. La loro somma è nove, il numero dei settori.

Dividendo ogni autovalore per la somma ottengo quote confrontabili, che chiamo *p*. La quota più grande misura la sincronizzazione; l'entropia spettrale descrive come si distribuisce il resto:

$$
p_i=\frac{\lambda_i}{\sum_j\lambda_j},
\qquad
s=\max_i p_i,
\qquad
h=-\frac{\sum_i p_i\log p_i}{\log 9}.
$$

Con nove settori senza correlazioni, tutte le quote sarebbero uguali: il modo principale spiegherebbe circa l'11% e l'entropia normalizzata varrebbe uno. Se tutti si muovessero perfettamente insieme, una sola direzione spiegherebbe il 100% e l'entropia scenderebbe a zero. Il rango effettivo, che calcolo anch'esso, esprime la stessa dispersione come numero di direzioni: da nove a una nei due casi limite.

L'idea fisica è che una perturbazione comune possa coinvolgere una parte crescente del sistema, riducendo la protezione della diversificazione. Un aumento delle correlazioni può però accompagnare una crisi già in corso. Per chiamarlo anticipatore occorre verificare che arrivi prima. Inoltre questa entropia riguarda gli autovalori dei rendimenti: ha un oggetto diverso dal conteggio delle allocazioni di Maslov e dalla complessità algoritmica.

Questa è un'estensione empirica del mio esperimento. Nei testi esaminati non ho trovato che Maslov usasse questi indicatori per la sua previsione.

![In alto, il gap di credito di Stati Uniti, Francia e Italia; in basso, la quota di movimento comune nei nove settori USA. Nel 2026 entrambi gli indicatori sono lontani dai livelli della crisi finanziaria.]({{ '/assets/media/postfigures/maslov-2026/credito-e-movimento-comune.png' | relative_url }})

*Le serie di credito sono trimestrali e revisionate: l'ultima osservazione mostrata è il primo trimestre 2026. Il movimento comune è calcolato su 252 sedute condivise dai nove fondi, fino al 22 ottobre 2026. La fascia grigia indica il 2007–2009; non è una soglia stimata dal modello.*

Il primo risultato riguarda la fotografia attuale. Il gap di credito USA è circa **−11,3 punti di PIL**: il rapporto fra credito e PIL si trova sotto la propria tendenza di lungo periodo. Nel campione settoriale americano, il modo comune spiega circa il **35%** delle oscillazioni standardizzate, un valore basso rispetto alla storia disponibile. Nel 2008–2009 quella quota era molto più alta.

Non emerge una concentrazione di segnali simile a quella fase. Restano differenze nazionali: in Francia il servizio del debito privato è sopra la propria media storica; in Spagna i prezzi reali delle case sono cresciuti di circa il 24% in tre anni, nel dato allineato al primo trimestre 2026. Da questi numeri non posso ricavare quanti mesi ci separino da una crisi.

## Il tentativo di anticipare un crollo

Per mettere alla prova la previsione ho fissato un evento concreto: una perdita dell'indice di almeno il 20% rispetto al prezzo di fine mese, entro i dodici mesi successivi. Ho confrontato un modello con indicatori finanziari convenzionali con una versione che aggiunge movimento comune ed entropia. Entrambi stimano una probabilità; i pesi e la soglia degli allarmi sono scelti usando soltanto esiti già maturati prima del 2016.

La base convenzionale comprende la volatilità recente e il rendimento dell'ultimo anno, la forza delle banche rispetto al mercato, lo spread di credito, la pendenza della curva dei tassi e il gap di credito USA. Ho usato una regressione logistica: somma questi segnali, dopo averli standardizzati sul passato, e trasforma il risultato in una probabilità fra zero e uno. Una penalizzazione L2 scoraggia pesi troppo grandi, che con pochi episodi di crisi rischierebbero di adattarsi ai dettagli del campione. Anche la sua intensità è scelta sui dati precedenti.

Questo è il punto in cui l'analogia fisica diventa un'ipotesi verificabile. Se la perdita di varietà dei movimenti contiene informazione anticipatrice, aggiungere *s* e *h* dovrebbe migliorare le previsioni su anni mai usati per scegliere il modello. Non ho imposto una temperatura critica, né identificato la volatilità con una temperatura economica. Ho lasciato che fosse il confronto fuori campione a stabilire se quei due numeri servissero.

Il periodo finale comprende 117 previsioni mensili per ciascun mercato, dal gennaio 2016 al settembre 2025. Sono le ultime origini per le quali, nei dati acquisiti, posso osservare dodici mesi completi.

Per confrontare le probabilità uso il *Brier score*, l'errore quadratico medio fra la previsione e l'esito: un numero più piccolo indica un errore minore. Negli USA aggiungere gli indicatori econofisici porta l'errore da circa 0,133 a 0,125. In Europa il guadagno è più piccolo.

![Il miglioramento dell'errore di previsione dopo aver aggiunto movimento comune ed entropia. Per Stati Uniti ed Europa gli intervalli comprendono sia un peggioramento sia un miglioramento.]({{ '/assets/media/postfigures/maslov-2026/guadagno-predittivo.png' | relative_url }})

*I punti mostrano il Brier score del modello convenzionale meno quello del modello esteso, sul periodo finale. Valori positivi favoriscono l'estensione econofisica. Gli intervalli approssimati al 95% derivano dal ricampionamento di blocchi temporali di cinque anni; ne abbiamo soltanto tre. L'incertezza resta ampia.*

Il secondo risultato è questo: **il miglioramento medio non basta a dimostrare un vantaggio predittivo affidabile**. Gli intervalli comprendono lo zero. Alla soglia fissata sul campione precedente, il modello a dodici mesi non ha emesso allarmi prima del primo raggiungimento della perdita negli episodi del 2020 e del 2022, né negli USA né in Europa. Sono gli stessi shock osservati su mercati collegati, quindi non li conto come quattro crisi indipendenti.

Ho eseguito anche un test separato sugli inizi delle crisi bancarie, usando la classificazione IMF {% cite laevenvalencia2026banking %}. Anche quel modello ha dato risultati insoddisfacenti. Nel periodo finale mancano nuove crisi sistemiche nei paesi considerati, perciò lì posso misurare gli allarmi sbagliati, senza verificare la capacità di intercettare una nuova crisi. Secondo questa classificazione, le tensioni bancarie del 2023 restano episodi di stress.

Un limite attraversa tutto il test: le serie macroeconomiche sono revisionate. Ho applicato ritardi convenzionali per evitare di usare un trimestre prima della sua disponibilità plausibile, ma questa ricostruzione non restituisce esattamente le informazioni che aveva un osservatore dell'epoca. Nell'audit ALFRED, per esempio, il servizio del debito delle famiglie USA del terzo trimestre 2007 valeva 14,32% nel vintage di fine 2007; la serie attuale riporta circa 15,71%, anche per cambi metodologici.

Al 23 ottobre 2026 riesco dunque a descrivere alcune vulnerabilità e a confrontarle con il passato. La soglia economica di Maslov resta da identificare. Per avvicinarmi a quel calcolo mi servirebbero soprattutto dati sulle scadenze e sulla distribuzione del debito fra i debitori, insieme alle versioni storiche disponibili a ogni data. Il racconto della dacia lascia aperta proprio questa curiosità: quali numeri aveva davanti quando decise di venderla?

I [risultati aggregati del confronto]({{ '/assets/media/postfigures/maslov-2026/confronto-modelli.csv' | relative_url }}) sono disponibili in CSV. Le figure usano gli esperimenti già eseguiti, senza nuovi adattamenti del modello sui risultati finali.

## Riferimenti

{% bibliography --cited %}
