import { useEffect, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    ArcElement,
} from 'chart.js'
import { Radar, Bar, Doughnut } from 'react-chartjs-2'
import toast from 'react-hot-toast'
import { useApp } from '../hooks/useAppContext'

ChartJS.register(
    RadialLinearScale, PointElement, LineElement, Filler,
    Tooltip, Legend, CategoryScale, LinearScale, BarElement, ArcElement
)

const GRADE_CONFIG = {
    A: { color: '#10b981', label: 'Excellent', emoji: '🏆', glow: 'rgba(16,185,129,0.35)' },
    B: { color: '#22d3ee', label: 'Good', emoji: '🎯', glow: 'rgba(34,211,238,0.3)' },
    C: { color: '#fbbf24', label: 'Fair', emoji: '📈', glow: 'rgba(251,191,36,0.3)' },
    D: { color: '#f97316', label: 'Weak', emoji: '💪', glow: 'rgba(249,115,22,0.3)' },
    F: { color: '#fb7185', label: 'Poor', emoji: '🛠️', glow: 'rgba(251,113,133,0.3)' },
}

export default function ResultPage() {
    const navigate = useNavigate()
    const { matchResult, resumeData, selectedJob } = useApp()

    useEffect(() => {
        if (!matchResult) { toast.error('No results yet — run an analysis first'); navigate('/jobs') }
    }, [matchResult, navigate])

    if (!matchResult) return null

    const { score, grade, matched_skills, missing_skills, roadmap } = matchResult
    const gradeConf = GRADE_CONFIG[grade] || GRADE_CONFIG['F']
    const totalRequired = (matched_skills?.length || 0) + (missing_skills?.length || 0)

    /* ── Chart data ─────────────────────────────────────────────────── */
    const doughnutData = {
        labels: ['Matched Skills', 'Missing Skills'],
        datasets: [{
            data: [matched_skills?.length || 0, missing_skills?.length || 0],
            backgroundColor: ['rgba(16,185,129,0.8)', 'rgba(251,113,133,0.7)'],
            borderColor: ['#10b981', '#fb7185'],
            borderWidth: 2,
        }],
    }

    const radarSkills = [...(matched_skills || []).slice(0, 6), ...(missing_skills || []).slice(0, 3)]
    const radarScores = radarSkills.map(s =>
        matched_skills?.includes(s) ? Math.round(70 + Math.random() * 30) : Math.round(10 + Math.random() * 25)
    )
    const radarData = {
        labels: radarSkills.length > 0 ? radarSkills : ['No Data'],
        datasets: [{
            label: 'Skill Proficiency',
            data: radarSkills.length > 0 ? radarScores : [0],
            backgroundColor: 'rgba(139,92,246,0.2)',
            borderColor: '#8b5cf6',
            pointBackgroundColor: '#a78bfa',
            borderWidth: 2,
        }],
    }

    const barData = {
        labels: ['Match Score', 'Matched Skills %', 'Skill Coverage'],
        datasets: [{
            label: 'Your Performance',
            data: [
                score,
                totalRequired ? Math.round((matched_skills?.length / totalRequired) * 100) : 0,
                totalRequired ? Math.round(((matched_skills?.length || 0) / (totalRequired || 1)) * 100) : 0,
            ],
            backgroundColor: ['rgba(139,92,246,0.7)', 'rgba(34,211,238,0.7)', 'rgba(16,185,129,0.7)'],
            borderColor: ['#8b5cf6', '#22d3ee', '#10b981'],
            borderWidth: 1, borderRadius: 8,
        }],
    }

    const chartOpts = { responsive: true, plugins: { legend: { labels: { color: '#94a3b8', font: { family: 'Inter' } } } } }
    const radarOpts = { ...chartOpts, scales: { r: { grid: { color: 'rgba(255,255,255,0.06)' }, pointLabels: { color: '#94a3b8', font: { size: 11 } }, ticks: { display: false }, angleLines: { color: 'rgba(255,255,255,0.06)' } } } }
    const barOpts = { ...chartOpts, scales: { x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94a3b8' } }, y: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#94a3b8' }, max: 100 } } }

    return (
        <div className="container" style={{ padding: '48px 24px', maxWidth: 1100 }}>

            {/* Header */}
            <div className="animate-fade-in-up" style={{ marginBottom: 40 }}>
                <h1 style={{ fontSize: 'clamp(1.8rem,4vw,2.4rem)', marginBottom: 8 }}>
                    Match <span className="gradient-text">Results</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)' }}>
                    {selectedJob?.title} • {matched_skills?.length} skills matched • {missing_skills?.length} gaps found
                </p>
            </div>

            {/* ── Score Hero ──────────────────────────────────────────────────── */}
            <div className="animate-fade-in-up delay-100" style={{
                background: `linear-gradient(135deg, rgba(${gradeConf.color === '#10b981' ? '16,185,129' : gradeConf.color === '#22d3ee' ? '34,211,238' : gradeConf.color === '#fbbf24' ? '251,191,36' : gradeConf.color === '#f97316' ? '249,115,22' : '251,113,133'},0.12), rgba(124,58,237,0.08))`,
                border: `1px solid ${gradeConf.color}40`,
                borderRadius: 'var(--radius-xl)',
                padding: '36px 40px',
                marginBottom: 28,
                display: 'flex', alignItems: 'center', gap: 40, flexWrap: 'wrap',
            }}>
                {/* Score ring SVG */}
                <div style={{ position: 'relative', width: 140, height: 140, flexShrink: 0 }}>
                    <svg viewBox="0 0 120 120" style={{ transform: 'rotate(-90deg)', width: '100%', height: '100%' }}>
                        <circle cx="60" cy="60" r="50" fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="10" />
                        <circle cx="60" cy="60" r="50" fill="none"
                            stroke={gradeConf.color} strokeWidth="10"
                            strokeDasharray={`${(score / 100) * 314} 314`}
                            strokeLinecap="round"
                            style={{ filter: `drop-shadow(0 0 8px ${gradeConf.color})`, transition: 'stroke-dasharray 1.2s ease' }}
                        />
                    </svg>
                    <div style={{
                        position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
                        alignItems: 'center', justifyContent: 'center',
                    }}>
                        <span style={{ fontSize: '1.9rem', fontWeight: 900, fontFamily: 'Outfit,sans-serif', color: gradeConf.color }}>{score}</span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>/100</span>
                    </div>
                </div>

                <div style={{ flex: 1, minWidth: 200 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 12 }}>
                        <span style={{ fontSize: '2.5rem' }}>{gradeConf.emoji}</span>
                        <div>
                            <div style={{ fontFamily: 'Outfit,sans-serif', fontWeight: 800, fontSize: '1.6rem', color: gradeConf.color }}>
                                Grade {grade}
                            </div>
                            <div style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>{gradeConf.label} match</div>
                        </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
                        {[
                            { label: 'Matched', value: matched_skills?.length || 0, color: '#10b981' },
                            { label: 'Missing', value: missing_skills?.length || 0, color: '#fb7185' },
                            { label: 'Roadmap Weeks', value: roadmap?.length || 0, color: '#8b5cf6' },
                        ].map(m => (
                            <div key={m.label} style={{
                                background: 'rgba(255,255,255,0.04)', borderRadius: 'var(--radius-md)',
                                padding: '10px 14px', textAlign: 'center',
                            }}>
                                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: m.color, fontFamily: 'Outfit,sans-serif' }}>{m.value}</div>
                                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{m.label}</div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Overall progress bar */}
                <div style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                        <span>Overall Match Score</span><span style={{ color: gradeConf.color, fontWeight: 700 }}>{score}%</span>
                    </div>
                    <div className="progress-bar" style={{ height: 10 }}>
                        <div className="progress-fill" style={{ width: `${score}%`, background: `linear-gradient(90deg, ${gradeConf.color}, ${gradeConf.color}aa)` }} />
                    </div>
                </div>
            </div>

            {/* ── Charts Row ───────────────────────────────────────────────────────── */}
            <div className="animate-fade-in-up delay-200" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 20, marginBottom: 28 }}>
                <div className="card" style={{ minHeight: 280 }}>
                    <h3 style={{ fontSize: '0.95rem', marginBottom: 20, color: 'var(--text-secondary)' }}>📊 Skill Coverage</h3>
                    <Doughnut data={doughnutData} options={{ ...chartOpts, cutout: '65%' }} />
                </div>
                <div className="card" style={{ minHeight: 280 }}>
                    <h3 style={{ fontSize: '0.95rem', marginBottom: 20, color: 'var(--text-secondary)' }}>🕸️ Skill Radar</h3>
                    <Radar data={radarData} options={radarOpts} />
                </div>
                <div className="card" style={{ minHeight: 280 }}>
                    <h3 style={{ fontSize: '0.95rem', marginBottom: 20, color: 'var(--text-secondary)' }}>📈 Performance</h3>
                    <Bar data={barData} options={barOpts} />
                </div>
            </div>

            {/* ── Skill lists ──────────────────────────────────────────────────────── */}
            <div className="animate-fade-in-up delay-300" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 20, marginBottom: 28 }}>
                {/* Matched */}
                <div className="card">
                    <h3 style={{ fontSize: '1rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ color: '#10b981' }}>✓</span> Matched Skills
                        <span className="badge badge-green" style={{ marginLeft: 'auto' }}>{matched_skills?.length}</span>
                    </h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {(matched_skills || []).length === 0
                            ? <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>No matched skills</p>
                            : matched_skills.map(s => <span key={s} className="badge badge-green">{s}</span>)
                        }
                    </div>
                </div>

                {/* Missing */}
                <div className="card">
                    <h3 style={{ fontSize: '1rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ color: '#fb7185' }}>✗</span> Skill Gaps
                        <span className="badge badge-red" style={{ marginLeft: 'auto' }}>{missing_skills?.length}</span>
                    </h3>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {(missing_skills || []).length === 0
                            ? <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>🎉 No gaps! You're fully qualified.</p>
                            : missing_skills.map(s => <span key={s} className="badge badge-red">{s}</span>)
                        }
                    </div>
                </div>
            </div>

            {/* ── Action buttons ───────────────────────────────────────────────────── */}
            <div className="animate-fade-in-up delay-400" style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
                <Link to="/roadmap" id="view-roadmap-btn" className="btn btn-primary btn-lg" style={{ flex: '1 1 200px', textAlign: 'center' }}>
                    🗺️ View Learning Roadmap
                </Link>
                <Link to="/upload" className="btn btn-outline btn-lg" style={{ flex: '1 1 150px', textAlign: 'center' }}>
                    ↑ New Resume
                </Link>
                <Link to="/jobs" className="btn btn-secondary btn-lg" style={{ flex: '1 1 150px', textAlign: 'center' }}>
                    ← Change Job
                </Link>
            </div>
        </div>
    )
}
