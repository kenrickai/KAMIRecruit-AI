export default function Footer() {
  return (
    <footer className="bg-slate-900 text-white py-8 mt-20">
      <div className="max-w-7xl mx-auto px-6 text-center">
        <p className="text-sm opacity-70">
          © {new Date().getFullYear()} KAMIRecruit AI — All rights reserved.
        </p>
      </div>
    </footer>
  );
}
