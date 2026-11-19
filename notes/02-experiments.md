# Experiment: stemming în BM25

## Ipoteza
Stemming-ul (Snowball, engleză) va îmbunătăți puțin recall@5, dar nu va
repara conceptual ratările: întrebările ratate nu folosesc cuvintele-cheie
din documentație, iar stemming-ul unește doar forme ale aceluiași cuvânt.

## Setup
- Corpus: 1183 de chunk-uri (fără release-notes.md)
- Set de evaluare: 42 de întrebări generate cu LLM, câte una pe chunk
- Metrică: recall@5 (bucata sursă apare în primele 5 rezultate)
- BM25: k1 = 1.5, b = 0.75

## Rezultate
| Variantă | Nimeriri | recall@5 |
|---|---|---|
| fără stemming | 31/42 | 0.738 |
| cu stemming | 29/42 | 0.690 |

Dezacorduri: 4 întrebări. Fără stemming câștigă 3, cu stemming câștigă 1.

## Test statistic (testul semnului)
- H0: stemming-ul nu are efect; fiecare dezacord e câștigat de o variantă cu probabilitatea 1/2.
- X = dezacorduri câștigate de varianta fără stemming, X ~ Binomial(4; 0.5).
- Observat: X = 3.
- p-value bilateral: P(X ≤ 1 sau X ≥ 3) = 10/16 = 0.625.

## Concluzie
Nicio dovadă de efect. Testul nu avea putere: cu 4 dezacorduri, cel mai mic
p-value posibil e 2/16 = 0.125, deci nici 4–0 n-ar fi fost semnificativ.
Pentru p < 0.05 sunt necesare cel puțin 6 dezacorduri, toate în aceeași direcție.

## Decizie
Rămânem fără stemming (varianta mai simplă).

## Ce am învățat
- O diferență de 2 întrebări din 42 nu înseamnă nimic fără un test.
- Contează doar întrebările la care variantele nu sunt de acord.
- Pentru comparații fine ne trebuie mai multe întrebări sau o metrică mai fină
  (poziția bucății corecte, MRR).

# BM25 baseline

## Setup
- Corpus: 1183 de chunk-uri (fără release-notes.md)
- Set de evaluare: 42 de întrebări generate cu LLM, o singură bucată relevantă pe întrebare
- BM25: k1 = 1.5, b = 0.75, fără stemming
- Rezultate căutate: primele 10

## Rezultate
| k | recall@k |
|---|---|
| 1 | 0.548 (23/42) |
| 2

# Embeddings și căutare hibridă

## Setup
- Embeddings: all-MiniLM-L6-v2 (sentence-transformers, local), vectori normalizați,
  similaritate cosinus (produs scalar)
- Hibrid: RRF (Reciprocal Rank Fusion), scor = Σ 1/(60 + poziție),
  primele 50 de rezultate din fiecare sistem
- Același corpus (1183 de chunk-uri) și același set de evaluare (42 de întrebări)

## Rezultate
| | BM25 | Embeddings | Hibrid |
|---|---|---|---|
| recall@1 | 0.548 | 0.405 | 0.595 |
| recall@5 | 0.738 | 0.643 | 0.786 |
| recall@10 | 0.762 | 0.786 | 0.857 |
| MRR | 0.621 | 0.531 | 0.681 |
| nDCG@10 | 0.656 | 0.592 | 0.723 |

## BM25 față de embeddings (top 10)
| | Embeddings: nu găsește | Embeddings: găsește |
|---|---|---|
| BM25: nu găsește | 6 | 4 |
| BM25: găsește | 3 | 29 |

- La performanță, practic la egalitate: dezacorduri 3 față de 4.
- Găsesc întrebări diferite: 7 întrebări găsite doar de unul dintre sisteme.
- Plafonul teoretic al combinării: 29 + 3 + 4 = 36/42 = 0.857.

## Observații
- BM25 e mai bun sus în listă (recall@1, recall@5): documentația tehnică are
  cuvinte exacte (Depends, Query) pe care BM25 le prinde bine.
- Embeddings-urile prind mai mult la k mare: leagă sensuri fără cuvinte comune.
- Posibile limite ale embeddings: model mic și general; bucățile lungi sunt
  tăiate după ~256 de tokeni.
- Hibridul atinge exact plafonul de 36/42 la recall@10 și e cel mai bun la
  toate metricile.
- 6 întrebări nu sunt găsite de niciun sistem.

## De ce RRF și nu media armonică
Media armonică a pozițiilor e RRF cu constanta 0. Cu 0, primul loc dintr-o
singură listă domină; cu 60, contează mai mult acordul dintre sisteme.
RRF folosește poziții, nu scoruri, pentru că scorurile BM25 și cosinusurile
sunt pe scări diferite.

## Semnificație (deschis)
Hibrid față de BM25, recall@10: +4 întrebări. Chiar cu 4–0, testul semnului
dă p = 0.125, deci nu e semnificativ. Testul pe „nimerit sau nu” pierde
informație. Următorul pas: test de permutare pe perechi, pe valorile 1/poziție.