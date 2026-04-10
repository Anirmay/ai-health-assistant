/**
 * Custom Hook for Health Chat
 * Manages chat state, messages, and API communication
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { sendChatMessage, formatErrorMessage } from '../services/apiService';

/**
 * Message object structure
 * @typedef {object} Message
 * @property {string} id - Unique message ID
 * @property {'user' | 'ai' | 'error' | 'system'} type - Message type
 * @property {string} text - Message content
 * @property {Date} timestamp - When the message was sent/received
 * @property {number} responseTime - Response time in seconds (for AI messages)
 */

/**
 * Hook for managing health chat conversations
 * @param {object} initialMessages - Optional initial messages
 * @returns {object} - Chat state and methods
 */
export function useHealthChat(initialMessages = []) {
  // State
  const [messages, setMessages] = useState(initialMessages);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sentMessageCount, setSentMessageCount] = useState(0);

  // Refs
  const messageIdRef = useRef(initialMessages.length);
  const abortControllerRef = useRef(null);
  const lastMessageTextRef = useRef('');

  /**
   * Generate unique message ID
   */
  const generateMessageId = useCallback(() => {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }, []);

  /**
   * Add a message to the chat
   */
  const addMessage = useCallback((message) => {
    const messageWithId = {
      id: generateMessageId(),
      timestamp: new Date(),
      ...message,
    };

    setMessages((prev) => [...prev, messageWithId]);
    messageIdRef.current += 1;
    return messageWithId;
  }, [generateMessageId]);

  /**
   * Remove a message by ID
   */
  const removeMessage = useCallback((messageId) => {
    setMessages((prev) => prev.filter((msg) => msg.id !== messageId));
  }, []);

  /**
   * Clear all messages
   */
  const clearMessages = useCallback(() => {
    setMessages([]);
    messageIdRef.current = 0;
    setSentMessageCount(0);
  }, []);

  /**
   * Send a message to the AI
   * Handles loading state, error handling, and duplicate prevention
   */
  const sendMessage = useCallback(
    async (message, context = null) => {
      // Validation
      if (!message || !message.trim()) {
        setError('Please enter a message');
        return null;
      }

      // Prevent duplicate messages
      if (message.trim() === lastMessageTextRef.current) {
        setError('Please write a different message');
        return null;
      }

      // Clear previous errors
      setError(null);
      setIsLoading(true);

      // Track message for duplicate prevention
      lastMessageTextRef.current = message.trim();

      try {
        // Add user message
        const userMessage = addMessage({
          type: 'user',
          text: message.trim(),
        });

        // Create abort controller for this request
        abortControllerRef.current = new AbortController();

        try {
          // Send to API
          const response = await sendChatMessage(message.trim(), context);

          // Verify we didn't abort during the request
          if (abortControllerRef.current.signal.aborted) {
            console.log('Request was cancelled');
            return null;
          }

          // Add AI response
          const aiMessage = addMessage({
            type: 'ai',
            text: response.reply,
            responseTime: response.response_time,
          });

          setSentMessageCount((prev) => prev + 1);
          return aiMessage;
        } catch (apiError) {
          // Remove user message if API call failed
          removeMessage(userMessage.id);

          // Format and throw error
          const errorText = formatErrorMessage(apiError);
          setError(errorText);

          // Add error message
          const errorMessage = addMessage({
            type: 'error',
            text: errorText,
          });

          return null;
        }
      } finally {
        setIsLoading(false);
      }
    },
    [addMessage, removeMessage]
  );

  /**
   * Cancel the current request
   */
  const cancelRequest = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsLoading(false);
      setError('Request cancelled');
    }
  }, []);

  /**
   * Clear error message
   */
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    // State
    messages,
    isLoading,
    error,
    sentMessageCount,

    // Methods
    addMessage,
    removeMessage,
    sendMessage,
    cancelRequest,
    clearMessages,
    clearError,
  };
}
