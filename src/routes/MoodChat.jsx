import React, { useState, useEffect, useRef } from 'react';
import ChatInterface from "../components/ChatInterface";

const MoodChat = () => {
    const [messages, setMessages] = useState([
        { 
            role: 'assistant', 
            content: "How are you feeling today? 😊" 
        }
    ]);
    const [message, setMessage] = useState('');
    const [sessionId, setSessionId] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const apiKey = import.meta.env.VITE_ONDEMAND_API_KEY;
    const externalUserId = '1';

    // Function to create a chat session
    const createChatSession = async () => {
        const response = await fetch('https://api.on-demand.io/chat/v1/sessions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'apikey': apiKey
            },
            body: JSON.stringify({
                pluginIds: [],
                externalUserId: externalUserId
            })
        });
        const data = await response.json();
        return data.data.id;
    };

    // Function to submit a query
    const submitQuery = async (sessionId, query) => {
        const response = await fetch(`https://api.on-demand.io/chat/v1/sessions/${sessionId}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'apikey': apiKey
            },
            body: JSON.stringify({
                endpointId: 'predefined-openai-gpt4o',
                query: query,
                pluginIds: ['plugin-1712327325', 'plugin-1713962163', 'plugin-1731189984'],
                responseMode: 'sync'
            })
        });
        const data = await response.json();
        return data;
    };

    // Initialize chat session
    useEffect(() => {
        const initSession = async () => {
            try {
                const id = await createChatSession();
                setSessionId(id);
            } catch (error) {
                console.error('Error creating session:', error);
            }
        };
        initSession();
    }, []);

    const handleSendMessage = async () => {
        if (!message.trim() || !sessionId || isLoading) return;

        setIsLoading(true);
        
        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: message }]);
        
        try {
            const response = await submitQuery(sessionId, message);
            // Add AI response
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: response.data.answer 
            }]);
        } catch (error) {
            console.error('Error submitting query:', error);
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: 'Sorry, there was an error processing your message.' 
            }]);
        }
        
        setMessage('');
        setIsLoading(false);
    };

    return (
        <ChatInterface 
            messages={messages} 
            message={message}
            setMessage={setMessage}
            sendMessage={handleSendMessage}
            isLoading={isLoading}
            disabled={!sessionId}
        />
    );
};

export default MoodChat;