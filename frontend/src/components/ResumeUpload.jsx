import { useState } from "react";
import { api } from "../api/client";

export default function ResumeUpload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [skills, setSkills] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setStatus("Please choose a PDF file.");
      return;
    }

    setStatus("Uploading & processing...");
    setSkills([]);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/process_resume", formData);
      const data = res.data;

      setSkills(data.skills || []);
      setStatus("Done!");
    } catch (err) {
      console.error(err);
      setStatus("Something went wrong while processing the CV.");
    }
  };

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-6 space-y-4">
      <h2 className="text-lg font-semibold text-slate-50">
        Upload your CV (PDF)
      </h2>
      <p className="text-xs text-slate-400">
        We will extract key skills and show them here. This is a prototype —
        don’t upload confidential documents.
      </p>

      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0] || null)}
          className="block w-full text-xs text-slate-200 
                     file:mr-3 file:py-1.5 file:px-3 file:rounded-full 
                     file:border-0 file:text-xs file:font-semibold
                     file:bg-indigo-500 file:text-white
                     hover:file:bg-indigo-600
                     bg-slate-900 border border-slate-700 rounded-lg px-3 py-2"
        />
        <button
          type="submit"
          className="w-full py-2 rounded-lg bg-gradient-to-r from-indigo-500 to-pink-500 
                     text-xs font-semibold tracking-wide hover:from-indigo-400 hover:to-pink-400"
        >
          Process CV
        </button>
      </form>

      {status && <p className="text-xs text-slate-300">{status}</p>}

      {skills.length > 0 && (
        <div className="mt-3">
          <h3 className="text-xs font-semibold text-slate-200 mb-2">
            Extracted Skills
          </h3>
          <div className="flex flex-wrap gap-2">
            {skills.map((skill) => (
              <span
                key={skill}
                className="px-2 py-1 rounded-full bg-slate-800 text-[11px] text-slate-100"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
