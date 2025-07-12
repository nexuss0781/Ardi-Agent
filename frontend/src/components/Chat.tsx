import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// --- Type Definitions ---
interface Message {
  sender: 'user' | 'agent';
  text: string;
}

// --- Component Props ---
interface ChatProps {
  runId: string | null;
  setRunId: (runId: string) => void;
}

// --- Main Component ---
const Chat: React.FC<ChatProps> = ({ runId, setRunId }) => {
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'agent', text: "Hello! What can I build for you today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // This is the API call to start the agent workflow
      const response = await axios.post(`${API_BASE_URL}/project/start`, {
        initial_request: input
      });
      
      const newRunId = response.data.run_id;
      setRunId(newRunId); // Save the new run ID to the parent state

      const agentResponse: Message = { 
        sender: 'agent', 
        text: `Project started with ID: ${newRunId}. The agent is now working.` 
      };
      setMessages(prev => [...prev, agentResponse]);

    } catch (err) {
      console.error("Error starting project:", err);
      const errorResponse: Message = {
        sender: 'agent',
        text: "Sorry, I couldn't start the project. Please ensure the backend is running."
      };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <p>{msg.text}</p>
          </div>
        ))}
        {isLoading && <div className="message agent loading"><p>Thinking...</p></div>}
      </div>
      <form className="chat-input-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Describe your project..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>Send</button>
      </form>
    </div>
  );
};

export default Chat;