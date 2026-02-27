import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import toast from 'react-hot-toast'
import { uploadResume } from '../utils/api'
import { useApp } from '../hooks/useAppContext'

const ACCEPTED = { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'], 'text/plain': ['.txt'] }

export default function UploadPage() {
    const navigate = useNavigate()
    const { setResumeData } = useApp()
    const [file, setFile] = useState(null)
    const [progress, setProgress] = useState(0)
    const [loading, setLoading] = useState(false)
    const [parsed, setParsed] = useState(null)

    const onDrop = useCallback(accepted => {
        if (!accepted.length) return
        const f = accepted[0]
        if (f.size > 2 * 1024 * 1024) { toast.error('File must be under 2 MB'); return }
        setFile(f); setParsed(null); setProgress(0)
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop, accept: ACCEPTED, maxFiles: 1,
        onDropRejected: () => toast.error('Please upload a PDF, DOCX, or TXT file'),
    })

    const handleUpload = async () => {
        if (!file) { toast.error('Please select a file first'); return }
        setLoading(true)
        try {
            const { data } = await uploadResume(file, setProgress)
            setParsed(data)
            setResumeData(data)
            toast.success('Resume parsed successfully! 🎉')
        } catch (err) {
            const msg = err.response?.data?.detail || 'Upload failed. Is the backend running?'
            toast.error(msg)
        } finally { setLoading(false) }
    }

    const handleContinue = () => navigate('/jobs')

    const fileSize = file ? (file.size / 1024).toFixed(1) + ' KB' : ''
    const ext = file?.name?.split('.').pop()?.toUpperCase() || ''

    return (
        <div className="container" style={{ padding: '48px 24px', maxWidth: 760 }}>
            {/* Header */}
            <div className="animate-fade-in-up" style={{ marginBottom: 40, textAlign: 'center' }}>
                <h1 style={{ fontSize: 'clamp(1.8rem,4vw,2.4rem)', marginBottom: 12 }}>
                    Upload Your <span className="gradient-text">Resume</span>
                </h1>
                <p style={{ color: 'var(--text-secondary)', fontSize: '1rem' }}>
                    Supports PDF, DOCX, and TXT — up to 2 MB. We'll extract your skills, experience, education and projects instantly.
                </p>
            </div>

            {/* Dropzone */}
            <div className="animate-fade-in-up delay-100">
                <div
                    {...getRootProps()}
                    style={{
                        border: `2px dashed ${isDragActive ? 'var(--purple-400)' : file ? 'var(--emerald-500)' : 'rgba(139,92,246,0.35)'}`,
                        borderRadius: 'var(--radius-xl)',
                        padding: '60px 32px',
                        textAlign: 'center',
                        cursor: 'pointer',
                        transition: 'all 0.3s',
                        background: isDragActive
                            ? 'rgba(139,92,246,0.08)'
                            : file
                                ? 'rgba(16,185,129,0.05)'
                                : 'rgba(139,92,246,0.03)',
                        position: 'relative',
                        overflow: 'hidden',
                    }}
                >
                    {isDragActive && (
                        <div style={{
                            position: 'absolute', inset: 0,
                            background: 'radial-gradient(circle at center, rgba(139,92,246,0.15), transparent 70%)',
                        }} />
                    )}
                    <input {...getInputProps()} id="resume-file-input" />

                    <div style={{ fontSize: '3.5rem', marginBottom: 20 }}>
                        {file ? '📄' : isDragActive ? '🎯' : '☁️'}
                    </div>

                    {file ? (
                        <div>
                            <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: 8 }}>{file.name}</div>
                            <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
                                <span className="badge badge-purple">{ext}</span>
                                <span className="badge badge-cyan">{fileSize}</span>
                            </div>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: 12 }}>
                                Click or drag to replace
                            </p>
                        </div>
                    ) : (
                        <div>
                            <p style={{ fontWeight: 600, fontSize: '1.05rem', marginBottom: 8 }}>
                                {isDragActive ? 'Drop it here!' : 'Drag & drop your resume here'}
                            </p>
                            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: 16 }}>
                                or click to browse files
                            </p>
                            <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
                                {['PDF', 'DOCX', 'TXT'].map(t => (
                                    <span key={t} className="badge badge-purple">{t}</span>
                                ))}
                                <span className="badge badge-cyan">Max 2 MB</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Upload Progress */}
            {loading && (
                <div className="animate-fade-in" style={{ marginTop: 24 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        <span>Uploading & analysing…</span>
                        <span>{progress}%</span>
                    </div>
                    <div className="progress-bar">
                        <div className="progress-fill" style={{
                            width: `${progress}%`,
                            background: 'linear-gradient(90deg, var(--purple-600), var(--cyan-400))',
                        }} />
                    </div>
                </div>
            )}

            {/* CTA Buttons */}
            <div className="animate-fade-in-up delay-200" style={{ display: 'flex', gap: 12, marginTop: 24 }}>
                <button
                    id="upload-resume-btn"
                    onClick={handleUpload}
                    disabled={!file || loading}
                    className="btn btn-primary"
                    style={{ flex: 1, fontSize: '1rem', padding: '14px 0' }}
                >
                    {loading ? (
                        <><span className="animate-spin-slow" style={{ display: 'inline-block' }}>⟳</span> Analysing…</>
                    ) : '🚀 Parse Resume'}
                </button>
                {parsed && (
                    <button id="continue-to-jobs-btn" onClick={handleContinue} className="btn btn-secondary" style={{ flex: 1, fontSize: '1rem' }}>
                        Continue to Jobs →
                    </button>
                )}
            </div>

            {/* Parsed Result Preview */}
            {parsed && (
                <div className="card animate-fade-in" style={{ marginTop: 32 }}>
                    <h2 style={{ fontSize: '1.15rem', marginBottom: 20, display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span style={{ background: 'linear-gradient(135deg,#7c3aed,#06b6d4)', padding: '4px 10px', borderRadius: 8, fontSize: '0.8rem', color: 'white' }}>PARSED</span>
                        Resume Summary
                    </h2>

                    {/* Skills */}
                    <div style={{ marginBottom: 20 }}>
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 10 }}>
                            Detected Skills ({parsed.skills?.length || 0})
                        </p>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                            {(parsed.skills || []).length > 0
                                ? parsed.skills.map(s => <span key={s} className="badge badge-purple">{s}</span>)
                                : <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>No skills detected — try a richer resume</span>
                            }
                        </div>
                    </div>

                    <div className="divider" />

                    {/* Meta */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
                        <Stat label="Experience" value={parsed.experience ? `${parsed.experience} years` : 'Not detected'} icon="💼" />
                        <Stat label="Education" value={parsed.education || 'Not detected'} icon="🎓" />
                    </div>

                    {parsed.projects?.length > 0 && (
                        <>
                            <div className="divider" />
                            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 10 }}>
                                Projects ({parsed.projects.length})
                            </p>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                                {parsed.projects.map((p, i) => (
                                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                                        <span style={{ color: 'var(--cyan-400)' }}>▸</span> {p}
                                    </div>
                                ))}
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    )
}

function Stat({ label, value, icon }) {
    return (
        <div style={{
            background: 'rgba(255,255,255,0.03)', borderRadius: 'var(--radius-md)',
            padding: '12px 16px', border: '1px solid var(--border)',
        }}>
            <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>{label}</p>
            <p style={{ fontWeight: 600 }}>{icon} {value}</p>
        </div>
    )
}
