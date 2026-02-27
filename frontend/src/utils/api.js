import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
    baseURL: BASE,
    timeout: 30000,
})

// ── Resume ─────────────────────────────────────────────────────────────────────
export const uploadResume = (file, onProgress) => {
    const form = new FormData()
    form.append('file', file)
    return api.post('/resume/upload', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: e => {
            if (onProgress) onProgress(Math.round((e.loaded * 100) / e.total))
        },
    })
}

export const getResume = (id) => api.get(`/resume/${id}`)

// ── Jobs ───────────────────────────────────────────────────────────────────────
export const listJobs = () => api.get('/jobs/')
export const getJob = (id) => api.get(`/jobs/${id}`)
export const createJob = (payload) => api.post('/jobs/', payload)

// ── Match ──────────────────────────────────────────────────────────────────────
export const matchResumeToJob = (resumeId, jobId) =>
    api.post('/match/', { resume_id: resumeId, job_id: jobId })

// ── Skills ─────────────────────────────────────────────────────────────────────
export const listSkills = () => api.get('/skills/')
export const searchSkills = (prefix) => api.get(`/skills/search/${prefix}`)
export const getSkillDeps = (skill) => api.get(`/skills/dependencies/${skill}`)
export const getSkillGraph = () => api.get('/skills/graph')

export default api
