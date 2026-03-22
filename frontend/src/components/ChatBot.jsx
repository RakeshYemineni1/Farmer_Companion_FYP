import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, ArrowLeft, Mic, MicOff, Volume2, VolumeX, Languages, ImagePlus, X } from 'lucide-react';
import TranslatedText from './TranslatedText';
import api from '../services/api';

const ChatBot = ({ onBack, user }) => {
  const loadMessages = () => {
    const saved = localStorage.getItem('krishisaathi_chat_messages');
    if (saved) {
      try {
        return JSON.parse(saved).map(msg => ({ ...msg, timestamp: new Date(msg.timestamp) }));
      } catch (e) {
        console.error('Error loading messages:', e);
      }
    }
    return [{
      id: 1,
      text: "Hello! I'm KrishiSaathi LLaMA Assistant, your AI farming companion. Ask me anything about crops, soil, fertilizers, diseases, or upload a plant image for analysis!",
      sender: 'bot',
      timestamp: new Date()
    }];
  };

  const sendMessageRef = useRef(null);
  const [messages, setMessages] = useState(loadMessages);
  const [inputMessage, setInputMessage] = useState('');
  const [attachedImage, setAttachedImage] = useState(null); // { file, previewUrl }
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('english');
  const [recognition, setRecognition] = useState(null);
  const [speechSynthesisObj, setSpeechSynthesisObj] = useState(null);
  const messagesEndRef = useRef(null);
  const imageInputRef = useRef(null);

  const languages = {
    'english':   { name: 'English',    code: 'en-IN' },
    'hindi':     { name: 'हिंदी',       code: 'hi-IN' },
    'bengali':   { name: 'বাংলা',       code: 'bn-IN' },
    'telugu':    { name: 'తెలుగు',      code: 'te-IN' },
    'marathi':   { name: 'मराठी',       code: 'mr-IN' },
    'tamil':     { name: 'தமிழ்',       code: 'ta-IN' },
    'gujarati':  { name: 'ગુજરાતી',     code: 'gu-IN' },
    'kannada':   { name: 'ಕನ್ನಡ',       code: 'kn-IN' },
    'malayalam': { name: 'മലയാളം',      code: 'ml-IN' },
    'punjabi':   { name: 'ਪੰਜਾਬੀ',      code: 'pa-IN' },
  };

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

  // Save messages to localStorage whenever messages change
  useEffect(() => {
    // Don't serialize blob URLs — they're revoked after use
    const toSave = messages.map(({ imagePreview, ...rest }) => rest);
    localStorage.setItem('krishisaathi_chat_messages', JSON.stringify(toSave));
    scrollToBottom();
  }, [messages]);

  const clearChat = () => {
    const defaultMessage = {
      id: 1,
      text: "Hello! I'm KrishiSaathi LLaMA Assistant, your AI farming companion. Ask me anything about crops, soil, fertilizers, diseases, or upload a plant image for analysis!",
      sender: 'bot',
      timestamp: new Date()
    };
    setMessages([defaultMessage]);
    localStorage.setItem('krishisaathi_chat_messages', JSON.stringify([defaultMessage]));
  };

  // ── Speech init ──────────────────────────────────────────────────────────
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      const inst = new SR();
      inst.continuous = false;
      inst.interimResults = false;
      inst.maxAlternatives = 1;
      inst.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        setInputMessage(transcript);
        sendMessageRef.current?.(transcript);
      };
      inst.onerror = () => setIsListening(false);
      inst.onend = () => setIsListening(false);
      setRecognition(inst);
    }
    if ('speechSynthesis' in window) {
      setSpeechSynthesisObj(window.speechSynthesis);
      const load = () => window.speechSynthesis.getVoices();
      window.speechSynthesis.getVoices().length > 0 ? load() : (window.speechSynthesis.onvoiceschanged = load);
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const startListening = () => {
    if (!recognition) return;
    recognition.lang = languages[selectedLanguage]?.code || 'en-IN';
    recognition.start();
    setIsListening(true);
  };

  const stopListening = () => { recognition?.stop(); setIsListening(false); };

  const speakText = (text, language = selectedLanguage) => {
    if (!speechSynthesisObj || !text) return;
    speechSynthesisObj.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const langCode = languages[language]?.code || 'en-IN';
    const baseLang = langCode.split('-')[0];
    const voiceMappings = {
      'hi': ['hi-IN', 'hi', 'en-IN', 'en-US'],
      'bn': ['bn-IN', 'bn', 'hi-IN', 'en-IN'],
      'te': ['te-IN', 'te', 'hi-IN', 'en-IN'],
      'ta': ['ta-IN', 'ta', 'hi-IN', 'en-IN'],
      'mr': ['mr-IN', 'mr', 'hi-IN', 'en-IN'],
      'gu': ['gu-IN', 'gu', 'hi-IN', 'en-IN'],
      'kn': ['kn-IN', 'kn', 'hi-IN', 'en-IN'],
      'ml': ['ml-IN', 'ml', 'hi-IN', 'en-IN'],
      'pa': ['pa-IN', 'pa', 'hi-IN', 'en-IN'],
      'en': ['en-IN', 'en-US', 'en-GB'],
    };
    const voices = speechSynthesisObj.getVoices();
    const priorities = voiceMappings[baseLang] || ['en-IN', 'en-US'];
    let selectedVoice = null;
    for (const p of priorities) {
      selectedVoice = voices.find(v => v.lang === p);
      if (selectedVoice) break;
    }
    if (!selectedVoice) {
      selectedVoice = voices.find(v => v.lang.startsWith(baseLang))
        || voices.find(v => v.lang.startsWith('en'))
        || voices[0];
    }
    if (selectedVoice) { utterance.voice = selectedVoice; utterance.lang = selectedVoice.lang; }
    else { utterance.lang = langCode; }
    utterance.rate = 0.8;
    utterance.pitch = 1;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    speechSynthesisObj.speak(utterance);
  };

  const stopSpeaking = () => { speechSynthesisObj?.cancel(); setIsSpeaking(false); };

  // ── Image attachment ─────────────────────────────────────────────────────
  const handleImageAttach = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setAttachedImage({ file, previewUrl: URL.createObjectURL(file) });
    e.target.value = '';
  };

  const removeImage = () => {
    if (attachedImage?.previewUrl) URL.revokeObjectURL(attachedImage.previewUrl);
    setAttachedImage(null);
  };

  // ── Send message ─────────────────────────────────────────────────────────
  const sendMessage = async (messageText = inputMessage) => {
    if (!messageText.trim() || isLoading) return;

    const imageToSend = attachedImage;
    setAttachedImage(null);

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date(),
      imagePreview: imageToSend?.previewUrl || null,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('message', messageText);
      formData.append('language', selectedLanguage);
      if (imageToSend?.file) formData.append('image', imageToSend.file);

      const { data } = await api.post('/chat', formData);
      const botResponseText = data.success
        ? data.response
        : "Sorry, I'm having trouble right now. Please try again.";

      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: botResponseText,
        sender: 'bot',
        timestamp: new Date(),
      }]);

      speakText(botResponseText, selectedLanguage);
    } catch {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: "Sorry, I couldn't connect to the server. Please check your connection and try again.",
        sender: 'bot',
        timestamp: new Date(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  useEffect(() => { sendMessageRef.current = sendMessage; });

  // ── Render ───────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-green-100 p-3 sm:p-4">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2 sm:gap-4">
            <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <ArrowLeft className="w-4 h-4 sm:w-5 sm:h-5" />
            </button>
            <div className="flex items-center gap-2 sm:gap-3">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 sm:w-6 sm:h-6 text-white" />
              </div>
              <div>
                <h1 className="text-lg sm:text-xl font-bold text-gray-900">
                  <TranslatedText text="KrishiSaathi LLaMA Assistant" language={user?.language} />
                </h1>

              </div>
            </div>
          </div>
          <button
            onClick={clearChat}
            className="text-xs sm:text-sm px-2 sm:px-3 py-1 sm:py-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors"
          >
            Clear Chat
          </button>
        </div>
      </div>

      {/* Chat Container */}
      <div className="max-w-4xl mx-auto p-2 sm:p-4 h-[calc(100vh-140px)] flex flex-col">

        {/* Messages */}
        <div className="flex-1 overflow-y-auto mb-3 sm:mb-4 space-y-3 sm:space-y-4 px-1">
          {messages.map((message) => (
            <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex items-start gap-2 sm:gap-3 max-w-[85%] sm:max-w-[80%] ${message.sender === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.sender === 'user' ? 'bg-blue-500' : 'bg-gradient-to-r from-green-500 to-blue-500'
                }`}>
                  {message.sender === 'user'
                    ? <User className="w-3 h-3 sm:w-4 sm:h-4 text-white" />
                    : <Bot className="w-3 h-3 sm:w-4 sm:h-4 text-white" />}
                </div>
                <div className={`rounded-2xl p-3 sm:p-4 ${
                  message.sender === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-gray-200 text-gray-800 shadow-sm'
                }`}>
                  {/* Show attached image preview in user bubble */}
                  {message.imagePreview && (
                    <img
                      src={message.imagePreview}
                      alt="attached"
                      className="rounded-lg mb-2 max-h-40 object-cover"
                    />
                  )}
                  <p className="whitespace-pre-wrap text-sm sm:text-base">{message.text}</p>
                  <p className={`text-xs mt-2 ${message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'}`}>
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-start gap-2 sm:gap-3">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center">
                  <Bot className="w-3 h-3 sm:w-4 sm:h-4 text-white" />
                </div>
                <div className="bg-white border border-gray-200 rounded-2xl p-3 sm:p-4 shadow-sm">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Language & Speech Controls */}
        <div className="bg-white rounded-xl sm:rounded-2xl border border-gray-200 p-2 sm:p-3 shadow-lg mb-2 sm:mb-3">
          <div className="flex flex-wrap items-center gap-2 sm:gap-3">
            <div className="flex items-center gap-2">
              <Languages className="text-green-600" size={16} />
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="px-2 py-1 sm:px-3 sm:py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 text-xs sm:text-sm"
              >
                {Object.entries(languages).map(([code, lang]) => (
                  <option key={code} value={code}>{lang.name}</option>
                ))}
              </select>
            </div>

            <button
              onClick={isListening ? stopListening : startListening}
              className={`flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-1 sm:py-2 rounded-lg font-medium text-xs sm:text-sm ${
                isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-green-500 text-white hover:bg-green-600'
              }`}
            >
              {isListening ? <MicOff size={14} /> : <Mic size={14} />}
              <span className="hidden sm:inline">{isListening ? 'Stop' : 'Speak'}</span>
            </button>

            <button
              onClick={isSpeaking ? stopSpeaking : undefined}
              disabled={!isSpeaking}
              className={`flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-1 sm:py-2 rounded-lg text-xs sm:text-sm ${
                isSpeaking ? 'bg-orange-500 text-white animate-pulse' : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {isSpeaking ? <VolumeX size={14} /> : <Volume2 size={14} />}
              <span className="hidden sm:inline">{isSpeaking ? 'Stop Audio' : 'Audio'}</span>
            </button>

            <button
              onClick={() => speakText(
                selectedLanguage === 'hindi' ? 'नमस्ते किसान' :
                selectedLanguage === 'telugu' ? 'హలో రైతు' :
                selectedLanguage === 'tamil' ? 'வணக்கம் விவசாயி' : 'Hello farmer',
                selectedLanguage
              )}
              className="px-2 sm:px-3 py-1 sm:py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 text-xs sm:text-sm"
            >
              Test
            </button>
          </div>
          <div className="text-xs text-gray-500 mt-2 hidden sm:block">
            Voice support varies by browser. You can also attach plant images for AI analysis.
          </div>
        </div>

        {/* Image preview strip */}
        {attachedImage && (
          <div className="bg-white rounded-xl border border-green-200 p-2 mb-2 flex items-center gap-3 shadow">
            <img src={attachedImage.previewUrl} alt="preview" className="h-14 w-14 object-cover rounded-lg" />
            <span className="text-sm text-gray-600 flex-1 truncate">{attachedImage.file.name}</span>
            <button onClick={removeImage} className="text-red-500 hover:text-red-700">
              <X size={18} />
            </button>
          </div>
        )}

        {/* Input bar */}
        <div className="bg-white rounded-xl sm:rounded-2xl border border-gray-200 p-3 sm:p-4 shadow-lg">
          <div className="flex gap-2 sm:gap-3 items-end">
            {/* Image attach button */}
            <button
              onClick={() => imageInputRef.current?.click()}
              className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors flex-shrink-0"
              title="Attach plant image for analysis"
            >
              <ImagePlus size={20} />
            </button>
            <input
              ref={imageInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleImageAttach}
            />

            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`Ask me about farming in ${languages[selectedLanguage]?.name}...`}
              className="flex-1 resize-none border-0 outline-none bg-transparent placeholder-gray-500 text-sm sm:text-base"
              rows="1"
              disabled={isLoading}
            />

            <button
              onClick={() => sendMessage()}
              disabled={(!inputMessage.trim() && !attachedImage) || isLoading}
              className="bg-gradient-to-r from-green-500 to-blue-500 text-white p-2 sm:p-3 rounded-xl hover:from-green-600 hover:to-blue-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
            >
              <Send className="w-4 h-4 sm:w-5 sm:h-5" />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ChatBot;
