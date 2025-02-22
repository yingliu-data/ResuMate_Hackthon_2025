
import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, X, Mic, MicOff, Send } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { toast } from 'sonner';

const ChatBox = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<{ text: string; sender: 'user' | 'bot'; type: 'text' | 'audio' }[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const handleTextSend = async () => {
    if (!message.trim()) return;

    setIsLoading(true);
    const userMessage = { text: message, sender: 'user' as const, type: 'text' as const };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { text: data.message, sender: 'bot', type: 'text' }]);
      setMessage('');
    } catch (error) {
      console.error('Error:', error);
      toast.error('Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      const chunks: BlobPart[] = [];
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' });

        // Create form data to send the audio
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');

        try {
          const response = await fetch('http://localhost:8000/chat/audio', {
            method: 'POST',
            body: formData,
          });

          if (!response.ok) {
            throw new Error('Failed to send audio');
          }

          const data = await response.json();
          setMessages(prev => [...prev, { text: data.message, sender: 'bot', type: 'text' }]);
        } catch (error) {
          console.error('Error sending audio:', error);
          toast.error('Failed to send audio message');
        }
      };

      mediaRecorder.start();
      setIsRecording(true);

      setMessages(prev => [...prev, {
        text: '🎤 Recording started...',
        sender: 'user',
        type: 'audio'
      }]);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      toast.error('Failed to access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setIsRecording(false);
    setMessages(prev => [...prev, {
      text: '🎤 Recording stopped',
      sender: 'user',
      type: 'audio'
    }]);
  };

  return (
    <div className="fixed bottom-4 left-4 z-50">
      {!isOpen ? (
        <Button
          onClick={() => setIsOpen(true)}
          className="rounded-full w-12 h-12 flex items-center justify-center"
        >
          <MessageSquare className="w-6 h-6" />
        </Button>
      ) : (
        <Card className="w-80 h-[400px] flex flex-col absolute bottom-0 left-0">
          <div className="p-4 border-b flex justify-between items-center">
            <h3 className="font-semibold">Chat Assistant</h3>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsOpen(false)}
              className="h-8 w-8"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[80%] p-2 rounded-lg ${
                    msg.sender === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-muted'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 border-t">
            <div className="flex gap-2">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    handleTextSend();
                  }
                }}
              />
              <Button
                onClick={handleTextSend}
                disabled={isLoading || isRecording}
                className="min-w-[40px]"
              >
                <Send className="h-4 w-4" />
              </Button>
              <Button
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isLoading}
                variant={isRecording ? 'destructive' : 'default'}
                className="min-w-[40px]"
              >
                {isRecording ? (
                  <MicOff className="h-4 w-4" />
                ) : (
                  <Mic className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};

export default ChatBox;
