import React, { useState, useRef, useEffect } from 'react';
import { Send, X, MessageSquare, Loader2 } from 'lucide-react';

const ChatInterface = ({ documentation, onClose }) => {
    const [messages, setMessages] = useState([
        {
            role: 'model',
            content:
                'Hi! I can help you answer questions about your codebase based on the generated documentation. What would you like to know?'
        }
    ]);

    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [error, setError] = useState(null);

    const messagesEndRef = useRef(null);

    const API_BASE = import.meta.env.VITE_API_BASE_URL;

    // Scroll to bottom when messages update
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    // ---------------------------
    // Initialize Chat Session
    // ---------------------------
    const initializeChat = async () => {
        try {
            const response = await fetch(`${API_BASE}/api/chat/initialize`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ documentation })
            });

            if (!response.ok) throw new Error('Initialization failed');

            const data = await response.json();
            setSessionId(data.sessionId);
            return data.sessionId;

        } catch (err) {
            console.error("Chat initialization error:", err);
            setError("Unable to connect to chat service.");
            return null;
        }
    };

    useEffect(() => {
        if (documentation && !sessionId) {
            initializeChat();
        }
    }, [documentation]);

    // ---------------------------
    // Send Message
    // ---------------------------
    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        let activeSession = sessionId;

        if (!activeSession) {
            activeSession = await initializeChat();
            if (!activeSession) return;
        }

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const history = messages.map(msg => ({
                role: msg.role,
                content: msg.content
            }));

            let response = await fetch(`${API_BASE}/api/chat/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sessionId: activeSession,
                    message: userMessage,
                    history
                })
            });

            // If session expired → recreate
            if (response.status === 404) {
                const newSession = await initializeChat();
                if (!newSession) throw new Error("Reinitialization failed");

                response = await fetch(`${API_BASE}/api/chat/message`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        sessionId: newSession,
                        message: userMessage,
                        history
                    })
                });
            }

            if (!response.ok) {
                const errText = await response.text();
                throw new Error(errText);
            }

            const data = await response.json();

            setMessages(prev => [
                ...prev,
                { role: 'model', content: data.response }
            ]);

        } catch (err) {
            console.error("Chat error:", err);
            setMessages(prev => [
                ...prev,
                {
                    role: 'model',
                    content: "Sorry, I encountered an error. Please try again."
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white rounded-2xl shadow-2xl overflow-hidden border border-gray-200">

            {/* Header */}
            <div className="p-5 border-b border-gray-200 flex justify-between items-center bg-gray-50">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                    <MessageSquare className="w-5 h-5 mr-2 text-indigo-600" />
                    Chat with Codebase
                </h3>
                <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-gray-600 transition"
                >
                    <X className="w-6 h-6" />
                </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5 bg-gray-50">

                {error && (
                    <div className="bg-red-100 text-red-600 p-3 rounded-lg text-sm">
                        {error}
                    </div>
                )}

                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                        <div
                            className={`max-w-[75%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                                msg.role === 'user'
                                    ? 'bg-indigo-600 text-white'
                                    : 'bg-white text-gray-800 border border-gray-200 shadow-sm'
                            }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div className="flex justify-start">
                        <div className="bg-white border border-gray-200 px-4 py-3 rounded-xl shadow-sm">
                            <Loader2 className="w-4 h-4 animate-spin text-gray-500" />
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-5 bg-white border-t border-gray-200">
                <form onSubmit={handleSendMessage} className="flex gap-3">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask about your project..."
                        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none text-gray-900"
                        disabled={isLoading}
                    />
                    <button
                        type="submit"
                        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50"
                        disabled={isLoading}
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </form>
            </div>

        </div>
    );
};

export default ChatInterface;
