import { Link } from 'react-router-dom'

const FEATURES = [
    { icon: '🧠', title: 'NLP Resume Parsing', desc: 'spaCy + Trie-based extraction pulls skills, experience, education and projects from any PDF or DOCX.' },
    { icon: '📊', title: 'TF-IDF Matching', desc: 'Cosine similarity on TF-IDF vectors gives a semantic match score — beyond simple keyword counting.' },
    { icon: '🔗', title: 'Skill Dependency Graph', desc: 'BFS & DFS on a directed graph surfaces prerequisite chains so you learn skills in the right order.' },
    { icon: '🗺️', title: 'Weekly Roadmap', desc: 'Topologically sorted learning plan with curated free resources per missing skill.' },
    { icon: '⚡', title: 'Trie-Based Lookup', desc: 'O(L) prefix search with fuzzy matching normalises 100+ known skills instantly.' },
    { icon: '📈', title: 'Visual Dashboard', desc: 'Radar charts, progress rings and bar charts make insights immediately actionable.' },
]

const STATS = [
    { value: '100+', label: 'Known Skills' },
    { value: '<2s', label: 'Analysis Time' },
    { value: '3', label: 'DSA Modules' },
    { value: '6+', label: 'Sample Jobs' },
]

export default function LandingPage() {
    return (
        <div style={{ overflow: 'hidden' }}>

            {/* ── Hero ─────────────────────────────────────────────────────────── */}
            <section style={{ position: 'relative', padding: '100px 0 80px', textAlign: 'center', overflow: 'hidden' }}>
                {/* Glow orbs */}
                <div className="glow-orb glow-orb-purple" style={{ width: 600, height: 600, top: -200, left: '50%', transform: 'translateX(-60%)' }} />
                <div className="glow-orb glow-orb-cyan" style={{ width: 400, height: 400, top: 100, right: '5%' }} />

                <div className="container" style={{ position: 'relative', zIndex: 1 }}>
                    <div className="animate-fade-in-up">
                        <span className="badge badge-purple" style={{ marginBottom: 20, fontSize: '0.8rem' }}>
                            🚀 Placement-Grade AI Platform
                        </span>
                    </div>

                    <h1 className="animate-fade-in-up delay-100" style={{ fontSize: 'clamp(2.5rem, 6vw, 4.5rem)', fontWeight: 900, marginBottom: 24, lineHeight: 1.1 }}>
                        Match Your Resume to{' '}
                        <span className="gradient-text">Any Job</span><br />
                        <span style={{ color: 'var(--text-secondary)', fontWeight: 600, fontSize: '0.7em' }}>
                            Powered by NLP + DSA + ML
                        </span>
                    </h1>

                    <p className="animate-fade-in-up delay-200" style={{
                        fontSize: '1.15rem', color: 'var(--text-secondary)',
                        maxWidth: 620, margin: '0 auto 40px', lineHeight: 1.7,
                    }}>
                        Upload your resume, select a job role, and get an AI-driven match score,
                        skill gap analysis, and a personalised weekly learning roadmap — all in seconds.
                    </p>

                    <div className="animate-fade-in-up delay-300" style={{ display: 'flex', gap: 16, justifyContent: 'center', flexWrap: 'wrap' }}>
                        <Link to="/upload" className="btn btn-primary btn-lg animate-pulse-glow">
                            ⚡ Analyse My Resume
                        </Link>
                        <a href="#features" className="btn btn-outline btn-lg">
                            See How It Works
                        </a>
                    </div>

                    {/* Stats */}
                    <div className="animate-fade-in-up delay-400" style={{
                        display: 'flex', gap: 40, justifyContent: 'center', marginTop: 64, flexWrap: 'wrap',
                    }}>
                        {STATS.map(s => (
                            <div key={s.label} style={{ textAlign: 'center' }}>
                                <div style={{ fontSize: '2rem', fontWeight: 800, fontFamily: 'Outfit,sans-serif' }} className="gradient-text">{s.value}</div>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>{s.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── Architecture visual ───────────────────────────────────────────── */}
            <section style={{ padding: '40px 0 80px' }}>
                <div className="container">
                    <div style={{
                        background: 'linear-gradient(135deg, rgba(124,58,237,0.08), rgba(6,182,212,0.06))',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-xl)',
                        padding: '40px 48px',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', flexWrap: 'wrap', gap: 8,
                    }}>
                        {['PDF / DOCX', '→', 'NLP Parser', '→', 'Skill Trie', '→', 'TF-IDF Matcher', '→', 'Skill Graph (BFS/DFS)', '→', 'Roadmap Generator'].map((node, i) => (
                            <div key={i} style={{
                                padding: node === '→' ? '0 4px' : '10px 18px',
                                borderRadius: 10,
                                background: node === '→' ? 'transparent' : 'rgba(139,92,246,0.12)',
                                border: node === '→' ? 'none' : '1px solid rgba(139,92,246,0.25)',
                                color: node === '→' ? 'var(--text-muted)' : 'var(--purple-400)',
                                fontWeight: node === '→' ? 400 : 600,
                                fontSize: '0.85rem',
                                fontFamily: node === '→' ? 'inherit' : 'Outfit,sans-serif',
                            }}>
                                {node}
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── Features ─────────────────────────────────────────────────────── */}
            <section id="features" style={{ padding: '40px 0 100px' }}>
                <div className="container">
                    <div style={{ textAlign: 'center', marginBottom: 60 }}>
                        <h2 style={{ fontSize: 'clamp(1.8rem,4vw,2.5rem)', marginBottom: 16 }}>
                            What Makes <span className="gradient-text">SkillMatch AI</span> Different
                        </h2>
                        <p style={{ color: 'var(--text-secondary)', maxWidth: 500, margin: '0 auto' }}>
                            A production-grade system built with real NLP, DSA, and ML — not just keyword matching.
                        </p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: 24 }}>
                        {FEATURES.map((f, i) => (
                            <div key={f.title} className={`card animate-fade-in-up delay-${(i % 5 + 1) * 100}`}
                                style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                                <div style={{
                                    width: 48, height: 48,
                                    background: 'linear-gradient(135deg, rgba(124,58,237,0.2), rgba(6,182,212,0.1))',
                                    borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    fontSize: '1.4rem',
                                }}>{f.icon}</div>
                                <h3 style={{ fontSize: '1.05rem', fontFamily: 'Outfit,sans-serif' }}>{f.title}</h3>
                                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6 }}>{f.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ── CTA Banner ───────────────────────────────────────────────────── */}
            <section style={{ padding: '0 0 100px' }}>
                <div className="container">
                    <div style={{
                        background: 'linear-gradient(135deg, rgba(124,58,237,0.25) 0%, rgba(6,182,212,0.15) 100%)',
                        border: '1px solid rgba(139,92,246,0.3)',
                        borderRadius: 'var(--radius-2xl)',
                        padding: '60px 48px', textAlign: 'center',
                        position: 'relative', overflow: 'hidden',
                    }}>
                        <div className="glow-orb glow-orb-purple" style={{ width: 400, height: 400, top: -100, left: '50%', transform: 'translateX(-50%)' }} />
                        <div style={{ position: 'relative', zIndex: 1 }}>
                            <h2 style={{ fontSize: 'clamp(1.6rem,4vw,2.2rem)', marginBottom: 16 }}>
                                Ready to land your dream job?
                            </h2>
                            <p style={{ color: 'var(--text-secondary)', marginBottom: 32, fontSize: '1rem' }}>
                                Upload your resume in seconds and get your personalised roadmap.
                            </p>
                            <Link to="/upload" className="btn btn-primary btn-lg">
                                🎯 Start Matching Now
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    )
}
