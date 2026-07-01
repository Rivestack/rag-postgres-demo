"""Load the markdown knowledge base into Postgres.

Chunks every docs/*.md file and inserts (source, text, emb). Embeddings use
OpenAI text-embedding-3-small — the same model rag.py embeds questions with, so
the cosine distances line up. --no-embed skips embedding and leaves emb NULL."""
import argparse
import os
import sys
from collections.abc import Iterator
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from openai import OpenAI


def chunk(text: str, size: int = 500) -> Iterator[str]:
    # Word-based chunks: crude but transparent, and ~500 words ≈ one topic.
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i : i + size])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-embed", action="store_true", help="insert text only, leave emb NULL")
    args = parser.parse_args()

    load_dotenv()
    for var in ["DATABASE_URL"] + ([] if args.no_embed else ["OPENAI_API_KEY"]):
        if not os.getenv(var):
            sys.exit(f"{var} is not set — copy .env.example to .env and fill it in.")

    client = None if args.no_embed else OpenAI()
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE docs")  # re-runs replace the corpus instead of duplicating it
        for path in sorted((Path(__file__).parent / "docs").glob("*.md")):
            for piece in chunk(path.read_text(encoding="utf-8")):
                if client is None:
                    cur.execute("INSERT INTO docs (source, text) VALUES (%s, %s)", (path.name, piece))
                else:
                    emb = client.embeddings.create(model="text-embedding-3-small", input=piece).data[0].embedding
                    cur.execute("INSERT INTO docs (source, text, emb) VALUES (%s, %s, %s::vector)",
                                (path.name, piece, str(emb)))
            print(f"ingested {path.name}")
        cur.execute("SELECT count(*) FROM docs")
        print(f"{cur.fetchone()[0]} chunks in the docs table")


if __name__ == "__main__":
    main()
