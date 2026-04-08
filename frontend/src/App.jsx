import React, { useState, useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import AnimatedGradientBackground from './components/AnimatedGradientBackground';

gsap.registerPlugin(ScrollTrigger);

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [scrollY, setScrollY] = useState(0);
  const containerRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Sync URL with page state
  useEffect(() => {
    const path = window.location.pathname.slice(1) || 'home';
    const page = ['home', 'symptom', 'medicine', 'chat', 'history'].includes(path) ? path : 'home';
    setCurrentPage(page);
  }, []);

  // Update URL when page changes
  useEffect(() => {
    if (currentPage !== 'home') {
      window.history.pushState({}, '', `/${currentPage}`);
    } else {
      window.history.pushState({}, '', '/');
    }
  }, [currentPage]);

  // Scroll to top when page changes
  useEffect(() => {
    window.scrollTo(0, 0);
    ScrollTrigger.refresh();
  }, [currentPage]);

  return (
    <div ref={containerRef} className="min-h-screen bg-slate-950 text-white overflow-hidden">
      <AnimatedGradientBackground />
      
      {/* Animated background orbs */}
      <div className="fixed inset-0 -z-5 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/3 right-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
      </div>

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3 group cursor-pointer">
            <div className="relative w-12 h-12 rounded-full bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/50 group-hover:shadow-cyan-500/80 transition-all">
              <span className="text-xl font-bold">🔬</span>
            </div>
            <div>
              <h1 className="text-2xl font-black gradient-text">HealthAI</h1>
              <p className="text-xs text-gray-400">AI-Powered Health</p>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-8">
            {['Home', 'Symptom', 'Medicine', 'Chat', 'History'].map((item) => (
              <button
                key={item}
                onClick={() => setCurrentPage(item.toLowerCase())}
                className={`relative px-4 py-2 transition-all ${
                  currentPage === item.toLowerCase()
                    ? 'text-cyan-400 font-semibold'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                {item}
                {currentPage === item.toLowerCase() && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-400 to-purple-600"></div>
                )}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <button className="p-2.5 glass rounded-full hover:bg-white/10 transition-all">
              ⚙️
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative z-10 pt-24">
        {currentPage === 'home' && <HomePage />}
        {currentPage === 'symptom' && <SymptomPage />}
        {currentPage === 'medicine' && <MedicinePage />}
        {currentPage === 'chat' && <ChatPage />}
        {currentPage === 'history' && <HistoryPage />}
      </main>
    </div>
  );
}

function HomePage() {
  const heroRef = useRef(null);
  const cardsRef = useRef([]);
  const statsRef = useRef([]);
  const titleRef = useRef(null);
  const mouseRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    // Heavy staggered entrance animation for hero section
    const children = Array.from(heroRef.current?.children || []);
    gsap.fromTo(
      children,
      { opacity: 0, y: 100, rotateX: -90 },
      { 
        opacity: 1, 
        y: 0, 
        rotateX: 0,
        stagger: 0.25, 
        duration: 1.2, 
        ease: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
        perspective: 1200
      }
    );

    // Feature cards entrance with bounce
    gsap.fromTo(
      cardsRef.current,
      { opacity: 0, y: 80, scale: 0.5 },
      { 
        opacity: 1, 
        y: 0, 
        scale: 1,
        stagger: 0.12, 
        duration: 1, 
        delay: 0.8,
        ease: 'back.out(1.7)'
      }
    );

    // Floating animation for cards
    cardsRef.current.forEach((card, idx) => {
      if (card) {
        gsap.to(card, {
          y: idx % 2 === 0 ? -15 : 15,
          duration: 3 + idx * 0.3,
          ease: 'sine.inOut',
          repeat: -1,
          yoyo: true
        });
      }
    });

    // Animated stats counter with scroll trigger
    statsRef.current.forEach((stat, idx) => {
      if (stat) {
        const valueEl = stat.querySelector('.stat-value');
        ScrollTrigger.create({
          trigger: stat,
          onEnter: () => {
            gsap.fromTo(
              valueEl,
              { textContent: '0' },
              {
                textContent: valueEl.getAttribute('data-value'),
                duration: 2,
                ease: 'power2.out',
                snap: { textContent: 1 },
                stagger: 0.05
              }
            );
          },
          once: true
        });
      }
    });

    // Title text animation
    if (titleRef.current) {
      const letters = titleRef.current.querySelectorAll('span');
      gsap.fromTo(
        letters,
        { opacity: 0, y: 50 },
        {
          opacity: 1,
          y: 0,
          stagger: 0.05,
          duration: 0.8,
          ease: 'power3.out'
        }
      );
    }

    // Mouse tracking effect
    const handleMouseMove = (e) => {
      mouseRef.current = { x: e.clientX, y: e.clientY };
      
      cardsRef.current.forEach((card) => {
        if (card) {
          const rect = card.getBoundingClientRect();
          const cardCenterX = rect.left + rect.width / 2;
          const cardCenterY = rect.top + rect.height / 2;
          
          const distX = mouseRef.current.x - cardCenterX;
          const distY = mouseRef.current.y - cardCenterY;
          const distance = Math.sqrt(distX * distX + distY * distY);
          
          if (distance < 400) {
            gsap.to(card, {
              x: distX * 0.08,
              y: distY * 0.08,
              duration: 0.5
            });
          }
        }
      });
    };

    window.addEventListener('mousemove', handleMouseMove);
    
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <div className="min-h-screen">
      {/* Animated background shapes */}
      <div className="fixed inset-0 overflow-hidden -z-20 pointer-events-none">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-purple-600 to-blue-600 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-1/3 -left-40 w-96 h-96 bg-gradient-to-br from-cyan-600 to-purple-600 rounded-full mix-blend-screen filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
      </div>

      {/* Hero */}
      <div ref={heroRef} className="max-w-7xl mx-auto px-6 py-20 space-y-8">
        <div className="space-y-6 max-w-3xl">
          <h1 ref={titleRef} className="text-7xl md:text-8xl font-black leading-tight">
            <span className="gradient-text inline-block mr-3">Your</span>
            <span className="gradient-text inline-block mr-3">AI</span>
            <span className="gradient-text inline-block">Health</span>
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 inline-block">Companion</span>
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl leading-relaxed animate-fade-in-delayed">
            Advanced AI-powered health analysis, medicine verification, and 24/7 health support. All in one intelligent platform.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <button className="magnetic-btn relative group px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-white shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/80 transition-all overflow-hidden">
              <span className="relative z-10 flex items-center gap-2">
                Start Now
                <span className="group-hover:translate-x-2 transition-transform">→</span>
              </span>
              <div className="ripple-effect absolute inset-0 bg-white opacity-0 group-hover:opacity-10 rounded-xl"></div>
            </button>
            <button className="magnetic-btn px-8 py-4 glass rounded-xl font-bold hover:bg-white/10 transition-all relative overflow-hidden group">
              <span className="relative z-10">Learn More</span>
              <div className="ripple-effect absolute inset-0 bg-cyan-400 opacity-0 group-hover:opacity-20 rounded-xl"></div>
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 pt-12">
          {[
            { icon: '🩺', title: 'Smart Diagnosis', desc: 'AI-powered symptom analysis', color: 'from-cyan-500 to-blue-600' },
            { icon: '💊', title: 'Medicine Check', desc: 'Verify authenticity instantly', color: 'from-purple-500 to-pink-600' },
            { icon: '🤖', title: 'AI Assistant', desc: '24/7 health guidance', color: 'from-blue-500 to-cyan-600' },
          ].map((feature, idx) => (
            <div
              key={idx}
              ref={(el) => (cardsRef.current[idx] = el)}
              className={`glass p-8 rounded-2xl hover:bg-white/10 transition-all border-l-4 border-transparent hover:border-gradient-to-r group cursor-pointer feature-card`}
            >
              <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-10 rounded-2xl pointer-events-none transition-opacity" 
                style={{backgroundImage: `linear-gradient(to right, var(--tw-gradient-stops))`}}></div>
              <div className="relative z-10 space-y-4">
                <div className="text-5xl group-hover:scale-125 group-hover:rotate-12 transition-transform duration-300 inline-block">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats with animation */}
      <div className="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-4 gap-8 relative z-20">
        {[
          { label: 'Active Users', value: '100', suffix: 'K+' },
          { label: 'Accuracy Rate', value: '98', suffix: '%' },
          { label: 'Response Time', value: '500', suffix: 'ms' },
          { label: 'Countries', value: '150', suffix: '+' },
        ].map((stat, idx) => (
          <div 
            key={idx} 
            ref={(el) => (statsRef.current[idx] = el)}
            className="text-center glass p-8 rounded-xl stat-card group cursor-pointer hover:bg-white/10 transition-all"
          >
            <div className="text-4xl font-black gradient-text mb-2 stat-value" data-value={stat.value}>
              0
            </div>
            <span className="text-cyan-400">{stat.suffix}</span>
            <p className="text-gray-400 mt-3">{stat.label}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function SymptomPage() {
  const [symptoms, setSymptoms] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const titleRef = useRef(null);
  const formRef = useRef(null);
  const resultRef = useRef(null);

  // Common symptoms for quick selection
  const commonSymptoms = [
    'fever', 'cough', 'headache', 'fatigue', 'sore throat',
    'body ache', 'nausea', 'diarrhea', 'shortness of breath', 'chest pain'
  ];

  useEffect(() => {
    gsap.fromTo(titleRef.current, 
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }
    );

    gsap.fromTo(formRef.current,
      { opacity: 0, scale: 0.9 },
      { opacity: 1, scale: 1, duration: 0.8, delay: 0.2, ease: 'back.out(1.5)' }
    );
  }, []);

  const addSymptom = (symptom) => {
    if (!symptoms.toLowerCase().includes(symptom.toLowerCase())) {
      setSymptoms(symptoms ? symptoms + ', ' + symptom : symptom);
    }
  };

  const analyzeSymptoms = async () => {
    if (!symptoms.trim()) {
      setError('Please enter at least one symptom');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:5000/api/symptoms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms: symptoms })
      });

      if (!response.ok) {
        throw new Error('Failed to analyze symptoms');
      }

      const data = await response.json();
      setResult(data);

      // Animate result
      setTimeout(() => {
        gsap.fromTo(resultRef.current,
          { opacity: 0, y: 30, scale: 0.9 },
          { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'back.out(1.5)' }
        );
      }, 0);

    } catch (err) {
      setError(err.message || 'Failed to analyze symptoms');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      analyzeSymptoms();
    }
  };

  return (
    <div className="min-h-screen max-w-6xl mx-auto px-6 py-20">
      <div className="space-y-8">
        {/* Title */}
        <div ref={titleRef} className="space-y-3">
          <h2 className="text-5xl font-black gradient-text">🩺 Symptom Analyzer</h2>
          <p className="text-gray-400 text-lg">AI-powered disease prediction from your symptoms</p>
        </div>

        {!result ? (
          <>
            {/* Input Form */}
            <div ref={formRef} className="glass p-12 rounded-2xl space-y-6 border border-white/10">
              {/* Textarea */}
              <div>
                <label className="block text-sm text-gray-400 mb-3">Describe your symptoms:</label>
                <textarea
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="e.g., I have fever, cough, headache, and fatigue..."
                  className="w-full h-32 glass rounded-xl p-4 text-white placeholder-gray-500 resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
                />
              </div>

              {/* Quick symptom selection */}
              <div>
                <label className="block text-sm text-gray-400 mb-3">Or select common symptoms:</label>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                  {commonSymptoms.map((symptom) => (
                    <button
                      key={symptom}
                      onClick={() => addSymptom(symptom)}
                      className="px-3 py-2 glass rounded-lg text-sm font-medium hover:bg-cyan-500/20 hover:border-cyan-500/50 border border-white/10 transition-all"
                    >
                      + {symptom}
                    </button>
                  ))}
                </div>
              </div>

              {error && (
                <div className="glass p-4 rounded-xl border-l-4 border-red-500 flex items-center gap-3">
                  <span className="text-2xl">⚠️</span>
                  <p className="text-red-400">{error}</p>
                </div>
              )}

              {/* Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={analyzeSymptoms}
                  disabled={loading}
                  className="flex-1 px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-white shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/80 transition-all hover:scale-105 active:scale-95 disabled:opacity-50"
                >
                  {loading ? '🔄 Analyzing...' : '🔍 Analyze Symptoms'}
                </button>
                <button
                  onClick={() => {
                    setSymptoms('');
                    setError(null);
                  }}
                  className="px-8 py-4 glass rounded-xl font-bold hover:bg-white/10 transition-all"
                >
                  Clear
                </button>
              </div>
            </div>
          </>
        ) : (
          <>
            {/* Results Display */}
            <div ref={resultRef} className="space-y-6">
              {/* EMERGENCY ALERT - HIGHEST PRIORITY - DISPLAY AT TOP */}
              {result && result.emergency_alert && result.emergency_alert.alert && (
                <div className="animate-pulse">
                  <div className="glass p-8 rounded-2xl border-l-8 border-red-500 bg-gradient-to-r from-red-500/20 to-orange-500/20 shadow-2xl shadow-red-500/50">
                    <div className="flex items-start gap-4">
                      <div className="text-5xl animate-bounce">🚨</div>
                      <div className="flex-1">
                        <p className="text-2xl font-black text-red-400 mb-3">
                          {result.emergency_alert.severity === 'CRITICAL' ? 'CRITICAL EMERGENCY' : 'URGENT ALERT'}
                        </p>
                        <p className="text-lg font-bold text-red-300 mb-4">{result.emergency_alert.message}</p>
                        <div className="bg-red-500/30 p-3 rounded-lg mb-3">
                          <p className="text-red-200 font-semibold">⚡ Immediate Action Required:</p>
                          <p className="text-red-300 mt-1 text-lg">{result.emergency_alert.action}</p>
                        </div>
                        {result.emergency_alert.advice && (
                          <p className="text-red-300 text-sm italic">{result.emergency_alert.advice}</p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Data Quality Warning - DISPLAY IF LIMITED SYMPTOMS */}
              {result && result.data_quality_warning && !result.emergency_alert?.alert && (
                <div className="glass p-6 rounded-lg border-l-4 border-yellow-500 bg-yellow-500/10">
                  <p className="text-yellow-400 font-semibold flex items-center gap-2">
                    <span>⚠️</span>
                    {result.data_quality_warning}
                  </p>
                  <p className="text-yellow-300 text-sm mt-2">
                    💡 Tip: Add more symptoms for more accurate predictions
                  </p>
                </div>
              )}

              {/* Main Result Card */}
              {result.primary_disease && (
                <div className="glass p-8 rounded-2xl border-l-8 border-green-500">
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <p className="text-gray-400 text-sm mb-2">PRIMARY PREDICTION</p>
                      <h3 className="text-4xl font-black text-green-400">
                        {result.primary_disease.disease}
                      </h3>
                      <p className="text-gray-400 mt-2">{result.primary_disease.advice}</p>
                    </div>
                    <div className="text-6xl">🩺</div>
                  </div>

                  {/* Confidence and Risk */}
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="glass p-4 rounded-lg border border-cyan-500/30">
                      <p className="text-gray-400 text-sm">Confidence</p>
                      <p className="text-3xl font-bold text-cyan-400">
                        {result.primary_disease.confidence}%
                      </p>
                    </div>
                    <div className="glass p-4 rounded-lg border border-yellow-500/30">
                      <p className="text-gray-400 text-sm">Risk Level</p>
                      <p className="text-3xl font-bold text-yellow-400">
                        {result.risk_level}
                      </p>
                    </div>
                    <div className="glass p-4 rounded-lg border border-purple-500/30">
                      <p className="text-gray-400 text-sm">Symptoms Matched</p>
                      <p className="text-3xl font-bold text-purple-400">
                        {result.symptom_count}
                      </p>
                    </div>
                  </div>

                  {/* When to See Doctor */}
                  {result.when_to_see_doctor && (
                    <div className="mt-6 glass p-6 rounded-lg border-l-4 border-blue-500 bg-blue-500/10">
                      <p className="text-sm text-gray-400 mb-1">WHEN TO SEE DOCTOR</p>
                      <p className="text-blue-300 font-semibold">{result.when_to_see_doctor}</p>
                    </div>
                  )}

                  {/* Explainability: Why This Result */}
                  {result.primary_disease && result.primary_disease.reasoning && (
                    <div className="mt-6 glass p-6 rounded-lg border border-cyan-500/30 bg-cyan-500/5">
                      <h4 className="font-bold text-cyan-400 mb-4">🔍 Why This Prediction?</h4>
                      <div className="space-y-3">
                        <div>
                          <p className="text-sm text-gray-400">Matched Symptoms:</p>
                          <div className="flex flex-wrap gap-2 mt-2">
                            {result.primary_disease.reasoning.matched_symptoms?.map((sym, i) => (
                              <span key={i} className="px-3 py-1 glass rounded-full text-xs text-cyan-300">
                                ✓ {sym}
                              </span>
                            ))}
                          </div>
                        </div>
                        <div>
                          <p className="text-sm text-gray-400">AI Analysis:</p>
                          <p className="text-gray-300 mt-1">{result.primary_disease.reasoning.explanation}</p>
                        </div>
                        <div className="grid grid-cols-2 gap-4 mt-4">
                          <div className="glass p-3 rounded">
                            <p className="text-xs text-gray-400">Confidence Level</p>
                            <p className="text-sm font-bold text-green-400">{result.primary_disease.reasoning.confidence_level}</p>
                          </div>
                          <div className="glass p-3 rounded">
                            <p className="text-xs text-gray-400">Symptoms Matched</p>
                            <p className="text-sm font-bold text-blue-400">{result.primary_disease.reasoning.match_count} of {result.symptom_count}</p>
                          </div>
                        </div>
                        {/* Data Quality Note */}
                        {result.primary_disease.reasoning.data_quality_note && (
                          <div className="mt-4 glass p-3 rounded border border-yellow-500/30 bg-yellow-500/5">
                            <p className="text-xs text-yellow-400">📊 {result.primary_disease.reasoning.data_quality_note}</p>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Alternative Diagnoses */}
              {result.results && result.results.length > 1 && (
                <div className="glass p-8 rounded-2xl border border-white/10">
                  <h4 className="text-xl font-bold gradient-text mb-4">Alternative Possibilities</h4>
                  <div className="space-y-3">
                    {result.results.slice(1).map((disease, idx) => (
                      <div
                        key={idx}
                        className="glass p-4 rounded-lg hover:bg-white/10 transition-all border border-white/5"
                      >
                        <div className="flex items-center justify-between mb-2">
                          <p className="font-semibold">{disease.disease}</p>
                          <p className="text-blue-400 font-bold">{disease.confidence}%</p>
                        </div>
                        <p className="text-sm text-gray-400">{disease.advice}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Important Notice */}
              <div className="glass p-6 rounded-xl border-l-4 border-yellow-500 bg-yellow-500/10">
                <p className="font-bold text-yellow-400 mb-2">⚠️ Important Disclaimer</p>
                <p className="text-sm text-gray-300">
                  This AI analysis is for informational purposes only and should not replace professional medical advice. 
                  Always consult a qualified healthcare provider for proper diagnosis and treatment.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-4">
                <button
                  onClick={() => {
                    setResult(null);
                    setSymptoms('');
                    setError(null);
                  }}
                  className="flex-1 px-8 py-4 glass hover:bg-white/10 rounded-xl font-bold transition-all"
                >
                  🔄 Analyze Again
                </button>
                <button className="flex-1 px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-white shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/80 transition-all">
                  💾 Save Results
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function MedicinePage() {
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const uploadRef = useRef(null);
  const titleRef = useRef(null);
  const previewRef = useRef(null);
  const resultRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(titleRef.current, 
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }
    );

    gsap.fromTo(uploadRef.current,
      { opacity: 0, scale: 0.8, rotateY: -80 },
      { opacity: 1, scale: 1, rotateY: 0, duration: 1, delay: 0.2, ease: 'back.out(1.5)', perspective: 1200 }
    );
  }, []);

  const handleUpload = () => {
    document.getElementById('medicine-upload')?.click();
  };

  const handleFileSelect = (file) => {
    if (!file) return;
    
    // Validate file size
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file');
      return;
    }

    setImageFile(file);
    setError(null);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setImagePreview(e.target.result);
      gsap.fromTo(previewRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.5)' }
      );
    };
    reader.readAsDataURL(file);
  };

  const handleVerify = async () => {
    if (!imageFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', imageFile);

    try {
      const response = await fetch('http://localhost:5000/api/verify-medicine', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Verification failed');
      }

      const data = await response.json();
      setResult(data);

      // Animate result
      gsap.fromTo(resultRef.current,
        { opacity: 0, y: 30, scale: 0.9 },
        { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'back.out(1.5)' }
      );
    } catch (err) {
      setError(err.message || 'Failed to verify medicine');
    } finally {
      setLoading(false);
    }
  };

  const resetUpload = () => {
    setImageFile(null);
    setImagePreview(null);
    setResult(null);
    setError(null);
    document.getElementById('medicine-upload').value = '';
  };

  return (
    <div className="min-h-screen max-w-5xl mx-auto px-6 py-20">
      <div className="space-y-8">
        <div ref={titleRef} className="space-y-3">
          <h2 className="text-5xl font-black gradient-text">🔬 Medicine Authenticator</h2>
          <p className="text-gray-400 text-lg">AI-powered medicine verification system - Detect counterfeit medicines instantly</p>
        </div>

        {!result ? (
          <>
            <div ref={uploadRef}
              className="glass p-12 rounded-2xl text-center space-y-6 border-2 border-dashed border-cyan-500/30 hover:border-cyan-500/60 transition-all cursor-pointer group hover:bg-white/5"
              onClick={handleUpload}
              onDragOver={(e) => {
                e.preventDefault();
                gsap.to(uploadRef.current, { scale: 1.05, duration: 0.3 });
              }}
              onDragLeave={() => {
                gsap.to(uploadRef.current, { scale: 1, duration: 0.3 });
              }}
              onDrop={(e) => {
                e.preventDefault();
                gsap.to(uploadRef.current, { scale: 1, duration: 0.3 });
                const file = e.dataTransfer.files[0];
                if (file) handleFileSelect(file);
              }}
            >
              <div className="text-6xl group-hover:scale-125 group-hover:rotate-12 transition-transform duration-300 inline-block">💊</div>
              <div>
                <h3 className="text-xl font-bold mb-2">Upload Medicine Image</h3>
                <p className="text-gray-400">PNG, JPG or WebP (Max 5MB)</p>
                <p className="text-sm text-gray-500 mt-2">or drag and drop</p>
              </div>
              <input
                id="medicine-upload"
                type="file"
                accept="image/*"
                onChange={(e) => {
                  const file = e.target.files[0];
                  if (file) handleFileSelect(file);
                }}
                className="hidden"
              />
            </div>

            {imagePreview && (
              <div ref={previewRef} className="space-y-6">
                <div className="glass p-6 rounded-2xl border border-cyan-500/30">
                  <div className="relative overflow-hidden rounded-xl">
                    <img 
                      src={imagePreview} 
                      alt="Preview" 
                      className="w-full h-64 object-cover"
                    />
                  </div>
                  <div className="mt-4 flex items-center justify-between">
                    <div>
                      <p className="text-gray-400 text-sm">File selected</p>
                      <p className="text-white font-semibold">{imageFile.name}</p>
                    </div>
                    <button
                      onClick={resetUpload}
                      className="px-4 py-2 bg-red-500/20 hover:bg-red-500/40 text-red-400 rounded-lg transition-all"
                    >
                      ✕ Clear
                    </button>
                  </div>
                </div>

                <button 
                  onClick={handleVerify}
                  disabled={loading}
                  className="w-full px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl font-bold text-white shadow-lg shadow-purple-500/50 hover:shadow-purple-500/80 transition-all hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? '🔄 Verifying...' : '🔐 Verify Authenticity'}
                </button>
              </div>
            )}

            {error && (
              <div className="glass p-6 rounded-xl border-l-4 border-red-500 flex items-start gap-4">
                <span className="text-3xl">⚠️</span>
                <div>
                  <p className="text-red-400 font-bold">Error</p>
                  <p className="text-gray-400 text-sm">{error}</p>
                </div>
              </div>
            )}
          </>
        ) : (
          <div ref={resultRef} className="space-y-6">
            {/* Main Result Card */}
            <div className={`glass p-8 rounded-2xl border-l-8 ${result.is_authentic ? 'border-green-500' : 'border-red-500'}`}>
              <div className="flex items-start justify-between mb-6">
                <div>
                  <p className="text-gray-400 text-sm mb-2">VERIFICATION RESULT</p>
                  <h3 className={`text-4xl font-black ${result.is_authentic ? 'text-green-400' : 'text-red-400'}`}>
                    {result.is_authentic ? '✓ AUTHENTIC' : '✗ COUNTERFEIT DETECTED'}
                  </h3>
                </div>
                <div className={`text-6xl ${result.is_authentic ? 'animate-bounce' : 'animate-pulse'}`}>
                  {result.is_authentic ? '🛡️' : '⚠️'}
                </div>
              </div>

              {/* Confidence Score */}
              <div className="mb-6">
                <p className="text-gray-400 text-sm mb-2">AI CONFIDENCE LEVEL</p>
                <div className="relative h-4 bg-white/5 rounded-full overflow-hidden border border-white/10">
                  <div 
                    className={`h-full rounded-full transition-all duration-1000 ${result.is_authentic ? 'bg-gradient-to-r from-green-500 to-cyan-500' : 'bg-gradient-to-r from-red-500 to-orange-500'}`}
                    style={{ width: `${(result.final_confidence || 0) * 100}%` }}
                  ></div>
                </div>
                <p className={`mt-2 font-bold text-lg ${result.is_authentic ? 'text-green-400' : 'text-red-400'}`}>
                  {Math.round((result.final_confidence || 0) * 100)}% Confidence
                </p>
              </div>

              {/* Recommendation */}
              <p className={`text-sm font-semibold p-4 rounded-lg ${result.is_authentic ? 'bg-green-500/10 text-green-300' : 'bg-red-500/10 text-red-300'}`}>
                {result.recommendation}
              </p>
            </div>

            {/* OCR Results (if available) */}
            {result.ocr_result && (
              <div className="glass p-6 rounded-2xl border border-white/10">
                <h4 className="text-lg font-bold mb-4">🔍 OCR Data Extraction</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="glass p-4 rounded-lg border border-white/5">
                    <p className="text-gray-400 text-sm">Medicine Name</p>
                    <p className="text-white font-semibold mt-1">
                      {result.ocr_result.medicine_name || 'Not detected'}
                    </p>
                  </div>
                  <div className="glass p-4 rounded-lg border border-white/5">
                    <p className="text-gray-400 text-sm">Batch Number</p>
                    <p className="text-white font-semibold mt-1">
                      {result.ocr_result.batch_number || 'Not found'}
                    </p>
                  </div>
                  <div className="glass p-4 rounded-lg border border-white/5">
                    <p className="text-gray-400 text-sm">Database Match</p>
                    <p className={`mt-1 font-semibold ${result.ocr_result.database_match ? 'text-green-400' : 'text-orange-400'}`}>
                      {result.ocr_result.database_match ? '✓ Found' : '⚠️ Not Found'}
                    </p>
                  </div>
                  <div className="glass p-4 rounded-lg border border-white/5">
                    <p className="text-gray-400 text-sm">OCR Confidence</p>
                    <p className="text-white font-semibold mt-1">
                      {Math.round((result.ocr_result.confidence || 0) * 100)}%
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Image Analysis */}
            {result.image_analysis && (
              <div className="glass p-6 rounded-2xl border border-white/10">
                <h4 className="text-lg font-bold mb-4">🎨 Image Quality Analysis</h4>
                <div className="space-y-4">
                  {/* Hologram Detection */}
                  <div className="flex items-center justify-between p-4 glass rounded-lg border border-white/5">
                    <div>
                      <p className="font-medium">Hologram Detection</p>
                      <p className="text-xs text-gray-400">Security feature verification</p>
                    </div>
                    <div className="text-right">
                      <div className="flex justify-end mb-1">
                        <span className={result.image_analysis.hologram_detected ? 'text-green-400' : 'text-gray-400'}>
                          {result.image_analysis.hologram_detected ? '✓' : '✗'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">{Math.round(result.image_analysis.hologram_confidence * 100)}%</p>
                    </div>
                  </div>

                  {/* Barcode Validation */}
                  <div className="flex items-center justify-between p-4 glass rounded-lg border border-white/5">
                    <div>
                      <p className="font-medium">Barcode Quality</p>
                      <p className="text-xs text-gray-400">Clear barcode structure</p>
                    </div>
                    <div className="text-right">
                      <div className="flex justify-end mb-1">
                        <span className={result.image_analysis.barcode_valid ? 'text-green-400' : 'text-gray-400'}>
                          {result.image_analysis.barcode_valid ? '✓' : '✗'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">{Math.round(result.image_analysis.barcode_confidence * 100)}%</p>
                    </div>
                  </div>

                  {/* Color Consistency */}
                  <div className="flex items-center justify-between p-4 glass rounded-lg border border-white/5">
                    <div>
                      <p className="font-medium">Color Consistency</p>
                      <p className="text-xs text-gray-400">Uniform color across packaging</p>
                    </div>
                    <div className="text-right">
                      <div className="flex justify-end mb-1">
                        <span className={result.image_analysis.color_consistency ? 'text-green-400' : 'text-gray-400'}>
                          {result.image_analysis.color_consistency ? '✓' : '✗'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">{Math.round(result.image_analysis.color_consistency_score * 100)}%</p>
                    </div>
                  </div>

                  {/* Text Clarity */}
                  <div className="flex items-center justify-between p-4 glass rounded-lg border border-white/5">
                    <div>
                      <p className="font-medium">Text Clarity</p>
                      <p className="text-xs text-gray-400">Sharp and legible text</p>
                    </div>
                    <div className="text-right">
                      <div className="flex justify-end mb-1">
                        <span className={result.image_analysis.text_clarity ? 'text-green-400' : 'text-gray-400'}>
                          {result.image_analysis.text_clarity ? '✓' : '✗'}
                        </span>
                      </div>
                      <p className="text-sm text-gray-400">{Math.round(result.image_analysis.text_clarity_score * 100)}%</p>
                    </div>
                  </div>

                  {/* Overall Quality */}
                  <div className="p-4 glass rounded-lg border border-cyan-500/30 bg-cyan-500/5">
                    <p className="font-medium text-cyan-400">Overall Packaging Quality</p>
                    <p className="text-xl font-bold mt-2 text-white">{result.image_analysis.overall_packaging_quality}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Explainability: Detailed Reasoning */}
            {result.reasoning && result.reasoning.length > 0 && (
              <div className="glass p-6 rounded-2xl border border-yellow-500/30 bg-yellow-500/5">
                <h4 className="text-lg font-bold mb-4 text-yellow-400">🔍 Detailed Analysis Breakdown</h4>
                <div className="space-y-4">
                  {result.reasoning.map((item, idx) => (
                    <div key={idx} className={`p-4 glass rounded-lg border-l-4 ${
                      item.status === 'PASS' ? 'border-green-500 bg-green-500/5' :
                      item.status === 'WARNING' ? 'border-yellow-500 bg-yellow-500/5' :
                      'border-red-500 bg-red-500/5'
                    }`}>
                      <div className="flex items-start justify-between mb-2">
                        <p className="font-bold">{item.layer}</p>
                        <span className={`px-2 py-1 text-xs font-bold rounded ${
                          item.status === 'PASS' ? 'bg-green-500/20 text-green-300' :
                          item.status === 'WARNING' ? 'bg-yellow-500/20 text-yellow-300' :
                          'bg-red-500/20 text-red-300'
                        }`}>
                          {item.status}
                        </span>
                      </div>
                      <p className="text-sm text-gray-300 mb-2">{item.detail}</p>
                      <div className="flex items-center justify-between">
                        <div className="w-full mr-4">
                          <div className="w-full h-2 bg-white/10 rounded-full overflow-hidden">
                            <div 
                              className={`h-full ${
                                item.status === 'PASS' ? 'bg-green-500' :
                                item.status === 'WARNING' ? 'bg-yellow-500' :
                                'bg-red-500'
                              }`}
                              style={{ width: `${item.score * 100}%` }}
                            ></div>
                          </div>
                        </div>
                        <p className="text-xs font-bold text-gray-300">{Math.round(item.score * 100)}%</p>
                      </div>
                      {item.overall_quality && (
                        <p className="text-xs text-gray-400 mt-2">Quality: {item.overall_quality}</p>
                      )}
                    </div>
                  ))}
                </div>

                {/* Overall Assessment */}
                <div className="mt-6 p-4 glass rounded-lg border border-cyan-500/30">
                  <p className="text-sm text-gray-400 mb-2">Overall Assessment</p>
                  <p className="text-lg font-bold text-cyan-400">
                    {result.is_authentic ? '✅ This medicine appears AUTHENTIC' : '⚠️ This medicine appears SUSPICIOUS/COUNTERFEIT'}
                  </p>
                </div>
              </div>
            )}

            {/* Decision Logic */}
            {result.decision_logic && (
              <div className="glass p-6 rounded-2xl border border-white/10">
                <h4 className="text-lg font-bold mb-4">⚙️ Decision Logic Breakdown</h4>
                <div className="space-y-3">
                  {result.decision_logic.component_scores && result.decision_logic.component_scores.map((component, idx) => (
                    <div key={idx} className="glass p-4 rounded-lg border border-white/5">
                      <div className="flex items-center justify-between mb-2">
                        <p className="font-medium">{component.component}</p>
                        <p className="text-blue-400 font-bold">{Math.round(component.score * 100)}%</p>
                      </div>
                      <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                          style={{ width: `${component.score * 100}%` }}
                        ></div>
                      </div>
                      <p className="text-xs text-gray-400 mt-2">Weight: {Math.round(component.weight * 100)}%</p>
                    </div>
                  ))}
                  <div className="p-4 glass rounded-lg border border-purple-500/30 bg-purple-500/5">
                    <p className="text-gray-400 text-sm">Threshold for Authenticity</p>
                    <p className="text-2xl font-bold text-purple-400 mt-1">≥ {Math.round(result.decision_logic.threshold * 100)}%</p>
                  </div>
                </div>
              </div>
            )}

            {/* Image Preview */}
            <div className="glass p-6 rounded-2xl border border-white/10">
              <p className="text-gray-400 text-sm mb-4">SCANNED IMAGE</p>
              <div className="relative overflow-hidden rounded-xl">
                <img 
                  src={imagePreview} 
                  alt="Verified" 
                  className="w-full h-64 object-cover"
                />
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button 
                onClick={resetUpload}
                className="flex-1 px-8 py-4 bg-white/5 hover:bg-white/10 rounded-xl font-bold text-white transition-all"
              >
                📸 Verify Another
              </button>
              <button 
                className="flex-1 px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl font-bold text-white shadow-lg shadow-purple-500/50 hover:shadow-purple-500/80 transition-all"
              >
                💾 Save Report
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function ChatPage() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Hello! 👋 I\'m your AI health assistant. How can I help you today?' },
  ]);
  const [input, setInput] = useState('');
  const messagesRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(containerRef.current,
      { opacity: 0, y: 50 },
      { opacity: 1, y: 0, duration: 0.8, ease: 'power3.out' }
    );
  }, []);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
      
      // Animate new messages
      const newMessages = messagesRef.current.querySelectorAll('[data-new="true"]');
      gsap.fromTo(newMessages,
        { opacity: 0, y: 20, scale: 0.9 },
        { opacity: 1, y: 0, scale: 1, duration: 0.5, ease: 'back.out(1.5)' }
      );
    }
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    
    setMessages([...messages, { role: 'user', text: input }]);
    setInput('');

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          text: 'Thanks for your question! Based on your query, I recommend consulting with a healthcare professional for personalized medical advice.',
        },
      ]);
    }, 800);
  };

  return (
    <div ref={containerRef} className="min-h-screen max-w-2xl mx-auto px-6 py-20">
      <div className="glass rounded-2xl h-96 flex flex-col overflow-hidden border border-white/10">
        <div className="p-6 border-b border-white/10 bg-gradient-to-r from-cyan-500/10 to-blue-500/10">
          <h2 className="text-2xl font-bold gradient-text">🤖 Health AI Chat</h2>
        </div>

        <div ref={messagesRef} className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} data-new="true" className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-xs px-4 py-3 rounded-lg ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-br-none shadow-lg shadow-cyan-500/30'
                    : 'glass rounded-bl-none border border-white/10'
                }`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        <div className="p-4 border-t border-white/10 flex gap-2 bg-slate-900/50">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask anything..."
            className="flex-1 glass rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
          />
          <button
            onClick={handleSend}
            className="px-6 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all hover:scale-105 active:scale-95"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

function HistoryPage() {
  const [symptomHistory, setSymptomHistory] = useState([]);
  const [medicineHistory, setMedicineHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('symptoms');
  const [selectedReport, setSelectedReport] = useState(null);
  const itemsRef = useRef([]);
  const containerRef = useRef(null);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    if (!loading) {
      gsap.fromTo(containerRef.current?.querySelector('h2'),
        { opacity: 0, x: -50 },
        { opacity: 1, x: 0, duration: 0.8, ease: 'power3.out' }
      );

      gsap.fromTo(itemsRef.current,
        { opacity: 0, x: -50, rotateY: -90 },
        { 
          opacity: 1, 
          x: 0, 
          rotateY: 0,
          stagger: 0.12, 
          duration: 0.8, 
          delay: 0.2,
          ease: 'back.out(1.5)',
          perspective: 1200
        }
      );

      itemsRef.current.forEach((item) => {
        if (item) {
          item.addEventListener('mouseenter', () => {
            gsap.to(item, { 
              x: 10, 
              duration: 0.3,
              boxShadow: '0 0 30px rgba(6, 182, 212, 0.3)'
            });
          });
          item.addEventListener('mouseleave', () => {
            gsap.to(item, { 
              x: 0, 
              duration: 0.3,
              boxShadow: 'none'
            });
          });
        }
      });
    }
  }, [loading]);

  const fetchHistory = async () => {
    try {
      const [symp, med] = await Promise.all([
        fetch('http://localhost:5000/api/symptoms/history').then(r => r.json()),
        fetch('http://localhost:5000/api/medicine/history').then(r => r.json())
      ]);
      setSymptomHistory(symp.data || []);
      setMedicineHistory(med.data || []);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching history:', err);
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const items = activeTab === 'symptoms' ? symptomHistory : medicineHistory;

  if (selectedReport) {
    return (
      <div className="min-h-screen max-w-4xl mx-auto px-6 py-20">
        <button
          onClick={() => setSelectedReport(null)}
          className="mb-6 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
        >
          ← Back to History
        </button>

        <div className="glass p-8 rounded-2xl border border-white/10 space-y-6">
          {activeTab === 'symptoms' && (
            <>
              <h2 className="text-3xl font-bold gradient-text">Symptom Analysis Report</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="glass p-4 rounded-xl border border-white/10">
                  <p className="text-gray-400">Primary Disease</p>
                  <p className="text-xl font-bold text-cyan-400">{selectedReport.primary_disease}</p>
                </div>
                <div className="glass p-4 rounded-xl border border-white/10">
                  <p className="text-gray-400">Confidence</p>
                  <p className="text-xl font-bold text-green-400">{(selectedReport.confidence * 100).toFixed(1)}%</p>
                </div>
                <div className="glass p-4 rounded-xl border border-white/10">
                  <p className="text-gray-400">Risk Level</p>
                  <p className={`text-xl font-bold ${
                    selectedReport.risk_level === 'High' ? 'text-red-400' :
                    selectedReport.risk_level === 'Medium' ? 'text-yellow-400' :
                    'text-green-400'
                  }`}>{selectedReport.risk_level}</p>
                </div>
              </div>

              {selectedReport.emergency_alert && (
                <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-xl">
                  <p className="text-red-300 font-bold">⚠️ Emergency Alert: Seek immediate medical attention</p>
                </div>
              )}

              <div>
                <h3 className="text-xl font-bold mb-3">Symptoms Analyzed</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedReport.symptoms?.map((sym, idx) => (
                    <span key={idx} className="px-3 py-1 glass rounded-full text-sm text-cyan-300">
                      {sym}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-xl font-bold mb-3">Recommendations</h3>
                <div className="space-y-2">
                  {selectedReport.recommendations?.map((rec, idx) => (
                    <p key={idx} className="text-gray-300">• {rec}</p>
                  ))}
                </div>
              </div>

              <p className="text-xs text-gray-500">Analyzed on: {formatDate(selectedReport.created_at)}</p>
            </>
          )}

          {activeTab === 'medicine' && (
            <>
              <h2 className="text-3xl font-bold gradient-text">Medicine Verification Report</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="glass p-4 rounded-xl border border-white/10">
                  <p className="text-gray-400">Status</p>
                  <p className={`text-xl font-bold ${selectedReport.is_authentic ? 'text-green-400' : 'text-red-400'}`}>
                    {selectedReport.is_authentic ? '✓ Authentic' : '✗ Counterfeit'}
                  </p>
                </div>
                <div className="glass p-4 rounded-xl border border-white/10">
                  <p className="text-gray-400">Confidence</p>
                  <p className="text-xl font-bold text-cyan-400">{(selectedReport.confidence * 100).toFixed(1)}%</p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h3 className="font-bold mb-2">OCR Extracted Data</h3>
                  <div className="glass p-3 rounded text-sm space-y-1 text-gray-300">
                    {selectedReport.ocr_data && Object.entries(selectedReport.ocr_data).map(([k, v]) => (
                      <p key={k}><span className="text-cyan-400">{k}:</span> {String(v)}</p>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="font-bold mb-2">Image Analysis</h3>
                  <div className="glass p-3 rounded text-sm space-y-1 text-gray-300">
                    {selectedReport.image_analysis && Object.entries(selectedReport.image_analysis).map(([k, v]) => (
                      <p key={k}><span className="text-cyan-400">{k}:</span> {String(v)}</p>
                    ))}
                  </div>
                </div>
              </div>

              <p className="text-gray-300">{selectedReport.recommendation}</p>
              <p className="text-xs text-gray-500">Analyzed on: {formatDate(selectedReport.created_at)}</p>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="min-h-screen max-w-4xl mx-auto px-6 py-20">
      <div className="space-y-8">
        <h2 className="text-5xl font-black gradient-text">📋 Health History</h2>
        
        {/* Tab Buttons */}
        <div className="flex gap-4">
          <button
            onClick={() => setActiveTab('symptoms')}
            className={`px-6 py-3 rounded-lg font-bold transition-all ${
              activeTab === 'symptoms'
                ? 'bg-cyan-500/30 border border-cyan-500'
                : 'bg-white/5 border border-white/10 hover:bg-white/10'
            }`}
          >
            🩺 Symptoms ({symptomHistory.length})
          </button>
          <button
            onClick={() => setActiveTab('medicine')}
            className={`px-6 py-3 rounded-lg font-bold transition-all ${
              activeTab === 'medicine'
                ? 'bg-cyan-500/30 border border-cyan-500'
                : 'bg-white/5 border border-white/10 hover:bg-white/10'
            }`}
          >
            💊 Medicine ({medicineHistory.length})
          </button>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <p className="text-gray-400">Loading history...</p>
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">No {activeTab} history yet. Start by analyzing your health!</p>
          </div>
        ) : (
          <div className="space-y-4 relative">
            {/* Timeline line */}
            <div className="absolute left-4 top-0 bottom-0 w-0.5 bg-gradient-to-b from-cyan-500 to-purple-600"></div>

            {items.map((item, idx) => (
              <div
                key={item.id}
                ref={(el) => (itemsRef.current[idx] = el)}
                onClick={() => setSelectedReport(item)}
                className="glass p-6 rounded-xl hover:bg-white/10 transition-all border-l-4 border-cyan-500 group cursor-pointer ml-8 relative"
              >
                {/* Timeline dot */}
                <div className="absolute -left-10 top-6 w-6 h-6 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 border-4 border-slate-950"></div>

                <div className="space-y-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-lg group-hover:text-cyan-400 transition-colors">
                        {activeTab === 'symptoms' ? item.primary_disease : 
                         (item.is_authentic ? '✓ Authentic Medicine' : '✗ Counterfeit Medicine')}
                      </h3>
                      <p className="text-gray-400">
                        {activeTab === 'symptoms' 
                          ? `${item.symptoms?.length || 0} symptoms analyzed`
                          : item.image_filename}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-400">{formatDate(item.created_at)}</p>
                      <p className={`font-bold text-lg ${
                        activeTab === 'symptoms'
                          ? 'text-cyan-400'
                          : item.is_authentic ? 'text-green-400' : 'text-red-400'
                      }`}>
                        {(item.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-2 text-sm">
                    <div className="glass p-2 rounded text-center">
                      <p className="text-gray-400">Risk</p>
                      <p className={`font-bold ${
                        item.risk_level === 'High' ? 'text-red-400' :
                        item.risk_level === 'Medium' ? 'text-yellow-400' :
                        'text-green-400'
                      }`}>{item.risk_level || 'N/A'}</p>
                    </div>
                    <div className="glass p-2 rounded text-center">
                      <p className="text-gray-400">Type</p>
                      <p className="text-cyan-400 font-bold">{activeTab === 'symptoms' ? 'Analysis' : 'Verification'}</p>
                    </div>
                    <div className="glass p-2 rounded text-center">
                      <p className="text-gray-400">Confidence</p>
                      <p className="text-green-400 font-bold">{(item.confidence * 100).toFixed(0)}%</p>
                    </div>
                  </div>

                  <p className="text-xs text-gray-500">Click to view full report →</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
