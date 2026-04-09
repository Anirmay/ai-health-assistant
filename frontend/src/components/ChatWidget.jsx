import React, { useState, useRef, useEffect, forwardRef, useImperativeHandle } from 'react';

const ChatWidget = forwardRef(({ disease, symptoms, confidence, riskLevel }, ref) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      text: 'Hi! I\'m your AI health assistant. Feel free to ask me any questions about your symptoms or the detected condition.',
      timestamp: new Date()
    }
  ]);
  
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const formRef = useRef(null);

  // Expose sendMessage method to parent
  useImperativeHandle(ref, () => ({
    sendMessage: (message) => {
      setInputValue(message);
      setTimeout(() => {
        const event = new Event('submit', { bubbles: false });
        formRef.current?.dispatchEvent(event);
      }, 100);
    }
  }));

  // Scroll to bottom when new messages arrive (scroll only container, not page)
  const scrollToBottom = () => {
    // Find the messages container (parent of messagesEndRef)
    const messagesContainer = messagesEndRef.current?.parentElement;
    if (messagesContainer) {
      // Use scroll within container, not scrollIntoView which affects page
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Send to chat endpoint with context
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          message: inputValue,
          context: {
            disease: disease,
            symptoms: symptoms,
            confidence: confidence,
            risk_level: riskLevel
          }
        })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.status === 'success') {
        // Extract the AI response
        const aiResponseText = data.ai_response?.answer || 'I\'m unable to generate a response at the moment.';
        
        const aiMessage = {
          id: messages.length + 2,
          type: 'ai',
          text: aiResponseText,
          follow_up: data.ai_response?.follow_up_suggestions || null,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error(data.error || 'Failed to get AI response');
      }
    } catch (err) {
      setError(err.message);
      
      // Add error message to chat
      const errorMessage = {
        id: messages.length + 2,
        type: 'error',
        text: `⚠️ ${err.message}. Please try again or refresh the page.`,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleFollowUpQuestion = async (question) => {
    // Set input value and trigger send immediately
    setInputValue(question);
    
    // Simulate form submission (bubbles: false to prevent page-level effects)
    setTimeout(() => {
      const event = new Event('submit', { bubbles: false });
      inputRef.current?.closest('form')?.dispatchEvent(event);
    }, 0);
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg shadow-2xl border border-slate-700">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 p-4 rounded-t-lg border-b border-slate-600">
        <h3 className="text-white font-bold text-lg flex items-center gap-2">
          <span className="text-xl">🤖</span>
          AI Health Assistant
        </h3>
        <p className="text-emerald-100 text-sm mt-1">Ask me anything about your symptoms</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-900">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs px-4 py-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-emerald-600 text-white rounded-br-none'
                  : message.type === 'error'
                  ? 'bg-red-900 text-red-100 rounded-bl-none'
                  : 'bg-slate-700 text-slate-100 rounded-bl-none'
              }`}
            >
              <p className="text-sm leading-relaxed">{message.text}</p>
              
              {/* Follow-up suggestions for AI messages */}
              {message.type === 'ai' && message.follow_up && message.follow_up.length > 0 && (
                <div className="mt-3 pt-3 border-t border-slate-600 space-y-2">
                  <p className="text-xs font-semibold text-slate-300">💡 Suggested follow-ups:</p>
                  {message.follow_up.slice(0, 2).map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleFollowUpQuestion(suggestion)}
                      className="block w-full text-left text-xs bg-slate-600 hover:bg-slate-500 p-2 rounded transition-colors"
                    >
                      {suggestion}
                    </button>
                  ))}
                </div>
              )}
              
              <p className="text-xs mt-2 opacity-60">
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-700 text-slate-100 px-4 py-3 rounded-lg rounded-bl-none">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-100"></div>
                  <div className="w-2 h-2 bg-slate-400 rounded-full animate-bounce delay-200"></div>
                </div>
                <span className="text-sm">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-slate-800 p-4 border-t border-slate-700 rounded-b-lg">
        <form ref={formRef} onSubmit={handleSendMessage} className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask a question... (e.g., 'Should I see a doctor?')"
            disabled={isLoading}
            className="flex-1 bg-slate-700 text-white px-4 py-2 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed placeholder-slate-400"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-6 py-2 rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span>{isLoading ? '...' : 'Send'}</span>
            <span className="text-lg">→</span>
          </button>
        </form>

        {/* Disclaimer */}
        <p className="text-xs text-slate-400 mt-3 leading-relaxed">
          ⚠️ <strong>Disclaimer:</strong> This AI is provided for informational purposes only. 
          Always consult with a healthcare professional for medical advice.
        </p>
      </div>
    </div>
  );
});

ChatWidget.displayName = 'ChatWidget';

export default ChatWidget;
