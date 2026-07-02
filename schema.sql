CREATE TABLE IF NOT EXISTS docs (
  id     BIGSERIAL PRIMARY KEY,
  source TEXT,
  text   TEXT NOT NULL,
  emb    vector(1536)
);
-- Optional at this scale; Rivestack tunes HNSW on paid plans
CREATE INDEX IF NOT EXISTS docs_emb_idx ON docs USING hnsw (emb vector_cosine_ops);
