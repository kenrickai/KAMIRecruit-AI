export default function Landing() {
  return (
    <section className="bg-gradient-to-br from-indigo-500 to-purple-600 text-white py-32">
      <div className="max-w-6xl mx-auto text-center px-6">
        <h1 className="text-5xl font-bold leading-tight">
          Intelligent Talent Screening with KAMIRecruit AI
        </h1>

        <p className="mt-6 text-lg opacity-90">
          Upload a CV → Extract Skills → Chat with AI → Get Instant Insights.
        </p>

        <a
        href="/upload"
        className="mt-10 inline-block bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:scale-105 transition"
      >
        Try Free Now
        </a>
      </div>
    </section>
  );
}
