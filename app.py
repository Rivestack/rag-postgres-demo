"""Optional web UI — the same rag.py functions behind a one-page chat.
Run: uvicorn app:app --reload   then open http://127.0.0.1:8000"""
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from rag import ask

app = FastAPI(title="rag-postgres-demo")


@app.post("/ask")
def ask_route(question: str = Body(embed=True)) -> dict:
    try:
        answer, sources, query_ms = ask(question)
    except RuntimeError as err:  # empty docs table
        raise HTTPException(status_code=400, detail=str(err))
    return {"answer": answer, "sources": sources, "query_ms": round(query_ms, 2)}


PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>RAG on Postgres</title><style>
  body{background:#0b0e14;color:#e6e6e6;font:16px/1.6 system-ui;max-width:640px;margin:48px auto;padding:0 16px}
  h1{font-size:20px;font-weight:600} small{color:#8b93a7}
  input{width:100%;padding:12px 14px;border-radius:8px;border:1px solid #2a2f3a;background:#12161f;color:#e6e6e6;font-size:15px;margin-top:16px}
  #answer{white-space:pre-wrap;margin-top:24px} .src{color:#8b93a7;font-size:13px;margin-top:12px}
  .ms{display:inline-block;background:#16324f;color:#7cc0ff;border-radius:99px;padding:2px 10px;font-size:12px;margin-top:12px}
</style></head><body>
<h1>Ask the Driftline docs</h1>
<small>RAG on plain PostgreSQL — no vector database</small>
<input id="q" placeholder="How do I rotate an API key?  (press Enter)" autofocus>
<div id="answer"></div><div class="src" id="sources"></div><div id="ms"></div>
<script>
q.addEventListener("keydown", async e => {
  if (e.key !== "Enter" || !q.value.trim()) return;
  answer.textContent = "thinking…"; sources.textContent = ""; ms.textContent = "";
  const r = await fetch("/ask", {method: "POST", headers: {"Content-Type": "application/json"},
                                 body: JSON.stringify({question: q.value})});
  const d = await r.json().catch(() => ({detail: "server error — check your .env and the terminal logs"}));
  if (!r.ok) { answer.textContent = d.detail || "server error"; return; }
  answer.textContent = d.answer;
  sources.textContent = "sources: " + d.sources.join(", ");
  ms.innerHTML = `<span class="ms">in-DB vector search ${d.query_ms} ms</span>`;
});
</script></body></html>"""


@app.get("/")
def index() -> HTMLResponse:
    return HTMLResponse(PAGE)
