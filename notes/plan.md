# Plan: jumătate statistică, jumătate cod

## Ritmul zilnic
- Dimineața (minte proaspătă): statistică. ~1 oră de citit, 1–2 ore de exerciții pe hârtie.
- După-amiaza: cod, pe mini-rag.
- La finalul fiecărei săptămâni: o sarcină care aplică statistica pe mini-rag.

## Cărți
- Blitzstein și Hwang, „Introduction to Probability” (PDF gratuit; cursul Stat 110 pe YouTube)
- Wasserman, „All of Statistics” (capitolele de inferență)
Numerotarea capitolelor poate diferi între ediții: verifică după titlu.

## Săptămâna 1
- Statistică: Blitzstein cap. 1–3 (numărare, probabilitate condiționată, variabile
  aleatoare discrete, binomial).
- Cod: finalizare Etapa 2: test de permutare pe perechi, bootstrap pentru intervale
  de încredere.
- Aplicare: testul semnului de mână, apoi permutarea pe MRR, hibrid față de BM25.

## Săptămâna 2
- Statistică: Blitzstein cap. 4–5 (medie, varianță, distribuții continue, normala)
  și capitolul cu legea numerelor mari și teorema limită centrală.
- Cod: reranker (cross-encoder) peste hibrid.
- Aplicare: de ce recall@5 pe 42 de întrebări are o eroare de ±13 puncte;
  câte întrebări ne trebuie pentru ±5.

## Săptămâna 3
- Statistică: Wasserman, capitolele despre estimare și intervale de încredere.
- Cod: Etapa 3: răspunsuri generate cu surse.
- Aplicare: interval de încredere pentru fiecare metrică din tabelul de rezultate.

## Săptămâna 4
- Statistică: Wasserman, capitolul despre bootstrap.
- Cod: LLM-judecător, calibrat pe 30 de răspunsuri evaluate de mine.
- Aplicare: cât de des e de acord judecătorul cu mine, cu interval bootstrap.

## Săptămâna 5
- Statistică: Wasserman, capitolul despre testarea ipotezelor (p-value,
  teste de permutare, teste multiple).
- Cod: Etapa 4: buclă de tool calling, fără framework.
- Aplicare: ce se întâmplă cu p-value-urile când compar 10 configurații deodată.

## Săptămâna 6
- Statistică: puterea testelor și dimensiunea eșantionului.
- Cod: LangGraph (classify → retrieve → rerank → synthesize), bazele MCP.
- Aplicare: extinderea setului de evaluare la numărul de întrebări calculat.

## Săptămâna 7
- Statistică: varianța sistemelor nedeterministe (rulări repetate ale LLM-ului).
- Cod: Etapa 5: API FastAPI, Docker Compose, evaluarea ca poartă în CI.
- Aplicare: un prag pentru poarta din CI care ține cont de zgomot, ca să nu
  pice build-ul din cauza norocului.