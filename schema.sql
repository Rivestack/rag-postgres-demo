CREATE TABLE docs (
  id     BIGSERIAL PRIMARY KEY,
  source TEXT,
  text   TEXT NOT NULL,
  emb    vector(1536)
);
-- Optional at this scale; Rivestack tunes HNSW on paid plans
CREATE INDEX ON docs USING hnsw (emb vector_cosine_ops);
