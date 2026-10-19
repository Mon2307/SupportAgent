const API_URL = import.meta.env.VITE_API_URL.replace(/\/$/, "");

export interface QueryModel {
  query_id: string;
  create_time: number;
  query_text: string;
  answer_text: string | null;
  sources: string[];
  is_complete: boolean;
}

export async function submitQuery(queryText: string): Promise<QueryModel> {
  const res = await fetch(`${API_URL}/submit_query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query_text: queryText }),
  });
  if (!res.ok) throw new Error(`submit_query failed: ${res.status}`);
  return res.json();
}

export async function getQuery(queryId: string): Promise<QueryModel | null> {
  const res = await fetch(`${API_URL}/get_query?query_id=${encodeURIComponent(queryId)}`);
  if (!res.ok) throw new Error(`get_query failed: ${res.status}`);
  return res.json();
}

export async function askAndWait(
  queryText: string,
  { intervalMs = 500, timeoutMs = 90000 } = {}
): Promise<QueryModel> {
  let query = await submitQuery(queryText);
  const deadline = Date.now() + timeoutMs;
  while (!query.is_complete) {
    if (Date.now() > deadline) throw new Error("Timed out waiting for an answer");
    await new Promise((r) => setTimeout(r, intervalMs));
    query = (await getQuery(query.query_id)) ?? query;
  }
  return query;
}
