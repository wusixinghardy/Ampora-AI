import React, { useRef, useEffect, useState } from 'react';
import { FaRegStopCircle } from "react-icons/fa";
import WaveIcon from './WaveIcon';
import { mockChatService } from '../services/mockChat';
import '../styles/ChatInterface.css';

const ChatInterface = ({ setIsProcessing, setVideoUrl }) => {
  const [chatInput, setChatInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [typingMessage, setTypingMessage] = useState('');
  const [fullResponse, setFullResponse] = useState('');
  const [typeIndex, setTypeIndex] = useState(0);
  
  const chatHistoryRef = useRef(null);
  const textareaRef = useRef(null);
  const typingTimerRef = useRef(null);
  const isCanceledRef = useRef(false);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory, typingMessage]);

  // Auto-resize textarea with proper scrolling
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const newHeight = Math.min(textareaRef.current.scrollHeight, 120); // Max 120px
      textareaRef.current.style.height = newHeight + 'px';
      
      // Enable scrolling if content exceeds max height
      if (textareaRef.current.scrollHeight > 120) {
        textareaRef.current.style.overflowY = 'auto';
      } else {
        textareaRef.current.style.overflowY = 'hidden';
      }
    }
  }, [chatInput]);

  // Handle typing effect
  useEffect(() => {
    if (isTyping && fullResponse) {
      if (typingTimerRef.current) {
        clearTimeout(typingTimerRef.current);
      }
      
      if (typeIndex < fullResponse.length && !isCanceledRef.current) {
        const randomDelay = Math.floor(Math.random() * 40) + 20;
        
        typingTimerRef.current = setTimeout(() => {
          setTypingMessage(prev => prev + fullResponse.charAt(typeIndex));
          setTypeIndex(prevIndex => prevIndex + 1);
        }, randomDelay);
        
        return () => {
          if (typingTimerRef.current) {
            clearTimeout(typingTimerRef.current);
          }
        };
      } else {
        setIsTyping(false);
        const finalText = isCanceledRef.current ? typingMessage : fullResponse;
        
        if (finalText.trim().length > 0) {
          setChatHistory(prevHistory => [
            ...prevHistory, 
            {
              sender: 'bot',
              text: finalText
            }
          ]);
        }
        
        setFullResponse('');
        setTypingMessage('');
        setTypeIndex(0);
        isCanceledRef.current = false;
      }
    }
  }, [isTyping, fullResponse, typeIndex, typingMessage]);

  const handleCancelTyping = () => {
    isCanceledRef.current = true;
    
    if (typingTimerRef.current) {
      clearTimeout(typingTimerRef.current);
    }
    
    setIsTyping(false);
    setIsProcessing(false);
    
    if (typingMessage.trim().length > 0) {
      setChatHistory(prevHistory => [
        ...prevHistory, 
        {
          sender: 'bot',
          text: typingMessage + " (Message interrupted)"
        }
      ]);
    }
    
    setFullResponse('');
    setTypingMessage('');
    setTypeIndex(0);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSend = async () => {
    if (!chatInput.trim() || isTyping) return;
    
    const currentInput = chatInput.trim();
    setChatInput('');
    
    const newUserMessage = { 
      sender: 'user', 
      text: currentInput
    };
    
    setChatHistory(prevHistory => [...prevHistory, newUserMessage]);
    
    setIsTyping(true);
    setTypingMessage('');
    setTypeIndex(0);
    isCanceledRef.current = false;
    setIsProcessing(true);
    
    try {
      const token = localStorage.getItem('authToken');
      
      // Use mock chat service (which handles mock vs real backend)
      const result = await mockChatService.sendMessage(currentInput, token);
      
      if (isCanceledRef.current) {
        setIsProcessing(false);
        return;
      }
      
      // Check if video was generated
      if (result.video_url) {
        setVideoUrl(result.video_url);
      }
      
      // Stop processing indicator once response is received
      setIsProcessing(false);
      
      setFullResponse(result.response || 'Sorry, I couldn\'t process your request.');
    } catch (err) {
      console.error("Error:", err);
      
      if (!isCanceledRef.current) {
        const errorMessage = err.message.includes('timed out') 
          ? 'Request timed out. Please try again.' 
          : err.message || 'Failed to contact the server. Please try again.';
        
        setFullResponse(errorMessage);
        setIsProcessing(false);
      }
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header-container">
        <h2 className="chat-header">Chat with Ampora AI</h2>
      </div>
      
      <div className="chat-history" ref={chatHistoryRef}>
        {chatHistory.length === 0 && !isTyping ? (
          <div className="empty-chat">
            <p>Start chatting to generate your video content</p>
          </div>
        ) : (
          <div className="conversation-container">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`message-group ${msg.sender}`}>
                <div className="message-role">
                  {msg.sender === 'user' ? 'You' : 'Ampora AI'}
                </div>
                <div className="message-content">
                  <p>{msg.text}</p>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="message-group bot">
                <div className="message-role">Ampora AI</div>
                <div className="message-content">
                  {typingMessage ? (
                    <p>{typingMessage}<span className="cursor-blink">|</span></p>
                  ) : (
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      
      <div className="chat-controls">
        <div className="chat-input-container">
          <textarea
            ref={textareaRef}
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Send a message..."
            className="chat-textarea"
            rows="1"
            disabled={isTyping}
          />
        </div>

        <div className="chat-actions">
          <div className="chat-actions-right">
            {isTyping ? (
              <button
                className="action-button cancel-button"
                onClick={handleCancelTyping}
                title="Cancel response"
              >
                <FaRegStopCircle className="button-icon" />
              </button>
            ) : (
              <button
                className="action-button send-button"
                onClick={handleSend}
                title="Send Message"
                disabled={chatInput.trim() === ''}
              >
                <WaveIcon size={20} color="#00ffcc" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
