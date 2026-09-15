import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import SearchCandidates from './pages/SearchCandidates'
import Rankings from './pages/Rankings'
import JDAnalyzer from './pages/JDAnalyzer'

export default function App() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/search" element={<SearchCandidates />} />
        <Route path="/rankings" element={<Rankings />} />
        <Route path="/jd-analyzer" element={<JDAnalyzer />} />
      </Routes>
    </div>
  )
}
