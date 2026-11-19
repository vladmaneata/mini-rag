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