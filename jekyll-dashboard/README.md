# jekyll-dashboard

Una piccola dashboard locale, stile spreadsheet, per organizzare i post markdown
di un sito Jekyll. Modifica titolo, descrizione, stato di pubblicazione, data e
tag direttamente sui file `.md`, e segnala i post che non rispettano lo schema
della front matter.

Niente build step, niente database: un backend Python (FastAPI, gestito con
[uv](https://docs.astral.sh/uv/)) che legge e scrive i file, e una singola
pagina HTML/JS.

## Uso

```bash
make install   # uv sync
make run       # avvia su http://127.0.0.1:8765
make test      # esegue i test di round-trip
```

Apri <http://127.0.0.1:8765> nel browser. Cambia la porta con `make run PORT=9000`.

## Puntare a un sito qualsiasi

Di default la dashboard usa `DEFAULT_SITE_ROOT` in `config.py`. Per usarla su
un altro sito, passa la root con la variabile `JEKYLL_SITE`:

```bash
make run JEKYLL_SITE=~/path/to/other/site
```

Vengono scansionate **tutte** le cartelle `_posts` trovate ricorsivamente sotto
la root. La "sezione" di ogni post è il nome della cartella che contiene
`_posts` (es. `science` per `.../science/_posts/`).

## Cosa fa

- Tabella di tutti i post nelle cartelle `_posts` configurate.
- Checkbox per `published`, campi di testo per titolo/descrizione, date picker
  per `date`, editor di tag con autocomplete dai tag esistenti.
- Filtri per sezione, stato (pubblicato / bozza / con errori) e ricerca testuale;
  ordinamento per colonna.
- Validazione dello schema: ogni post mostra `ok` oppure l'elenco dei problemi
  (campi mancanti, date non valide, chiavi duplicate).
- Salvataggio in blocco: modifichi più post, premi **Salva modifiche**.

## Schema validato

Campi obbligatori: `layout`, `title`, `date`, `published`, `categories`,
`description`. Opzionale: `tags`. Modificabile in `config.py`.

## Comportamento in scrittura

- Solo il blocco di front matter viene riscritto; **il corpo markdown resta
  identico byte per byte** (verificato dai test).
- Al salvataggio la front matter viene **normalizzata** allo schema canonico:
  ordine delle chiavi fisso, `date` in formato `YYYY-MM-DD`, `categories` e
  `tags` come liste a blocco, chiavi duplicate risolte.
- La dashboard **non inventa** le descrizioni mancanti: lascia il campo vuoto e
  lo segnala come errore di schema, così lo compili tu.

## Configurazione

La root del sito è in `config.py` (`DEFAULT_SITE_ROOT`) e sovrascrivibile con
`JEKYLL_SITE`. I campi obbligatori dello schema sono in `REQUIRED_FIELDS`.
