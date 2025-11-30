import { Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";

import Landing from "./pages/Landing.jsx";
import Admin from "./pages/Admin.jsx";
import Chat from "./pages/Chat.jsx";
import Upload from "./pages/Upload.jsx";

import Contact from "./pages/Contact.jsx";
import Pricing from "./pages/Pricing.jsx";
import Features from "./pages/Features.jsx";

export default function App() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/upload" element={<Upload />} />

        {/* Newly added */}
        <Route path="/contact" element={<Contact />} />
        <Route path="/pricing" element={<Pricing />} />
        <Route path="/features" element={<Features />} />
      </Routes>

      <Footer />
    </>
  );
}
