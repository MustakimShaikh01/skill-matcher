import { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useApp } from '../hooks/useAppContext'

const LEVEL_STYLES = {
    beginner: { badge: 'badge-green', icon: '🌱', bar: '#10b981' },
    intermediate: { badge: 'badge-amber', icon: '🔥', bar: '#fbbf24' },
    advanced: { badge: 'badge-red', icon: '⚡', bar: '#fb7185' },
}

export default function RoadmapPage() {
    const navigate = useNavigate()
    const { matchResult, selectedJob } = useApp()

    useEffect(() => {
        if (!matchResult) { toast.error('Run an analysis first'); navigate('/jobs') }
    }, [matchResult, navigate])

    if (!matchResult) return null

    const { roadmap = [], score, grade, missing_skills = [], matched_skills = [] } = matchResult
    const totalWeeks = roadmap.length

    return (
        <div className="container" style={{ padding: '48px 24px', maxWidth: 900 }}>

            {/* Header */}
            <div className="animate-fade-in-up" style={{ marginBottom: 16 }}>
                <h1 style={{ fontSize: 'clamp(1.8rem,4vw,2.4rem)', marginBottom: 8 }}>
                    Your Learning <span className="gradient-text">Roadmap</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)' }}>
                    {selectedJob?.title} • {totalWeeks}-week dependency-ordered learning plan
                </p>
            </div>

            {/* Summary Bar */}
            <div className="animate-fade-in-up delay-100 card" style={{
                marginBottom: 36,
                background: 'linear-gradient(135deg, rgba(124,58,237,0.12), rgba(6,182,212,0.06))',
                display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 20, padding: '20px 28px',
            }}>
                {[
                    { label: 'Match Score', value: `${score}/100`, color: '#8b5cf6' },
                    { label: 'Grade', value: grade, color: '#22d3ee' },
                    { label: 'Skills to Learn', value: totalWeeks, color: '#fb7185' },
                    { label: 'Already Have', value: matched_skills.length, color: '#10b981' },
                ].map(s => (
                    <div key={s.label} style={{ textAlign: 'center' }}>
                        <div style={{ fontSize: '1.7rem', fontWeight: 900, fontFamily: 'Outfit,sans-serif', color: s.color }}>{s.value}</div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 4 }}>{s.label}</div>
                    </div>
                ))}
            </div>

            {totalWeeks === 0 ? (
                <div className="card animate-fade-in" style={{ textAlign: 'center', padding: '60px 40px' }}>
                    <div style={{ fontSize: '4rem', marginBottom: 16 }}>🎉</div>
                    <h2 style={{ marginBottom: 12 }}>You're fully qualified!</h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>
                        No skill gaps detected. Your resume is a strong match for {selectedJob?.title}.
                    </p>
                    <Link to="/upload" className="btn btn-primary">Analyse Another Resume</Link>
                </div>
            ) : (
                <>
                    {/* Timeline */}
                    <div style={{ position: 'relative' }}>
                        {/* Vertical line */}
                        <div style={{
                            position: 'absolute', left: 19, top: 0, bottom: 0, width: 2,
                            background: 'linear-gradient(180deg, var(--purple-600), var(--cyan-500), transparent)',
                            zIndex: 0,
                        }} />

                        <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
                            {roadmap.map((item, i) => {
                                const lvl = LEVEL_STYLES[item.level] || LEVEL_STYLES.beginner
                                return (
                                    <RoadmapItem key={item.week} item={item} lvl={lvl} i={i} total={totalWeeks} />
                                )
                            })}
                        </div>
                    </div>

                    {/* Total duration pill */}
                    <div className="animate-fade-in-up" style={{
                        marginTop: 40, textAlign: 'center',
                        background: 'rgba(139,92,246,0.1)', border: '1px solid rgba(139,92,246,0.25)',
                        borderRadius: 'var(--radius-xl)', padding: '20px 32px',
                    }}>
                        <p style={{ color: 'var(--text-secondary)', marginBottom: 6, fontSize: '0.9rem' }}>Estimated total learning time</p>
                        <p style={{ fontFamily: 'Outfit,sans-serif', fontWeight: 800, fontSize: '1.5rem' }} className="gradient-text">
                            {totalWeeks} Week{totalWeeks !== 1 ? 's' : ''} • ~{totalWeeks * 5}–{totalWeeks * 10} hours
                        </p>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: 8 }}>
                            All resources are 100% free. Beginner skills first, advanced last.
                        </p>
                    </div>
                </>
            )}

            {/* Action buttons */}
            <div style={{ display: 'flex', gap: 12, marginTop: 32, flexWrap: 'wrap' }}>
                <Link to="/results" className="btn btn-secondary" style={{ flex: '1 1 140px', textAlign: 'center' }}>
                    ← Back to Results
                </Link>
                <Link to="/upload" className="btn btn-outline" style={{ flex: '1 1 140px', textAlign: 'center' }}>
                    New Analysis
                </Link>
                <button id="print-roadmap-btn" onClick={() => window.print()} className="btn btn-primary" style={{ flex: '1 1 160px' }}>
                    🖨️ Print / Save PDF
                </button>
            </div>
        </div>
    )
}

function RoadmapItem({ item, lvl, i, total }) {
    const isLast = i === total - 1

    return (
        <div className={`animate-fade-in-up delay-${Math.min(i * 100, 500)}`}
            style={{ display: 'flex', gap: 16, paddingBottom: isLast ? 0 : 28, position: 'relative', zIndex: 1 }}>

            {/* Dot */}
            <div style={{
                width: 40, height: 40, borderRadius: '50%', flexShrink: 0,
                background: `linear-gradient(135deg, ${lvl.bar}, ${lvl.bar}88)`,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '1.1rem', boxShadow: `0 0 16px ${lvl.bar}55`,
                border: `2px solid ${lvl.bar}60`,
                zIndex: 2, position: 'relative',
            }}>{lvl.icon}</div>

            {/* Card */}
            <div className="card" style={{ flex: 1, padding: '20px 24px' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8, marginBottom: 10 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)' }}>WEEK {item.week}</span>
                        <h3 style={{ fontSize: '1.05rem', fontFamily: 'Outfit,sans-serif' }}>{item.skill}</h3>
                    </div>
                    <span className={`badge ${lvl.badge}`} style={{ textTransform: 'capitalize' }}>{item.level}</span>
                </div>

                <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6, marginBottom: 14 }}>
                    {item.description}
                </p>

                {/* Resources */}
                {item.resources?.length > 0 && (
                    <div>
                        <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 8 }}>
                            Free Resources
                        </p>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                            {item.resources.map((url, ri) => {
                                let domain = ''
                                try { domain = new URL(url).hostname.replace('www.', '') } catch { }
                                return (
                                    <a
                                        key={ri}
                                        href={url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        style={{
                                            display: 'flex', alignItems: 'center', gap: 8,
                                            padding: '8px 12px', borderRadius: 8,
                                            background: 'rgba(139,92,246,0.08)',
                                            border: '1px solid rgba(139,92,246,0.18)',
                                            color: 'var(--purple-400)',
                                            fontSize: '0.82rem', fontWeight: 500,
                                            textDecoration: 'none', transition: 'all 0.2s',
                                        }}
                                        onMouseEnter={e => { e.target.style.background = 'rgba(139,92,246,0.15)'; e.target.style.borderColor = 'rgba(139,92,246,0.4)' }}
                                        onMouseLeave={e => { e.target.style.background = 'rgba(139,92,246,0.08)'; e.target.style.borderColor = 'rgba(139,92,246,0.18)' }}
                                    >
                                        <span>🔗</span>
                                        <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{domain}</span>
                                        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>↗</span>
                                    </a>
                                )
                            })}
                        </div>
                    </div>
                )}
            </div>
        </div>
    )
}
