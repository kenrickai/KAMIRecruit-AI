import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function Admin() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkHealth = async () => {
    setLoading(true);
    try {
      const res = await api.get("/api/health");
      setHealth(res.data);
    } catch (err) {
      console.error(err);
      setHealth({ status: "error", message: "Cannot reach backend" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <section className="max-w-4xl mx-auto px-4 py-10 md:py-16">
      <h1 className="text-2xl md:text-3xl font-bold mb-2">Admin Dashboard</h1>
      <p className="text-sm text-slate-300 mb-4">
        Simple observability panel for the prototype. In a full version, this
        could show CV logs, extracted skill stats, and agent traces.
      </p>

      <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-semibold text-slate-100">
            Backend Health
          </h2>
          <button
            onClick={checkHealth}
            disabled={loading}
            className="px-3 py-1.5 rounded-full bg-slate-800 text-[11px] hover:bg-slate-700 disabled:opacity-60"
          >
            {loading ? "Checking..." : "Refresh"}
          </button>
        </div>

        <pre className="text-[11px] bg-slate-950 rounded-xl p-3 text-slate-200 overflow-x-auto">
{JSON.stringify(health, null, 2) || "Waiting for response..."}
        </pre>
      </div>
    </section>
  );
}
