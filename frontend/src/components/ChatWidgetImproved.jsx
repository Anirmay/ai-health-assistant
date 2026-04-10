/**
 * Improved Chat Widget Component
 * Modern UI with proper API integration, error handling, and auto-scroll
 */

import React, { useRef, useEffect, useCallback } from 'react';
import { useHealthChat } from '../hooks/useHealthChat';

/**
 * Loading Spinner Component
 */
function LoadingSpinner() {
  return (
    <div className="flex items-center gap-2">
      <div className="flex gap-1">
        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
        <div className="w-2 h-2 bg-emerald-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
      </div>
      <span className="text-sm text-slate-300">AI is thinking...</span>
    </div>
  );
}

/**
 * Error Alert Component
 */
function ErrorAlert({ message, onDismiss }) {
  return (
    <div className="mx-4 mb-4 p-3 bg-red-900/30 border border-red-600 rounded-lg flex items-start gap-3">
      <span className="text-lg mt-0.5">⚠️</span>
      <div className="flex-1">
        <p className="text-sm text-red-200 whitespace-pre-wrap">{message}</p>
      </div>
      <button
        onClick={onDismiss}
        className="mt-1 text-red-300 hover:text-red-100 transition-colors text-lg"
        aria-label="Dismiss error"
      >
        ✕
      </button>
    </div>
  );
}

/**
 * Message Bubble Component
 */
function MessageBubble({ message }) {
  const isUser = message.type === 'user';
  const isError = message.type === 'error';
  const isSystem = message.type === 'system';

  let bubbleClass =
    'max-w-xs lg:max-w-2xl px-4 py-3 rounded-lg text-sm leading-relaxed';

  if (isUser) {
    bubbleClass += ' bg-emerald-600 text-white rounded-br-none shadow-md';
  } else if (isError) {
    bubbleClass +=
      ' bg-red-900/40 border border-red-600 text-red-100 rounded-bl-none whitespace-pre-wrap';
  } else if (isSystem) {
    bubbleClass += ' bg-slate-700 text-slate-300 rounded-bl-none italic text-xs';
  } else {
    // AI message
    bubbleClass += ' bg-gradient-to-br from-slate-700 to-slate-600 text-slate-100 rounded-bl-none shadow-md';
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div>
        <div className={bubbleClass}>
          <p className="break-words">{message.text}</p>

          {/* Response time for AI messages */}
          {message.responseTime !== undefined && (
            <p className="text-xs mt-2 opacity-60">
              ⏱️ {message.responseTime.toFixed(2)}s
            </p>
          )}

          {/* Timestamp */}
          <p className="text-xs mt-2 opacity-60">
            {message.timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </p>
        </div>
      </div>
    </div>
  );
}

/**
 * Main Chat Widget Component
 */
function ChatWidget({ disease = null, symptoms = [], confidence = 0, riskLevel = null }) {
  const {
    messages,
    isLoading,
    error,
    sentMessageCount,
    sendMessage,
    cancelRequest,
    clearError,
    clearMessages,
  } = useHealthChat([
    {
      id: 'initial',
      type: 'system',
      text: 'Welcome to AI Health Assistant. Ask me anything about your health!',
      timestamp: new Date(),
    },
  ]);

  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);
  const [inputValue, setInputValue] = React.useState('');

  /**
   * Auto-scroll to latest message
   */
  const scrollToBottom = useCallback(() => {
    if (messagesEndRef.current && messagesContainerRef.current) {
      // Use requestAnimationFrame for smooth scrolling
      requestAnimationFrame(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' });
      });
    }
  }, []);

  /**
   * Auto-scroll when messages change
   */
  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  /**
   * Focus input field when not loading
   */
  useEffect(() => {
    if (!isLoading) {
      inputRef.current?.focus();
    }
  }, [isLoading]);

  /**
   * Handle form submission
   */
  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim() || isLoading) {
      return;
    }

    const messageToSend = inputValue;
    setInputValue(''); // Clear input immediately

    // Prepare context if we have disease information
    const context = disease ? {
      disease,
      symptoms,
      confidence,
      risk_level: riskLevel,
    } : null;

    // Send message
    await sendMessage(messageToSend, context);
  };

  /**
   * Handle input change
   */
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  /**
   * Handle key down for send on Enter
   */
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  /**
   * Handle cancel button
   */
  const handleCancel = () => {
    cancelRequest();
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-slate-950 via-slate-900 to-slate-900 rounded-lg shadow-2xl border border-slate-700/50 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 px-4 py-4 border-b border-slate-600 flex items-center justify-between">
        <div>
          <h3 className="text-white font-bold text-lg flex items-center gap-2">
            <span className="text-2xl">💬</span>
            AI Health Assistant
          </h3>
          <p className="text-emerald-100 text-xs mt-1">
            {sentMessageCount > 0 ? `${sentMessageCount} question${sentMessageCount !== 1 ? 's' : ''} asked` : 'Ask me anything'}
          </p>
        </div>
        <button
          onClick={clearMessages}
          className="text-white hover:bg-emerald-700 px-3 py-1 rounded text-sm transition-colors"
          title="Clear chat history"
        >
          🗑️ Clear
        </button>
      </div>

      {/* Error Alert */}
      {error && (
        <ErrorAlert message={error} onDismiss={clearError} />
      )}

      {/* Messages Container */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-900/50 scroll-smooth"
      >
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-700/50 text-slate-100 px-4 py-3 rounded-lg rounded-bl-none border border-slate-600">
              <LoadingSpinner />
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-slate-800/50 border-t border-slate-700 px-4 py-4">
        <form onSubmit={handleSendMessage} className="space-y-3">
          {/* Input Field */}
          <div className="flex gap-2">
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your symptoms, health concerns, remedies..."
              disabled={isLoading}
              className="flex-1 bg-slate-700/50 text-white px-4 py-3 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed placeholder-slate-400 transition-colors"
              aria-label="Message input"
            />

            {isLoading ? (
              <button
                type="button"
                onClick={handleCancel}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-3 rounded-lg font-semibold transition-all flex items-center gap-2"
              >
                <span>Stop</span>
              </button>
            ) : (
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white px-6 py-3 rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 whitespace-nowrap"
                aria-label="Send message"
              >
                <span>Send</span>
                <span>→</span>
              </button>
            )}
          </div>

          {/* Help Text */}
          <div className="text-xs text-slate-400 space-y-1">
            <p>💡 Context: Press Shift+Enter for new line. Ask follow-up questions for more details.</p>
            <p>⚠️ <strong>Medical Disclaimer:</strong> This AI is for information only. Always consult healthcare professionals for medical advice.</p>
          </div>
        </form>
      </div>
    </div>
  );
}

ChatWidget.displayName = 'ChatWidget';

export default ChatWidget;
