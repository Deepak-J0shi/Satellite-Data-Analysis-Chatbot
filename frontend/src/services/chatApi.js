import api from "./api";

export async function sendMessage(message, sessionId=null) {

  const response = await api.post("/api/chat", {
    message,
    session_id: sessionId,
  });

  return response.data;
}