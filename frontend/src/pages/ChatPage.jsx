import { useState } from "react";

import {
  Send,
  Pin,
} from "lucide-react";

import { sendMessage } from "../services/chatApi";

export default function ChatPage() {

  const [input, setInput] = useState("");

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([]);

  const [sessionId, setSessionId] = useState(null);

  async function handleSend() {

    if (!input.trim()) return;

    const userMessage = input;

    setInput("");

    // Add User Message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    try {

      setLoading(true);

      const response = await sendMessage(
        userMessage,
        sessionId
      );

      console.log("Backend Response:", response);

      // Save Session
      if (!sessionId && response.session_id) {
        setSessionId(response.session_id);
      }

      // Add Assistant Message
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          reply: response.reply,
          preview_url: response.preview_url,
        },
      ]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          reply: "Error while processing request.",
        },
      ]);

    } finally {

      setLoading(false);

    }
  }

  return (

    <div className="h-screen flex flex-col bg-slate-50 dark:bg-[#0f172a] transition-all duration-300">

      {/* Header */}
      <div className="bg-white dark:bg-[#111827] border-b border-slate-200 dark:border-slate-800 px-8 py-4">

        <div className="max-w-5xl mx-auto">

          <h1 className="text-2xl font-semibold tracking-tight text-slate-900 dark:text-white">
            Satellite Analysis Workspace
          </h1>

          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            AI-powered geospatial intelligence and visualization
          </p>

        </div>

      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-8">

        <div className="max-w-5xl mx-auto space-y-6">

          {messages.map((msg, index) => (

            <div key={index}>

              {/* USER MESSAGE */}
              {msg.role === "user" && (

                <div className="flex justify-end">

                  <div className="bg-blue-600 text-white px-5 py-4 rounded-2xl max-w-2xl">
                    {msg.content}
                  </div>

                </div>
              )}

              {/* ASSISTANT MESSAGE */}
              {msg.role === "assistant" && (

                <div className="bg-white dark:bg-[#111827] border border-slate-200 dark:border-slate-800 rounded-2xl p-6 transition-all duration-300">

                  {/* Reply */}
                  <p className="text-slate-700 dark:text-slate-300 leading-8 whitespace-pre-wrap">

                    {msg.reply}

                  </p>

                  {/* Preview Section */}
                  {msg.preview_url && (

                    <div className="mt-6 space-y-4">

                      {/* Preview Image */}
                      <div className="rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800">

                        <img
                          src={msg.preview_url}
                          alt="Satellite Preview"
                          className="w-full object-cover"
                        />

                      </div>

                      {/* URL Box */}
                      <div className="bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 overflow-x-auto">

                        <p className="text-sm text-slate-600 dark:text-slate-400 break-all">

                          {msg.preview_url}

                        </p>

                      </div>

                    </div>
                  )}

                  {/* Actions */}
                  <div className="mt-5 flex justify-end">

                    <button className="flex items-center gap-2 border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 px-5 py-3 rounded-xl transition-all">

                      <Pin size={16} />
                      Pin to Dashboard

                    </button>

                  </div>

                </div>
              )}

            </div>
          ))}

          {/* Loading */}
          {loading && (

            <div className="text-slate-500 dark:text-slate-400">

              Processing analysis...

            </div>

          )}

        </div>

      </div>

      {/* Input */}
      <div className="bg-white dark:bg-[#111827] border-t border-slate-200 dark:border-slate-800 px-6 py-5">

        <div className="max-w-5xl mx-auto flex gap-4">

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about NDVI, SAR, flood mapping..."
            className="flex-1 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white placeholder:text-slate-400 rounded-2xl px-5 py-4 outline-none"
          />

          <button
            onClick={handleSend}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 rounded-2xl transition-all"
          >

            <Send size={18} />

          </button>

        </div>

      </div>

    </div>
  );
}