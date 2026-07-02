"""Ask questions over the docs table. The entire retrieval step is one SQL query."""
import os
import sys

import psycopg2
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
for var in ("DATABASE_URL", "OPENAI_API_KEY"):
    if not os.getenv(var):
        sys.exit(f"{var} is not set — copy .env.example to .env and fill it in.")
client = OpenAI()

SYSTEM = ("Answer the question using ONLY the context below. Cite the source files you used "
          "in [brackets]. If the context doesn't contain the answer, say you don't know.\n\n")


def search(question: str, k: int = 3) -> tuple[list[tuple[str, str, float]], float]:
    """Embed the question, then let Postgres find the k nearest chunks."""
    q_emb = client.embeddings.create(model="text-embedding-3-small", input=question).data[0].embedding
    # This is the whole vector search: <=> is pgvector's cosine distance.
    sql = ("SELECT source, text, emb <=> %s::vector AS dist "
           "FROM docs WHERE emb IS NOT NULL ORDER BY dist LIMIT %s")
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute(sql, (str(q_emb), k))
        hits = cur.fetchall()
        # Ask Postgres what the search cost — measured, not guessed, network-independent.
        cur.execute("EXPLAIN (ANALYZE, FORMAT JSON) " + sql, (str(q_emb), k))
        query_ms = cur.fetchone()[0][0]["Execution Time"]
    if not hits:
        raise RuntimeError("No embedded chunks in the docs table — run `python ingest.py` first.")
    return hits, query_ms


def ask(question: str) -> tuple[str, list[str], float]:
    """Retrieve context, then have the model answer from it (and only it)."""
    hits, query_ms = search(question)
    context = "\n\n".join(f"[{source}]\n{text}" for source, text, _ in hits)
    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM + context},
            {"role": "user", "content": question},
        ],
    )
    sources = list(dict.fromkeys(source for source, _, _ in hits))  # dedupe, keep rank order
    return reply.choices[0].message.content or "", sources, query_ms


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python rag.py "How do I rotate an API key?"')
    try:
        answer, sources, query_ms = ask(" ".join(sys.argv[1:]))
    except RuntimeError as err:
        sys.exit(str(err))
    print(f"\n{answer}\n")
    print(f"sources: {', '.join(sources)}")
    print(f"vector search (in-DB): {query_ms:.2f} ms")
