import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { listJobs, matchResumeToJob } from '../utils/api'
import { useApp } from '../hooks/useAppContext'

const LEVEL_COLOR = { beginner: 'badge-green', intermediate: 'badge-amber', advanced: 'badge-red' }

export default function JobsPage() {
    const navigate = useNavigate()
    const { resumeData, setSelectedJob, setMatchResult } = useApp()
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [matching, setMatching] = useState(false)
    const [selected, setSelected] = useState(null)
    const [search, setSearch] = useState('')

    useEffect(() => {
        listJobs()
            .then(r => setJobs(r.data))
            .catch(() => toast.error('Could not load jobs — is the backend running?'))
            .finally(() => setLoading(false))
    }, [])

    // Redirect if no resume
    useEffect(() => {
        if (!resumeData) { toast.error('Please upload a resume first'); navigate('/upload') }
    }, [resumeData, navigate])

    const filtered = jobs.filter(j =>
        j.title.toLowerCase().includes(search.toLowerCase()) ||
        j.description.toLowerCase().includes(search.toLowerCase()) ||
        j.required_skills?.some(s => s.toLowerCase().includes(search.toLowerCase()))
    )

    const handleMatch = async () => {
        if (!selected) { toast.error('Select a job first'); return }
        setMatching(true)
        try {
            const { data } = await matchResumeToJob(resumeData.resume_id, selected.job_id)
            setSelectedJob(selected)
            setMatchResult(data)
            toast.success('Analysis complete! 🎯')
            navigate('/results')
        } catch (err) {
            toast.error(err.response?.data?.detail || 'Matching failed')
        } finally { setMatching(false) }
    }

    return (
        <div className="container" style={{ padding: '48px 24px', maxWidth: 900 }}>
            {/* Header */}
            <div className="animate-fade-in-up" style={{ marginBottom: 32 }}>
                <h1 style={{ fontSize: 'clamp(1.8rem,4vw,2.4rem)', marginBottom: 12 }}>
                    Select a <span className="gradient-text">Job Role</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)' }}>
                    Pick the position you're targeting. We'll analyse your resume against it.
                </p>
                {resumeData && (
                    <div style={{ marginTop: 12, display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Resume loaded with</span>
                        <span className="badge badge-purple">{resumeData.skills?.length || 0} skills</span>
                        <span className="badge badge-cyan">{resumeData.experience || 0} yrs exp</span>
                    </div>
                )}
            </div>

            {/* Search */}
            <div className="animate-fade-in-up delay-100" style={{ marginBottom: 24 }}>
                <input
                    id="job-search-input"
                    className="input"
                    placeholder="🔍  Search jobs by title, skill, or description…"
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                />
            </div>

            {/* Jobs Grid */}
            {loading ? (
                <div style={{ display: 'grid', gap: 16 }}>
                    {[1, 2, 3].map(i => (
                        <div key={i} className="card" style={{ height: 140 }}>
                            <div className="skeleton" style={{ height: 20, width: '40%', marginBottom: 12 }} />
                            <div className="skeleton" style={{ height: 14, width: '90%', marginBottom: 8 }} />
                            <div className="skeleton" style={{ height: 14, width: '70%' }} />
                        </div>
                    ))}
                </div>
            ) : (
                <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
                    {filtered.length === 0 ? (
                        <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
                            No jobs match your search. <button className="btn btn-sm btn-secondary" onClick={() => setSearch('')} style={{ marginLeft: 8 }}>Clear</button>
                        </div>
                    ) : filtered.map((job, i) => (
                        <JobCard
                            key={job.job_id}
                            job={job}
                            selected={selected?.job_id === job.job_id}
                            resumeSkills={resumeData?.skills || []}
                            onSelect={() => setSelected(selected?.job_id === job.job_id ? null : job)}
                            delay={i * 50}
                        />
                    ))}
                </div>
            )}

            {/* Match CTA */}
            {selected && (
                <div className="animate-fade-in" style={{
                    position: 'sticky', bottom: 24, marginTop: 32,
                    background: 'rgba(8,12,20,0.95)', backdropFilter: 'blur(20px)',
                    border: '1px solid rgba(139,92,246,0.3)',
                    borderRadius: 'var(--radius-xl)', padding: '16px 24px',
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12,
                }}>
                    <div>
                        <p style={{ fontWeight: 700 }}>Selected: {selected.title}</p>
                        <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{selected.required_skills?.length} required skills</p>
                    </div>
                    <button id="run-match-btn" onClick={handleMatch} disabled={matching} className="btn btn-primary btn-lg">
                        {matching
                            ? <><span className="animate-spin-slow" style={{ display: 'inline-block' }}>⟳</span>&nbsp;Analysing…</>
                            : '🎯 Run AI Analysis'
                        }
                    </button>
                </div>
            )}
        </div>
    )
}

function JobCard({ job, selected, resumeSkills, onSelect, delay }) {
    const resumeSkillsLower = resumeSkills.map(s => s.toLowerCase())
    const matched = job.required_skills?.filter(s => resumeSkillsLower.includes(s.toLowerCase())) || []
    const overlap = job.required_skills?.length
        ? Math.round((matched.length / job.required_skills.length) * 100)
        : 0

    return (
        <div
            id={`job-card-${job.job_id}`}
            className="card animate-fade-in-up"
            onClick={onSelect}
            style={{
                cursor: 'pointer',
                border: `1px solid ${selected ? 'var(--purple-500)' : 'var(--border)'}`,
                background: selected ? 'rgba(124,58,237,0.08)' : 'var(--bg-card)',
                boxShadow: selected ? 'var(--shadow-glow-purple)' : 'none',
                animationDelay: `${delay}ms`,
                transition: 'all 0.2s',
            }}
        >
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 12, marginBottom: 12 }}>
                <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                    <div style={{
                        width: 40, height: 40, borderRadius: 10,
                        background: 'linear-gradient(135deg, rgba(124,58,237,0.3), rgba(6,182,212,0.2))',
                        display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.2rem', flexShrink: 0,
                    }}>💼</div>
                    <div>
                        <h3 style={{ fontSize: '1.05rem', fontFamily: 'Outfit,sans-serif' }}>{job.title}</h3>
                        <div style={{ display: 'flex', gap: 8, marginTop: 4 }}>
                            <span className="badge badge-purple" style={{ fontSize: '0.7rem' }}>{job.required_skills?.length} skills required</span>
                        </div>
                    </div>
                </div>

                {/* Overlap mini-bar */}
                <div style={{ textAlign: 'right', minWidth: 80 }}>
                    <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: 4 }}>Your match</p>
                    <div style={{
                        fontSize: '1.2rem', fontWeight: 800, fontFamily: 'Outfit,sans-serif',
                        color: overlap >= 70 ? 'var(--emerald-400)' : overlap >= 40 ? 'var(--amber-400)' : 'var(--rose-400)',
                    }}>{overlap}%</div>
                </div>
            </div>

            <p style={{
                color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.6, marginBottom: 14,
                display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden',
            }}>
                {job.description}
            </p>

            {/* Required skills chips */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {(job.required_skills || []).map(skill => {
                    const has = resumeSkillsLower.includes(skill.toLowerCase())
                    return (
                        <span key={skill} className={`badge ${has ? 'badge-green' : 'badge-red'}`} style={{ fontSize: '0.72rem' }}>
                            {has ? '✓' : '✗'} {skill}
                        </span>
                    )
                })}
            </div>

            {/* Select indicator */}
            {selected && (
                <div style={{
                    position: 'absolute', top: 12, right: 12,
                    width: 24, height: 24, borderRadius: '50%',
                    background: 'var(--purple-500)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '0.75rem', color: 'white', fontWeight: 700,
                }}>✓</div>
            )}
        </div>
    )
}
