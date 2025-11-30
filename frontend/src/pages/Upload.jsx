import ResumeUpload from "../components/ResumeUpload.jsx";

export default function Upload() {
  return (
    <section className="max-w-4xl mx-auto px-4 py-10 md:py-16">
      <h1 className="text-2xl md:text-3xl font-bold mb-2">
        Upload your CV & discover your skill story
      </h1>
      <p className="text-sm text-slate-300 mb-6 max-w-xl">
        We’ll parse your resume, extract key skills, and surface them in a way
        that’s easier to discuss with NGOs and mission-driven organizations.
      </p>
      <ResumeUpload />
    </section>
  );
}
