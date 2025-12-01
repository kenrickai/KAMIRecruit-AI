// -----------------------------
// API Base URL
// -----------------------------
// frontend/src/api/apiClient.js
const API_BASE = import.meta.env.VITE_API_BASE || "";


// Core request helper
async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  return res.json();
}

// -----------------------------
// AI Chat
// -----------------------------
export async function chatWithAI(message) {
  return request("/api/chat", {
    method: "POST",
    body: JSON.stringify({ message }),
  });
}

// -----------------------------
// Resume Upload (multipart/form-data)
// -----------------------------
export async function uploadResume(formData) {
  const res = await fetch(`${API_BASE}/api/upload-resume`, {
    method: "POST",
    body: formData, // <-- no content-type needed, browser sets it
  });

  return res.json();
}

// -----------------------------
// Generic API wrapper
// -----------------------------
export const api = {
  get: (path) => request(path),
  post: (path, body) =>
    request(path, {
      method: "POST",
      body: JSON.stringify(body),
    }),
};

export default api;
