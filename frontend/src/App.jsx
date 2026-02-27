import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AppProvider } from './hooks/useAppContext'
import Navbar from './components/Navbar'
import UploadPage from './pages/UploadPage'
import JobsPage from './pages/JobsPage'
import ResultPage from './pages/ResultPage'
import RoadmapPage from './pages/RoadmapPage'
import LandingPage from './pages/LandingPage'

export default function App() {
    return (
        <AppProvider>
            <BrowserRouter>
                <Toaster
                    position="top-right"
                    toastOptions={{
                        style: {
                            background: '#111827',
                            color: '#f1f5f9',
                            border: '1px solid rgba(139,92,246,0.3)',
                            borderRadius: '12px',
                            fontSize: '0.9rem',
                        },
                        success: { iconTheme: { primary: '#10b981', secondary: '#fff' } },
                        error: { iconTheme: { primary: '#fb7185', secondary: '#fff' } },
                    }}
                />
                <Navbar />
                <main style={{ flex: 1 }}>
                    <Routes>
                        <Route path="/" element={<LandingPage />} />
                        <Route path="/upload" element={<UploadPage />} />
                        <Route path="/jobs" element={<JobsPage />} />
                        <Route path="/results" element={<ResultPage />} />
                        <Route path="/roadmap" element={<RoadmapPage />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </main>
            </BrowserRouter>
        </AppProvider>
    )
}
