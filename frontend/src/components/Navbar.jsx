import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useApp } from '../hooks/useAppContext'

const STEPS = [
    { path: '/upload', label: 'Upload Resume', num: 1 },
    { path: '/jobs', label: 'Select Job', num: 2 },
    { path: '/results', label: 'Results', num: 3 },
    { path: '/roadmap', label: 'Roadmap', num: 4 },
]

export default function Navbar() {
    const location = useLocation()
    const { resumeData, selectedJob } = useApp()
    const [scrolled, setScrolled] = useState(false)

    useEffect(() => {
        const fn = () => setScrolled(window.scrollY > 20)
        window.addEventListener('scroll', fn)
        return () => window.removeEventListener('scroll', fn)
    }, [])

    const isLanding = location.pathname === '/'

    const currentStep = STEPS.findIndex(s => s.path === location.pathname) + 1

    return (
        <nav style={{
            position: 'sticky', top: 0, zIndex: 50,
            background: scrolled ? 'rgba(8,12,20,0.95)' : 'rgba(8,12,20,0.7)',
            backdropFilter: 'blur(20px)',
            borderBottom: '1px solid rgba(139,92,246,0.12)',
            transition: 'all 0.3s',
        }}>
            <div className="container" style={{
                display: 'flex', alignItems: 'center',
                justifyContent: 'space-between', height: 64,
            }}>
                {/* Logo */}
                <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10 }}>
                    <div style={{
                        width: 36, height: 36,
                        background: 'linear-gradient(135deg, #7c3aed, #06b6d4)',
                        borderRadius: 10,
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 18, fontWeight: 900,
                    }}>⚡</div>
                    <span style={{ fontFamily: 'Outfit,sans-serif', fontWeight: 800, fontSize: '1.15rem' }}>
                        Skill<span className="gradient-text">Match</span> AI
                    </span>
                </Link>

                {/* Step indicators — only on app pages */}
                {!isLanding && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
                        {STEPS.map((step, i) => {
                            const done = currentStep > step.num
                            const active = location.pathname === step.path
                            const canNav = step.num === 1 || (step.num === 2 && resumeData) || (step.num === 3 && selectedJob) || (step.num === 4 && selectedJob)

                            return (
                                <div key={step.path} style={{ display: 'flex', alignItems: 'center' }}>
                                    <Link
                                        to={canNav ? step.path : '#'}
                                        title={step.label}
                                        style={{ textDecoration: 'none' }}
                                        onClick={e => !canNav && e.preventDefault()}
                                    >
                                        <div style={{
                                            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2,
                                        }}>
                                            <div style={{
                                                width: 32, height: 32, borderRadius: '50%',
                                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                                fontSize: '0.78rem', fontWeight: 700,
                                                background: done ? '#10b981' : active
                                                    ? 'linear-gradient(135deg, #7c3aed, #8b5cf6)'
                                                    : 'rgba(255,255,255,0.05)',
                                                color: (done || active) ? 'white' : '#475569',
                                                border: active ? 'none' : `1px solid ${done ? '#10b981' : 'rgba(139,92,246,0.2)'}`,
                                                boxShadow: active ? '0 0 16px rgba(139,92,246,0.5)' : 'none',
                                                transition: 'all 0.3s',
                                                cursor: canNav ? 'pointer' : 'not-allowed',
                                                opacity: canNav ? 1 : 0.4,
                                            }}>
                                                {done ? '✓' : step.num}
                                            </div>
                                            <span style={{
                                                fontSize: '0.65rem', fontWeight: 600, letterSpacing: '0.03em',
                                                color: active ? '#a78bfa' : '#475569',
                                                display: window.innerWidth < 640 ? 'none' : 'block',
                                            }}>{step.label}</span>
                                        </div>
                                    </Link>
                                    {i < STEPS.length - 1 && (
                                        <div style={{
                                            width: 40, height: 2, margin: '0 4px', marginBottom: 14,
                                            background: done ? '#10b981' : 'rgba(139,92,246,0.15)',
                                            transition: 'background 0.5s',
                                        }} />
                                    )}
                                </div>
                            )
                        })}
                    </div>
                )}

                {/* CTA */}
                <Link to="/upload" className="btn btn-primary btn-sm">
                    {isLanding ? 'Get Started' : 'New Analysis'}
                </Link>
            </div>
        </nav>
    )
}
