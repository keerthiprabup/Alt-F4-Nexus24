import React, { useState } from 'react';
import axios from 'axios';
import './SaheliChat.css'; // Import CSS file

const SaheliChat = () => {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');

  const sendMessage = async () => {
    if (!inputText.trim()) return;
  
    // Save user query
    const userQuery = { sender: 'User', text: inputText };
    setMessages(prevMessages => [...prevMessages, userQuery]);
  
    // Clear input
    setInputText('');
  
    try {
      // Send user query to server
      const response = await axios.post('http://localhost:8000/api/generate', { query: inputText });
  
      // Save Saheli's response
      const saheliResponse = { sender: 'Saheli', text: response.data.response };
      setMessages(prevMessages => [...prevMessages, saheliResponse]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="saheli-chat-container">
      <div className="conversation-container">
        {/* Map through messages and display both user queries and Saheli's responses */} 
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender === 'User' ? 'user-message' : 'saheli-message'}>
            <b>{msg.sender}:</b> {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input type="text" value={inputText} onChange={(e) => setInputText(e.target.value)} placeholder="Type your message here" />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default SaheliChat;
