import React, { useState, useEffect, useRef, useMemo, createContext, useContext } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import AnimatedGradientBackground from './components/AnimatedGradientBackground';

gsap.registerPlugin(ScrollTrigger);

// Global Language Context and Dictionary
export const LanguageContext = createContext();

const translations = {
  en: {
    nav: { home: 'Home', symptom: 'Symptom', medicine: 'Medicine', chat: 'Chat', history: 'History' },
    hero: { your: 'Your', ai: 'AI', health: 'Health', companion: 'Companion', desc: 'Advanced AI-powered health analysis, medicine verification, and 24/7 health support. All in one intelligent platform.', start: 'Start Now', learn: 'Learn More' },
    features: { diag_title: 'Smart Diagnosis', diag_desc: 'AI-powered symptom analysis', med_title: 'Medicine Check', med_desc: 'Verify authenticity instantly', ai_title: 'AI Assistant', ai_desc: '24/7 health guidance' },
    stats: { users: 'Active Users', acc: 'Accuracy Rate', time: 'Response Time', countries: 'Countries' },
    symptom: { title: 'Symptom Analyzer', subtitle: 'AI-powered disease prediction from your symptoms', desc: 'Describe your symptoms:', ph: 'e.g., I have fever, cough, headache, and fatigue...', common: 'Or select common symptoms:', analyze: 'Analyze Symptoms', analyzing: 'Analyzing...', clear: 'Clear' },
    medicine: { title: 'Medicine Authenticator', subtitle: 'AI-powered medicine verification system - Detect counterfeit medicines instantly', upload: 'Upload Medicine Image', format: 'PNG, JPG or WebP (Max 5MB)', drag: 'or drag and drop', verify: 'Verify Authenticity', verifying: 'Verifying...', clear: 'Clear' },
    chat: { title: 'AI Health Chat', ph: 'Type your health question...', btn: 'Send' },
    history: { title: 'Health History', symp_tab: 'Symptoms', med_tab: 'Medicine', loading: 'Loading history...', empty: 'No history yet. Start by analyzing your health!', back: 'Back to History' },
    login: { title: 'Welcome Back', subtitle: 'Login to access your health history and more.', email: 'Email Address', email_ph: 'you@example.com', password: 'Password', forgot: 'Forgot Password?', login_btn: 'Login', no_account: "Don't have an account?", signup: 'Sign Up' },
    signup: { title: 'Create Account', subtitle: 'Join us to start your health journey.', name: 'Full Name', name_ph: 'John Doe', email: 'Email Address', email_ph: 'you@example.com', password: 'Password', confirm: 'Confirm Password', signup_btn: 'Sign Up', have_account: 'Already have an account?', login: 'Login' },
    about: { title: 'About HealthAI', subtitle: 'Your trusted AI-powered health companion.', desc1: 'HealthAI is an advanced platform leveraging artificial intelligence to provide instant symptom analysis, verify medicine authenticity, and offer 24/7 health guidance.', desc2: 'Our mission is to make healthcare information accessible, accurate, and easy to understand for everyone.', warning: 'Please remember that our AI is an informational tool and not a substitute for professional medical advice.', back: 'Back to Home' }
  },
  hi: {
    nav: { home: 'होम', symptom: 'लक्षण', medicine: 'दवा', chat: 'चैट', history: 'इतिहास' },
    hero: { your: 'आपका', ai: 'AI', health: 'स्वास्थ्य', companion: 'साथी', desc: 'उन्नत एआई-संचालित स्वास्थ्य विश्लेषण, दवा सत्यापन, और 24/7 स्वास्थ्य सहायता। सब कुछ एक बुद्धिमान मंच में।', start: 'अभी शुरू करें', learn: 'और जानें' },
    features: { diag_title: 'स्मार्ट निदान', diag_desc: 'एआई-संचालित लक्षण विश्लेषण', med_title: 'दवा की जाँच', med_desc: 'तुरंत प्रामाणिकता सत्यापित करें', ai_title: 'एआई सहायक', ai_desc: '24/7 स्वास्थ्य मार्गदर्शन' },
    stats: { users: 'सक्रिय उपयोगकर्ता', acc: 'सटीकता दर', time: 'प्रतिक्रिया समय', countries: 'देश' },
    symptom: { title: 'लक्षण विश्लेषक', subtitle: 'आपके लक्षणों से एआई-संचालित रोग भविष्यवाणी', desc: 'अपने लक्षणों का वर्णन करें:', ph: 'उदा., मुझे बुखार, खांसी, सिरदर्द है...', common: 'या सामान्य लक्षणों का चयन करें:', analyze: 'लक्षणों का विश्लेषण करें', analyzing: 'विश्लेषण कर रहा है...', clear: 'साफ़ करें' },
    medicine: { title: 'दवा प्रमाणक', subtitle: 'एआई-संचालित दवा सत्यापन प्रणाली', upload: 'दवा की छवि अपलोड करें', format: 'PNG, JPG या WebP (अधिकतम 5MB)', drag: 'या खींचें और छोड़ें', verify: 'प्रामाणिकता सत्यापित करें', verifying: 'सत्यापित कर रहा है...', clear: 'साफ़ करें' },
    chat: { title: 'एआई स्वास्थ्य चैट', ph: 'अपना स्वास्थ्य प्रश्न टाइप करें...', btn: 'भेजें' },
    history: { title: 'स्वास्थ्य इतिहास', symp_tab: 'लक्षण', med_tab: 'दवा', loading: 'इतिहास लोड हो रहा है...', empty: 'अभी तक कोई इतिहास नहीं है। अपने स्वास्थ्य का विश्लेषण करके शुरू करें!', back: 'इतिहास पर वापस जाएं' },
    login: { title: 'वापसी पर स्वागत है', subtitle: 'अपने स्वास्थ्य इतिहास और अधिक तक पहुंचने के लिए लॉगिन करें।', email: 'ईमेल पता', email_ph: 'you@example.com', password: 'पासवर्ड', forgot: 'पासवर्ड भूल गए?', login_btn: 'लॉगिन करें', no_account: 'खाता नहीं है?', signup: 'साइन अप करें' },
    signup: { title: 'खाता बनाएं', subtitle: 'अपनी स्वास्थ्य यात्रा शुरू करने के लिए हमसे जुड़ें।', name: 'पूरा नाम', name_ph: 'जॉन डो', email: 'ईमेल पता', email_ph: 'you@example.com', password: 'पासवर्ड', confirm: 'पासवर्ड की पुष्टि करें', signup_btn: 'साइन अप करें', have_account: 'क्या आपके पास पहले से एक खाता है?', login: 'लॉगिन करें' },
    about: { title: 'HealthAI के बारे में', subtitle: 'आपका विश्वसनीय एआई-संचालित स्वास्थ्य साथी।', desc1: 'HealthAI एक उन्नत मंच है जो त्वरित लक्षण विश्लेषण प्रदान करने, दवा की प्रामाणिकता सत्यापित करने और 24/7 स्वास्थ्य मार्गदर्शन प्रदान करने के लिए कृत्रिम बुद्धिमत्ता का लाभ उठाता है।', desc2: 'हमारा मिशन स्वास्थ्य देखभाल की जानकारी को सभी के लिए सुलभ, सटीक और समझने में आसान बनाना है।', warning: 'कृपया याद रखें कि हमारा एआई एक सूचनात्मक उपकरण है और पेशेवर चिकित्सा सलाह का विकल्प नहीं है।', back: 'होम पर वापस जाएं' }
  },
  bn: {
    nav: { home: 'হোম', symptom: 'লক্ষণ', medicine: 'ওষুধ', chat: 'চ্যাট', history: 'ইতিহাস' },
    hero: { your: 'আপনার', ai: 'AI', health: 'স্বাস্থ্য', companion: 'সঙ্গী', desc: 'উন্নত এআই-চালিত স্বাস্থ্য বিশ্লেষণ, ওষুধ যাচাইকরণ এবং 24/7 স্বাস্থ্য সহায়তা। সবকিছু একটি বুদ্ধিমান প্ল্যাটফর্মে।', start: 'এখন শুরু করুন', learn: 'আরও জানুন' },
    features: { diag_title: 'স্মার্ট রোগ নির্ণয়', diag_desc: 'এআই-চালিত লক্ষণ বিশ্লেষণ', med_title: 'ওষুধ চেক', med_desc: 'অবিলম্বে সত্যতা যাচাই করুন', ai_title: 'এআই সহকারী', ai_desc: '24/7 স্বাস্থ্য নির্দেশিকা' },
    stats: { users: 'সক্রিয় ব্যবহারকারী', acc: 'সঠিকতা হার', time: 'প্রতিক্রিয়া সময়', countries: 'দেশ' },
    symptom: { title: 'লক্ষণ বিশ্লেষক', subtitle: 'আপনার লক্ষণ থেকে এআই-চালিত রোগ পূর্বাভাস', desc: 'আপনার লক্ষণ বর্ণনা করুন:', ph: 'যেমন, আমার জ্বর, কাশি, মাথাব্যথা আছে...', common: 'বা সাধারণ লক্ষণ নির্বাচন করুন:', analyze: 'লক্ষণ বিশ্লেষণ করুন', analyzing: 'বিশ্লেষণ করা হচ্ছে...', clear: 'পরিষ্কার করুন' },
    medicine: { title: 'ওষুধ যাচাইকারী', subtitle: 'এআই-চালিত ওষুধ যাচাইকরণ সিস্টেম', upload: 'ওষুধের ছবি আপলোড করুন', format: 'PNG, JPG বা WebP (সর্বোচ্চ 5MB)', drag: 'বা টেনে আনুন এবং ছেড়ে দিন', verify: 'সত্যতা যাচাই করুন', verifying: 'যাচাই করা হচ্ছে...', clear: 'পরিষ্কার করুন' },
    chat: { title: 'এআই স্বাস্থ্য চ্যাট', ph: 'আপনার স্বাস্থ্য প্রশ্ন টাইপ করুন...', btn: 'পাঠান' },
    history: { title: 'স্বাস্থ্য ইতিহাস', symp_tab: 'লক্ষণ', med_tab: 'ওষুধ', loading: 'ইতিহাস লোড হচ্ছে...', empty: 'এখনও কোন ইতিহাস নেই। আপনার স্বাস্থ্য বিশ্লেষণ করে শুরু করুন!', back: 'ইতিহাসে ফিরে যান' },
    login: { title: 'স্বাগতম', subtitle: 'আপনার স্বাস্থ্য ইতিহাস এবং আরও অনেক কিছু অ্যাক্সেস করতে লগইন করুন।', email: 'ইমেল ঠিকানা', email_ph: 'you@example.com', password: 'পাসওয়ার্ড', forgot: 'পাসওয়ার্ড ভুলে গেছেন?', login_btn: 'লগইন করুন', no_account: 'অ্যাকাউন্ট নেই?', signup: 'সাইন আপ করুন' },
    signup: { title: 'অ্যাকাউন্ট তৈরি করুন', subtitle: 'আপনার স্বাস্থ্য যাত্রা শুরু করতে আমাদের সাথে যোগ দিন।', name: 'পুরো নাম', name_ph: 'জন ডো', email: 'ইমেল ঠিকানা', email_ph: 'you@example.com', password: 'পাসওয়ার্ড', confirm: 'পাসওয়ার্ড নিশ্চিত করুন', signup_btn: 'সাইন আপ করুন', have_account: 'ইতিমধ্যেই একটি অ্যাকাউন্ট আছে?', login: 'লগইন করুন' },
    about: { title: 'HealthAI সম্পর্কে', subtitle: 'আপনার বিশ্বস্ত এআই-চালিত স্বাস্থ্য সঙ্গী।', desc1: 'HealthAI হল একটি উন্নত প্ল্যাটফর্ম যা তাত্ক্ষণিক লক্ষণ বিশ্লেষণ প্রদান করতে, ওষুধের সত্যতা যাচাই করতে এবং 24/7 স্বাস্থ্য নির্দেশিকা প্রদান করতে কৃত্রিম বুদ্ধিমত্তা ব্যবহার করে।', desc2: 'আমাদের লক্ষ্য হল স্বাস্থ্যসেবা তথ্য সবার জন্য অ্যাক্সেসযোগ্য, সঠিক এবং সহজে বোঝা যায় এমন করা।', warning: 'দয়া করে মনে রাখবেন যে আমাদের এআই একটি তথ্যমূলক সরঞ্জাম এবং পেশাদার চিকিৎসা পরামর্শের বিকল্প নয়।', back: 'হোমে ফিরে যান' }
  }
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [scrollY, setScrollY] = useState(0);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const containerRef = useRef(null);

  // Language State
  const [language, setLanguage] = useState('en');
  // Translation function that gracefully falls back to English or the raw key if a translation is missing
  const t = (section, key) => translations[language]?.[section]?.[key] || translations['en']?.[section]?.[key] || key;

  // Generate random properties for particles and icons
  const particles = useMemo(() => [...Array(30)].map(() => ({
    size: Math.random() * 4 + 1,
    top: Math.random() * 100,
    left: Math.random() * 100,
    duration: Math.random() * 5 + 5,
    yOffset: Math.random() * 100 + 50,
    xOffset: Math.random() * 50 - 25,
  })), []);

  const floatingIcons = useMemo(() => [...Array(15)].map((_, i) => ({
    // Health themed emojis: pill, heart, cross
    icon: ['💊', '❤️', '➕'][i % 3],
    top: Math.random() * 100,
    left: Math.random() * 100,
    rotation: Math.random() * 360,
    size: Math.random() * 16 + 10,
    duration: Math.random() * 6 + 6,
    yOffset: Math.random() * 60 + 30,
    rotOffset: Math.random() * 180 - 90,
  })), []);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Sync URL with page state
  useEffect(() => {
    const path = window.location.pathname.slice(1) || 'home';
    const page = ['home', 'symptom', 'medicine', 'chat', 'history', 'login', 'signup', 'about'].includes(path) ? path : 'home';
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

  // Animate particles and icons using GSAP
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.utils.toArray('.bg-particle').forEach((particle, i) => {
        gsap.to(particle, {
          y: `-=${particles[i].yOffset}`,
          x: `+=${particles[i].xOffset}`,
          duration: particles[i].duration,
          repeat: -1,
          yoyo: true,
          ease: 'sine.inOut'
        });
      });
      gsap.utils.toArray('.bg-floating-icon').forEach((icon, i) => {
        gsap.to(icon, {
          y: `-=${floatingIcons[i].yOffset}`,
          rotation: `+=${floatingIcons[i].rotOffset}`,
          duration: floatingIcons[i].duration,
          repeat: -1,
          yoyo: true,
          ease: 'sine.inOut'
        });
      });
    }, containerRef);
    return () => ctx.revert();
  }, [particles, floatingIcons]);

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
    <div ref={containerRef} className={`min-h-screen overflow-hidden transition-colors duration-500 ${isDarkMode ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'}`}>
      <AnimatedGradientBackground />
      
      {/* Animated background orbs */}
      <div className="fixed inset-0 -z-5 overflow-hidden pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-1/3 right-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>

        {/* Floating Particles */}
        {particles.map((p, i) => (
          <div
            key={`particle-${i}`}
            className={`bg-particle absolute rounded-full bg-current transition-opacity duration-500 ${isDarkMode ? 'opacity-20' : 'opacity-10'}`}
            style={{
              width: `${p.size}px`,
              height: `${p.size}px`,
              top: `${p.top}%`,
              left: `${p.left}%`,
            }}
          />
        ))}

        {/* Floating Icons */}
        {floatingIcons.map((fi, i) => (
          <div
            key={`icon-${i}`}
            className={`bg-floating-icon absolute transition-opacity duration-500 ${isDarkMode ? 'opacity-10' : 'opacity-5'}`}
            style={{
              top: `${fi.top}%`,
              left: `${fi.left}%`,
              fontSize: `${fi.size}px`,
              transform: `rotate(${fi.rotation}deg)`
            }}
          >
            {fi.icon}
          </div>
        ))}
      </div>

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3 group cursor-pointer" onClick={() => setCurrentPage('home')}>
            <div className="relative w-12 h-12 rounded-full bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/50 group-hover:shadow-cyan-500/80 transition-all">
              <span className="text-xl font-bold">🔬</span>
            </div>
            <div>
              <h1 className="text-2xl font-black gradient-text">HealthAI</h1>
              <p className="text-xs text-gray-400">AI-Powered Health</p>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-8">
            {['home', 'symptom', 'medicine', 'chat', 'history'].map((item) => (
              <button
                key={item}
                onClick={() => setCurrentPage(item)}
                className={`relative px-4 py-2 transition-all capitalize ${
                  currentPage === item
                    ? 'text-cyan-400 font-semibold'
                    : 'text-gray-300 hover:text-white'
                }`}
              >
                {t('nav', item)}
                {currentPage === item && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-400 to-purple-600"></div>
                )}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="p-2 glass rounded-lg bg-transparent border border-white/10 text-sm outline-none cursor-pointer focus:ring-2 focus:ring-cyan-500"
            >
              <option value="en" className="bg-slate-900 text-white">EN</option>
              <option value="hi" className="bg-slate-900 text-white">हिंदी</option>
              <option value="bn" className="bg-slate-900 text-white">বাংলা</option>
            </select>
            <button 
              onClick={() => setIsDarkMode(!isDarkMode)}
              className="p-2.5 glass rounded-full hover:bg-white/20 transition-all"
              title="Toggle Theme"
            >
              {isDarkMode ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="relative z-10 pt-24">
        {currentPage === 'home' && <HomePage setCurrentPage={setCurrentPage} />}
        {currentPage === 'symptom' && <SymptomPage />}
        {currentPage === 'medicine' && <MedicinePage />}
        {currentPage === 'chat' && <ChatPage />}
        {currentPage === 'history' && <HistoryPage />}
        {currentPage === 'login' && <LoginPage setCurrentPage={setCurrentPage} />}
        {currentPage === 'signup' && <SignupPage setCurrentPage={setCurrentPage} />}
        {currentPage === 'about' && <AboutPage setCurrentPage={setCurrentPage} />}
      </main>
    </div>
    </LanguageContext.Provider>
  );
}

function HomePage({ setCurrentPage }) {
  const { t } = useContext(LanguageContext);
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
            <span className="gradient-text inline-block mr-3">{t('hero', 'your')}</span>
            <span className="gradient-text inline-block mr-3">{t('hero', 'ai')}</span>
            <span className="gradient-text inline-block">{t('hero', 'health')}</span>
            <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400 inline-block">{t('hero', 'companion')}</span>
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl leading-relaxed animate-fade-in-delayed">
            {t('hero', 'desc')}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 pt-4">
            <button onClick={() => setCurrentPage('login')} className="magnetic-btn relative group px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-white shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/80 transition-all overflow-hidden">
              <span className="relative z-10 flex items-center gap-2">
                {t('hero', 'start')}
                <span className="group-hover:translate-x-2 transition-transform">→</span>
              </span>
              <div className="ripple-effect absolute inset-0 bg-white opacity-0 group-hover:opacity-10 rounded-xl"></div>
            </button>
            <button onClick={() => setCurrentPage('about')} className="magnetic-btn px-8 py-4 glass rounded-xl font-bold hover:bg-white/10 transition-all relative overflow-hidden group">
              <span className="relative z-10">{t('hero', 'learn')}</span>
              <div className="ripple-effect absolute inset-0 bg-cyan-400 opacity-0 group-hover:opacity-20 rounded-xl"></div>
            </button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 pt-12">
          {[
            { icon: '🩺', title: t('features', 'diag_title'), desc: t('features', 'diag_desc'), color: 'from-cyan-500 to-blue-600' },
            { icon: '💊', title: t('features', 'med_title'), desc: t('features', 'med_desc'), color: 'from-purple-500 to-pink-600' },
            { icon: '🤖', title: t('features', 'ai_title'), desc: t('features', 'ai_desc'), color: 'from-blue-500 to-cyan-600' },
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
          { label: t('stats', 'users'), value: '100', suffix: 'K+' },
          { label: t('stats', 'acc'), value: '98', suffix: '%' },
          { label: t('stats', 'time'), value: '500', suffix: 'ms' },
          { label: t('stats', 'countries'), value: '150', suffix: '+' },
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

function AboutPage({ setCurrentPage }) {
  const { t } = useContext(LanguageContext);
  const containerRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(containerRef.current,
      { opacity: 0, y: 30, scale: 0.98 },
      { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'power3.out' }
    );
  }, []);

  return (
    <div ref={containerRef} className="min-h-screen max-w-4xl mx-auto px-6 py-20">
      <button
        onClick={() => setCurrentPage('home')}
        className="mb-8 px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all"
      >
        ← {t('about', 'back')}
      </button>

      <div className="glass p-12 rounded-2xl space-y-8 border border-white/10">
        <div className="text-center space-y-4">
          <div className="inline-flex relative w-24 h-24 rounded-full bg-gradient-to-br from-cyan-400 to-purple-600 items-center justify-center shadow-lg shadow-cyan-500/50 mb-4 animate-bounce">
            <span className="text-5xl">🔬</span>
          </div>
          <h2 className="text-5xl font-black gradient-text">{t('about', 'title')}</h2>
          <p className="text-xl text-cyan-400 font-semibold">{t('about', 'subtitle')}</p>
        </div>

        <div className="space-y-6 text-lg text-gray-300 leading-relaxed mt-12">
          <p className="glass p-6 rounded-xl border-l-4 border-cyan-500 bg-cyan-500/5 hover:bg-cyan-500/10 transition-colors">{t('about', 'desc1')}</p>
          <p className="glass p-6 rounded-xl border-l-4 border-purple-500 bg-purple-500/5 hover:bg-purple-500/10 transition-colors">{t('about', 'desc2')}</p>
          
          <div className="p-6 bg-yellow-500/10 border border-yellow-500/30 rounded-xl mt-8">
            <p className="text-yellow-400 font-bold flex items-center gap-2 mb-2">
              <span className="text-2xl">⚠️</span> Important Notice
            </p>
            <p className="text-yellow-200/80 text-base">{t('about', 'warning')}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function LoginPage({ setCurrentPage }) {
  const { t } = useContext(LanguageContext);
  const containerRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(containerRef.current,
      { opacity: 0, y: 50, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'power3.out' }
    );
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    // Here you would add actual login logic with API calls
    // For now, let's just navigate back to the home page after "login"
    setCurrentPage('home');
  };

  return (
    <div ref={containerRef} className="min-h-screen max-w-md mx-auto px-6 py-20">
      <div className="glass p-12 rounded-2xl space-y-8 border border-white/10 text-center">
        <h2 className="text-4xl font-black gradient-text">{t('login', 'title')}</h2>
        <p className="text-gray-400">{t('login', 'subtitle')}</p>
        
        <form onSubmit={handleLogin} className="space-y-6 text-left">
          <div>
            <label className="block text-sm text-gray-400 mb-2">{t('login', 'email')}</label>
            <input 
              type="email"
              placeholder={t('login', 'email_ph')}
              required
              className="w-full glass rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">{t('login', 'password')}</label>
            <input 
              type="password"
              placeholder="••••••••"
              required
              className="w-full glass rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            />
          </div>
          <div className="text-right">
            <a href="#" onClick={(e) => e.preventDefault()} className="text-sm text-cyan-400 hover:underline">{t('login', 'forgot')}</a>
          </div>
          
          <button
            type="submit"
            className="w-full px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-white shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/80 transition-all hover:scale-105 active:scale-95"
          >
            {t('login', 'login_btn')}
          </button>
        </form>

        <p className="text-sm text-gray-400">
          {t('login', 'no_account')}{' '}
          <button onClick={() => setCurrentPage('signup')} className="font-bold text-cyan-400 hover:underline">{t('login', 'signup')}</button>
        </p>
      </div>
    </div>
  );
}

function SymptomPage() {
  const { t } = useContext(LanguageContext);
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
          <h2 className="text-5xl font-black gradient-text">🩺 {t('symptom', 'title')}</h2>
          <p className="text-gray-400 text-lg">{t('symptom', 'subtitle')}</p>
        </div>

        {!result ? (
          <>
            {/* Input Form */}
            <div ref={formRef} className="glass p-12 rounded-2xl space-y-6 border border-white/10">
              {/* Textarea */}
              <div>
                <label className="block text-sm text-gray-400 mb-3">{t('symptom', 'desc')}</label>
                <textarea
                  value={symptoms}
                  onChange={(e) => setSymptoms(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={t('symptom', 'ph')}
                  className="w-full h-32 glass rounded-xl p-4 text-white placeholder-gray-500 resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
                />
              </div>

              {/* Quick symptom selection */}
              <div>
                <label className="block text-sm text-gray-400 mb-3">{t('symptom', 'common')}</label>
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
                  {loading ? `🔄 ${t('symptom', 'analyzing')}` : `🔍 ${t('symptom', 'analyze')}`}
                </button>
                <button
                  onClick={() => {
                    setSymptoms('');
                    setError(null);
                  }}
                  className="px-8 py-4 glass rounded-xl font-bold hover:bg-white/10 transition-all"
                >
                  {t('symptom', 'clear')}
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

function SignupPage({ setCurrentPage }) {
  const { t } = useContext(LanguageContext);
  const containerRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(containerRef.current,
      { opacity: 0, y: 50, scale: 0.95 },
      { opacity: 1, y: 0, scale: 1, duration: 0.8, ease: 'power3.out' }
    );
  }, []);

  const handleSignup = (e) => {
    e.preventDefault();
    // Placeholder for actual signup logic/API call
    setCurrentPage('login');
  };

  return (
    <div ref={containerRef} className="min-h-screen max-w-md mx-auto px-6 py-20">
      <div className="glass p-12 rounded-2xl space-y-8 border border-white/10 text-center">
        <h2 className="text-4xl font-black gradient-text">{t('signup', 'title')}</h2>
        <p className="text-gray-400">{t('signup', 'subtitle')}</p>
        
        <form onSubmit={handleSignup} className="space-y-5 text-left">
          <div>
            <label className="block text-sm text-gray-400 mb-2">{t('signup', 'name')}</label>
            <input 
              type="text"
              placeholder={t('signup', 'name_ph')}
              required
              className="w-full glass rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">{t('signup', 'email')}</label>
            <input 
              type="email"
              placeholder={t('signup', 'email_ph')}
              required
              className="w-full glass rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">{t('signup', 'password')}</label>
            <input 
              type="password"
              placeholder="••••••••"
              required
              className="w-full glass rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-2">{t('signup', 'confirm')}</label>
            <input 
              type="password"
              placeholder="••••••••"
              required
              className="w-full glass rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
            />
          </div>
          
          <button
            type="submit"
            className="w-full px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-xl font-bold text-white shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/80 transition-all hover:scale-105 active:scale-95"
          >
            {t('signup', 'signup_btn')}
          </button>
        </form>

        <p className="text-sm text-gray-400">
          {t('signup', 'have_account')}{' '}
          <button onClick={() => setCurrentPage('login')} className="font-bold text-cyan-400 hover:underline">{t('signup', 'login')}</button>
        </p>
      </div>
    </div>
  );
}

function MedicinePage() {
  const { t } = useContext(LanguageContext);
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
          <h2 className="text-5xl font-black gradient-text">🔬 {t('medicine', 'title')}</h2>
          <p className="text-gray-400 text-lg">{t('medicine', 'subtitle')}</p>
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
                <h3 className="text-xl font-bold mb-2">{t('medicine', 'upload')}</h3>
                <p className="text-gray-400">{t('medicine', 'format')}</p>
                <p className="text-sm text-gray-500 mt-2">{t('medicine', 'drag')}</p>
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
                      ✕ {t('medicine', 'clear')}
                    </button>
                  </div>
                </div>

                <button 
                  onClick={handleVerify}
                  disabled={loading}
                  className="w-full px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl font-bold text-white shadow-lg shadow-purple-500/50 hover:shadow-purple-500/80 transition-all hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? `🔄 ${t('medicine', 'verifying')}` : `🔐 ${t('medicine', 'verify')}`}
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
  const { t } = useContext(LanguageContext);
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
          <h2 className="text-2xl font-bold gradient-text">{t('chat', 'title')}</h2>
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
            placeholder={t('chat', 'ph')}
            className="flex-1 glass rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-cyan-500 transition-all"
          />
          <button
            onClick={handleSend}
            className="px-6 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg font-bold hover:shadow-lg hover:shadow-cyan-500/50 transition-all hover:scale-105 active:scale-95"
          >
            {t('chat', 'btn')}
          </button>
        </div>
      </div>
    </div>
  );
}

function HistoryPage() {
  const { t } = useContext(LanguageContext);
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
          ← {t('history', 'back')}
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
        <h2 className="text-5xl font-black gradient-text">📋 {t('history', 'title')}</h2>
        
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
            🩺 {t('history', 'symp_tab')} ({symptomHistory.length})
          </button>
          <button
            onClick={() => setActiveTab('medicine')}
            className={`px-6 py-3 rounded-lg font-bold transition-all ${
              activeTab === 'medicine'
                ? 'bg-cyan-500/30 border border-cyan-500'
                : 'bg-white/5 border border-white/10 hover:bg-white/10'
            }`}
          >
            💊 {t('history', 'med_tab')} ({medicineHistory.length})
          </button>
        </div>

        {loading ? (
          <div className="text-center py-8">
            <p className="text-gray-400">{t('history', 'loading')}</p>
          </div>
        ) : items.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-400">{t('history', 'empty')}</p>
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
