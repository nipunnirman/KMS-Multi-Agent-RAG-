import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User } from 'lucide-react';
import type { CitationRenderer as _CitationRendererType } from './components/CitationRenderer';
import { CitationRenderer } from './components/CitationRenderer';
import type { QAResponse } from './citation.types';
import './App.css';
import './citation.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  citations?: QAResponse['citations'];
}

function App() {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || loading) return;

    const userMsg: Message = { role: 'user', content: question };
    setMessages(prev => [...prev, userMsg]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await fetch('/qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMsg.content }),
      });

      if (!res.ok) throw new Error('Failed to fetch response');

      const data: QAResponse = await res.json();

      const aiMsg: Message = {
        role: 'assistant',
        content: data.answer,
        citations: data.citations
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg: Message = { role: 'assistant', content: "Sorry, I encountered an error answering that." };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="logo">
          <div className="logo-icon">
            <Bot size={24} color="#fff" />
          </div>
          <h1>Vector DB Assistant</h1>
        </div>
      </header>

      <main className="chat-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">
              <Bot size={48} />
            </div>
            <h2>How can I help you today?</h2>
            <p>Ask me anything about vector databases, indexing, or RAG.</p>
            <div className="example-questions">
              <button onClick={() => setQuestion("What are the advantages of vector databases?")}>
                "What are the advantages of vector databases?"
              </button>
              <button onClick={() => setQuestion("Explain HNSW indexing.")}>
                "Explain HNSW indexing."
              </button>
            </div>
          </div>
        ) : (
          <div className="messages-list">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-row ${msg.role}`}>
                <div className="avatar">
                  {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                </div>
                <div className="message-content">
                  {msg.role === 'user' ? (
                    <p>{msg.content}</p>
                  ) : (
                    <CitationRenderer text={msg.content} citations={msg.citations || null} />
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message-row assistant">
                <div className="avatar"><Bot size={20} /></div>
                <div className="message-content loading">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </main>

      <footer className="input-area">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
            disabled={loading}
          />
          <button type="submit" disabled={!question.trim() || loading}>
            <Send size={20} />
          </button>
        </form>
      </footer>
    </div>
  );
}

export default App;
