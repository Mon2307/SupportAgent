import { useState } from "react";
import { askAndWait, QueryModel } from "./api";

interface Turn {
  question: string;
  result?: QueryModel;
  error?: string;
}

function sourceLabel(source: string) {
  const [path, start] = source.split(/:(?=\d+$)/);
  const rel = path.includes("/data/") ? path.split("/data/").pop()! : path;
  return start ? `${rel} (offset ${start})` : rel;
}

export default function App() {
  const [input, setInput] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: any) {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setInput("");
    setLoading(true);
    setTurns((t) => [...t, { question }]);

    const update = (patch: Partial<Turn>) =>
      setTurns((t) => t.map((turn, i) => (i === t.length - 1 ? { ...turn, ...patch } : turn)));

    try {
      update({ result: await askAndWait(question) });
    } catch (err) {
      update({ error: err instanceof Error ? err.message : String(err) });
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Support Agent</h1>

      <section className="turns">
        {turns.length === 0 && <p className="muted">Ask a question about the support docs.</p>}
        {turns.map((turn, i) => (
          <article key={i} className="turn">
            <p className="question">{turn.question}</p>
            {turn.error && <p className="error">{turn.error}</p>}
            {!turn.result && !turn.error && <p className="muted">Thinking…</p>}
            {turn.result && (
              <>
                <p className="answer">{turn.result.answer_text}</p>
                {turn.result.sources.length > 0 && (
                  <details>
                    <summary>Sources ({turn.result.sources.length})</summary>
                    <ul>
                      {turn.result.sources.map((s) => (
                        <li key={s}>{sourceLabel(s)}</li>
                      ))}
                    </ul>
                  </details>
                )}
              </>
            )}
          </article>
        ))}
      </section>

      <form onSubmit={onSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question…"
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={loading || !input.trim()}>
          {loading ? "Waiting…" : "Ask"}
        </button>
      </form>
    </main>
  );
}
