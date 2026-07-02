# Build a RAG Chatbot with Just PostgreSQL — no vector database

![Demo](demo.gif)

▶️ **[Watch the video walkthrough](https://www.youtube.com/@rivestackio)**

A complete, working RAG pipeline in ~160 lines of Python. No LangChain, no Pinecone, no framework — one Postgres table, one SQL query, and two OpenAI calls. That's the whole trick.

## Why no Pinecone?

| | Postgres + pgvector | Dedicated vector DB |
|---|---|---|
| Your embeddings live | next to your app data | in a second system to sync |
| Filtering & joins | plain SQL | vendor query DSL |
| Bills to pay | one | two |
| Vector search p50 | [~3.7 ms on a $15 Rivestack node](https://rivestack.io/pgvector-benchmarks) | comparable, plus network hop |

## Quickstart

1. **Create a free Postgres database** at [rivestack.io](https://rivestack.io) — pgvector comes enabled, nothing to install.
2. **Copy the connection string** from your dashboard, then `cp .env.example .env` and paste it in (plus your OpenAI key).
3. **Create the table** — paste `schema.sql` into the dashboard's SQL editor, or run:
   ```bash
   psql "$DATABASE_URL" -f schema.sql
   ```
4. **Ingest the knowledge base** (15 markdown files in `docs/` — swap in your own):
   ```bash
   pip install -r requirements.txt
   python ingest.py
   ```
5. **Ask it something:**
   ```bash
   python rag.py "How do I rotate an API key?"
   ```

Want a UI? `uvicorn app:app --reload` and open http://127.0.0.1:8000.

## How it works

RAG is simpler than the ecosystem makes it look:

1. `ingest.py` splits each markdown file into ~500-word chunks and inserts them with an embedding (OpenAI `text-embedding-3-small`, 1536 dimensions).
2. `rag.py` embeds your **question** with the same model, then retrieval is **one SQL query**:

   ```sql
   SELECT source, text, emb <=> %s::vector AS dist
   FROM docs WHERE emb IS NOT NULL
   ORDER BY dist
   LIMIT 3;
   ```

   `<=>` is pgvector's cosine-distance operator; the HNSW index makes it fast.
3. The top 3 chunks become the context for `gpt-4o-mini`, with a system prompt that says: answer **only** from this context and cite your sources in `[brackets]`.

No orchestration layer, no retriever abstraction, no "chains" — a database doing what databases do.

## How fast is the retrieval?

The CLI and the web UI print the **in-database search time** on every question — Postgres's own measurement via `EXPLAIN ANALYZE`, so it doesn't change with your distance from the database. See for yourself:

```
EXPLAIN ANALYZE SELECT source, text FROM docs ORDER BY emb <=> '[...]'::vector LIMIT 3;

 Limit  (actual time=0.62..0.64 rows=3 loops=1)
   ->  Index Scan using docs_emb_idx on docs  (actual time=0.61..0.63 rows=3 loops=1)
         Order By: (emb <=> '[...]'::vector)
 Execution Time: 0.74 ms
```

Sub-millisecond in-database at this scale. At 250k × 1536-dim vectors, a $15 Rivestack node sustains ~1,000 QPS at a 3.7 ms p50 — measured with [pgvector-bench](https://rivestack.io/pgvector-bench), an open-source CLI you can point at your own database to reproduce the numbers.

## Works on any Postgres

Nothing here is Rivestack-specific — it runs against any PostgreSQL 15+ with the pgvector extension (`CREATE EXTENSION vector;` first if your provider doesn't pre-enable it). If something else populates your `emb` column (a pipeline, a trigger, a batch job), run `python ingest.py --no-embed` to insert text only.

Rivestack is simply the fastest way to get there: free tier, pgvector pre-enabled, NVMe storage, and a built-in [semantic search UI](https://rivestack.io/#semantic-search) to eyeball your vectors without writing code.

## Get started

Spin up the free tier at **[rivestack.io](https://rivestack.io)** — no credit card, Postgres with pgvector ready in 60 seconds.

Upgrading to a dedicated $15/mo Solo node? Use promo code **FIRSTMONTHFREE** for an extra month free.

---

MIT licensed. The `docs/` folder documents **Driftline**, a fictional uptime-monitoring product invented for this demo — swap in your own docs and the pipeline doesn't change.
