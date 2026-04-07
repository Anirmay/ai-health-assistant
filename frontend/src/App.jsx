import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { AnimatedBackground3D } from './components/AnimatedBackground3D';

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    document.body.classList.toggle('dark-theme', isDark);
    document.body.classList.toggle('light-theme', !isDark);
  }, [isDark]);

  const navItems = [
    { id: 'home', label: '🏥 Home', icon: '🏠' },
    { id: 'symptom', label: '🩺 Symptom Checker', icon: '🔍' },
    { id: 'medicine', label: '💊 Medicine Verify', icon: '✓' },
    { id: 'history', label: '📋 History', icon: '📊' },
    { id: 'chat', label: '💬 Ask AI', icon: '🤖' },
  ];

  const mainBackgroundClass = isDark
    ? 'min-h-screen bg-transparent text-white'
    : 'min-h-screen bg-transparent text-slate-900';

  return (
    <div>
      <AnimatedBackground3D isDark={isDark} />
      
      <div className={mainBackgroundClass}>
        {/* Navigation */}
        <nav className={`fixed top-0 w-full backdrop-blur-lg z-50 ${isDark ? 'bg-black/40 border-b border-cyan-500/20' : 'bg-white/80 border-b border-slate-200/70'}`}>
          <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <motion.div 
              className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              💫 AI Health
            </motion.div>
            
            <div className="hidden md:flex gap-2">
              {navItems.map((item) => (
                <motion.button
                  key={item.id}
                  onClick={() => setCurrentPage(item.id)}
                  className={`px-4 py-2 rounded-lg transition-all ${
                    currentPage === item.id
                      ? 'bg-gradient-to-r from-cyan-500 to-purple-500 text-white'
                      : 'text-gray-300 hover:text-white'
                  }`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {item.label}
                </motion.button>
              ))}
            </div>

            <button
              onClick={() => setIsDark(!isDark)}
              className={`p-2 rounded-full transition-all ${isDark ? 'bg-purple-500/20 hover:bg-purple-500/40 text-white' : 'bg-slate-200/70 hover:bg-slate-200/90 text-slate-900'}`}
            >
              {isDark ? '🌙' : '☀️'}
            </button>
          </div>
        </nav>

        {/* Main Content */}
        <div className="pt-20 px-6">
          {currentPage === 'home' && <HomePage />}
          {currentPage === 'symptom' && <SymptomChecker />}
          {currentPage === 'medicine' && <MedicineVerifier />}
          {currentPage === 'history' && <HealthHistory />}
          {currentPage === 'chat' && <AIChatBot />}
        </div>
      </div>
    </div>
  );
}

// Home Page
const HomePage = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
    className="max-w-7xl mx-auto"
  >
    <div className="grid md:grid-cols-2 gap-12 py-20">
      <div>
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
          Your AI Health Assistant
        </h1>
        <p className="text-xl text-gray-300 mb-8">
          Get instant disease predictions, verify medicine authenticity, and chat with AI-powered health advice—all in one place.
        </p>
        <button className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-lg font-bold hover:shadow-lg hover:shadow-purple-500/50 transition-all">
          Get Started 🚀
        </button>
      </div>
      <div className="grid grid-cols-2 gap-4">
        {[
          { icon: '🩺', title: 'Symptom Analysis', desc: 'AI-powered symptom checking' },
          { icon: '💊', title: 'Medicine Safety', desc: 'Detect counterfeit drugs' },
          { icon: '📊', title: 'Health Reports', desc: 'Track your health data' },
          { icon: '🤖', title: 'AI Chat', desc: '24/7 health Q&A' },
        ].map((item, idx) => (
          <motion.div
            key={idx}
            className="p-6 bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-cyan-500/20 rounded-lg backdrop-blur"
            whileHover={{ y: -10 }}
          >
            <div className="text-3xl mb-2">{item.icon}</div>
            <h3 className="font-bold mb-2">{item.title}</h3>
            <p className="text-sm text-gray-400">{item.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </motion.div>
);

// Symptom Checker
const SymptomChecker = () => {
  const [symptoms, setSymptoms] = useState('');
  const [result, setResult] = useState(null);

  const handleCheck = async () => {
    // Placeholder for API call
    setResult({
      disease: 'Likely Respiratory Infection',
      confidence: 0.92,
      risk: 'Medium',
      recommendations: ['See a doctor', 'Stay hydrated', 'Rest well'],
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="max-w-2xl mx-auto py-10"
    >
      <div className="bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-cyan-500/20 rounded-xl p-8 backdrop-blur">
        <h2 className="text-3xl font-bold mb-6">🩺 Symptom Checker</h2>
        <textarea
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          placeholder="Describe your symptoms..."
          className="w-full h-32 bg-black/50 border border-cyan-500/30 rounded-lg p-4 text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
        />
        <button
          onClick={handleCheck}
          className="mt-6 w-full px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-lg font-bold hover:shadow-lg hover:shadow-purple-500/50"
        >
          Analyze Symptoms
        </button>

        {result && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8 p-6 bg-black/50 border border-green-500/30 rounded-lg"
          >
            <h3 className="text-xl font-bold text-cyan-400 mb-4">{result.disease}</h3>
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div>
                <p className="text-gray-400 text-sm">Confidence</p>
                <p className="text-2xl font-bold text-green-400">{(result.confidence * 100).toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Risk Level</p>
                <p className="text-2xl font-bold text-yellow-400">{result.risk}</p>
              </div>
            </div>
            <p className="text-sm text-gray-400">⚠️ Disclaimer: Not a substitute for professional medical advice</p>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

// Medicine Verifier
const MedicineVerifier = () => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="max-w-2xl mx-auto py-10"
  >
    <div className="bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-cyan-500/20 rounded-xl p-8 backdrop-blur">
      <h2 className="text-3xl font-bold mb-6">💊 Medicine Authenticator</h2>
      <div className="border-2 border-dashed border-cyan-500/30 rounded-lg p-12 text-center cursor-pointer hover:border-cyan-500/50 transition">
        <p className="text-xl mb-2">📸 Upload Medicine Image</p>
        <p className="text-gray-400">or drag and drop here</p>
      </div>
    </div>
  </motion.div>
);

// Health History
const HealthHistory = () => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="max-w-4xl mx-auto py-10"
  >
    <h2 className="text-3xl font-bold mb-6">📋 Health History</h2>
    <div className="space-y-4">
      {[1, 2, 3].map((item) => (
        <motion.div
          key={item}
          className="bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-cyan-500/20 rounded-lg p-6"
          whileHover={{ x: 10 }}
        >
          <p className="text-gray-400">Check #{item}</p>
          <p className="font-bold">Respiratory Infection</p>
          <p className="text-sm text-gray-500">2 days ago</p>
        </motion.div>
      ))}
    </div>
  </motion.div>
);

// AI Chat
const AIChatBot = () => (
  <motion.div
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    className="max-w-2xl mx-auto py-10 h-96"
  >
    <div className="h-full bg-gradient-to-br from-cyan-500/10 to-purple-500/10 border border-cyan-500/20 rounded-xl p-8 backdrop-blur flex flex-col">
      <h2 className="text-3xl font-bold mb-6">💬 Chat with Health AI</h2>
      <div className="flex-1 overflow-y-auto mb-4 bg-black/30 rounded p-4">
        <p className="text-gray-400">Chat history will appear here...</p>
      </div>
      <input
        type="text"
        placeholder="Ask a health question..."
        className="w-full bg-black/50 border border-cyan-500/30 rounded-lg p-3 text-white focus:outline-none focus:border-cyan-500"
      />
    </div>
  </motion.div>
);
