import { createContext, useContext, useState } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
    const [resumeData, setResumeData] = useState(null)   // parsed resume + id
    const [selectedJob, setSelectedJob] = useState(null)   // chosen job
    const [matchResult, setMatchResult] = useState(null)   // full match response
    const [step, setStep] = useState(1)      // 1=upload 2=jobs 3=results

    return (
        <AppContext.Provider value={{
            resumeData, setResumeData,
            selectedJob, setSelectedJob,
            matchResult, setMatchResult,
            step, setStep,
        }}>
            {children}
        </AppContext.Provider>
    )
}

export function useApp() {
    const ctx = useContext(AppContext)
    if (!ctx) throw new Error('useApp must be used inside AppProvider')
    return ctx
}
