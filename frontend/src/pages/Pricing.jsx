export default function Pricing() {
  return (
    <section className="max-w-4xl mx-auto py-20 px-4">
      <h1 className="text-3xl font-bold mb-4">Pricing</h1>

      <p className="text-slate-300 mb-6">
        Choose a plan that fits your hiring workflow.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="bg-slate-900/60 border border-slate-700 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-2">Free</h2>
          <p className="text-slate-400 text-sm mb-4">Try the essentials</p>
          <ul className="text-slate-300 text-sm space-y-2">
            <li>✓ CV Skill Extraction</li>
            <li>✓ Chat with AI</li>
          </ul>
        </div>

        <div className="bg-slate-900/60 border border-indigo-500 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-2">Pro</h2>
          <p className="text-slate-400 text-sm mb-4">For active hiring teams</p>
          <ul className="text-slate-300 text-sm space-y-2">
            <li>✓ Unlimited Uploads</li>
            <li>✓ Advanced AI Insights</li>
          </ul>
        </div>

        <div className="bg-slate-900/60 border border-pink-500 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-2">Enterprise</h2>
          <p className="text-slate-400 text-sm mb-4">Custom solutions</p>
          <ul className="text-slate-300 text-sm space-y-2">
            <li>✓ API Access</li>
            <li>✓ Dedicated Support</li>
          </ul>
        </div>
      </div>
    </section>
  );
}
