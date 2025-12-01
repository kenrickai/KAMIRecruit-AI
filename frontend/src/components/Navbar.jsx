export default function Navbar() {
  return (
    <header className="bg-white shadow sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-indigo-600">KAMIRecruit</h1>

        <nav className="space-x-6 text-slate-700 font-medium">
          <a href="/" className="hover:text-indigo-600">Home</a>
          <a href="/upload" className="hover:text-indigo-600">Upload CV</a>
          <a href="/chat" className="hover:text-indigo-600">Chat</a>
          <a href="/pricing" className="hover:text-indigo-600">Pricing</a>
          <a href="/features" className="hover:text-indigo-600">Features</a>
          <a href="/contact" className="hover:text-indigo-600">Contact</a>
        </nav>

      </div>
    </header>
  );
}
