import { useEffect, useState } from 'react'

const STAGES = [
  { key: 'upload', label: 'Upload' },
  { key: 'extract', label: 'Extract' },
  { key: 'analyze', label: 'Analyze' },
  { key: 'save', label: 'Save' },
]

const API_URL = import.meta.env.VITE_API_URL

function ProgressMap({ file, onComplete }) {
  const [currentStage, setCurrentStage] = useState(0)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function runAnalysis() {
      try {
        setCurrentStage(0) // Upload

        setCurrentStage(1) // Extract

        const response = await fetch(`${API_URL}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': file.type },
          body: file,
        })

        setCurrentStage(2) // Analyze

        if (!response.ok) {
          throw new Error(`Request failed: ${response.status}`)
        }

        const result = await response.json()

        setCurrentStage(3) // Save
        onComplete(result)

      } catch (err) {
        setError(err.message)
      }
    }

    runAnalysis()
  }, [file])

  return (
    <div className="max-w-2xl mx-auto px-6 py-20">
      <h1 className="text-2xl font-serif text-[#0B1F3A] mb-10">
        Reviewing your bill...
      </h1>

      <div className="flex items-center gap-2">
        {STAGES.map((stage, i) => (
          <div key={stage.key} className="flex items-center gap-2">
            <div
              className={`px-4 py-2 rounded-full text-xs font-medium border ${
                i < currentStage
                  ? 'bg-[#0B1F3A] text-white border-[#0B1F3A]'
                  : i === currentStage
                  ? 'border-[#D4A24C] bg-[#FAEEDA] text-[#85631F]'
                  : 'border-slate-300 text-slate-400'
              }`}
            >
              {stage.label}
            </div>
            {i < STAGES.length - 1 && (
              <div className="w-4 h-px bg-slate-300" />
            )}
          </div>
        ))}
      </div>

      {error && (
        <p className="mt-8 text-sm text-[#8B2E2E]">
          Something went wrong: {error}
        </p>
      )}
    </div>
  )
}

export default ProgressMap