import { useState } from "react";
import { api } from "../api/client";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    if (!input.trim()) return;

    // Show your message in UI
    setMessages((prev) => [...prev, { sender: "You", text: input }]);

    try {
      const res = await api.post("/api/chat", { message: input });
      const reply = res.data.reply || "No response received.";

      // Add AI message
      setMessages((prev) => [...prev, { sender: "AI", text: reply }]);

    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { sender: "AI", text: "Error: Unable to reach server." },
      ]);
    }

    setInput("");
  }

  return (
    <div className="min-h-screen p-6 bg-gray-100">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow-lg">

        <h1 className="text-2xl font-semibold mb-4">Chat with KAMIRecruit AI</h1>

        <div className="border h-96 overflow-y-auto p-4 rounded-lg mb-4 bg-gray-50">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`my-2 p-2 rounded-md text-sm ${
                msg.sender === "You"
                  ? "bg-blue-100 text-blue-800 self-end"
                  : "bg-gray-200 text-gray-800 self-start"
              }`}
            >
              <strong>{msg.sender}: </strong> {msg.text}
            </div>
          ))}
        </div>

        <div className="flex gap-3">
          <input
            className="flex-1 px-3 py-2 border rounded-lg"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
          />

          <button
            onClick={sendMessage}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
