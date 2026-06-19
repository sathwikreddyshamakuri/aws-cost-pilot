import { useState } from 'react'
import Dashboard from './components/Dashboard'
import ProgressMap from './components/ProgressMap'
import Results from './components/Results'

function App() {
  const [screen, setScreen] = useState('dashboard')
  const [selectedFile, setSelectedFile] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)

  return (
    <div className="min-h-screen bg-[#F7F5F0]">
      {screen === 'dashboard' && (
        <Dashboard
          onAnalysisStart={(file) => {
            setSelectedFile(file)
            setScreen('progress')
          }}
        />
      )}
      {screen === 'progress' && (
        <ProgressMap
          file={selectedFile}
          onComplete={(result) => {
            setAnalysisResult(result)
            setScreen('results')
          }}
        />
      )}
      {screen === 'results' && (
        <Results result={analysisResult} onReset={() => setScreen('dashboard')} />
      )}
    </div>
  )
}

export default App