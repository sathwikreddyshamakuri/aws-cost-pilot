import { useState } from 'react'

function Dashboard({ onAnalysisStart }) {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)

  function handleFileSelect(selectedFile) {
    const validTypes = ['application/pdf', 'text/csv']
    if (selectedFile && validTypes.includes(selectedFile.type)) {
      setFile(selectedFile)
    } else {
      alert('Please upload a PDF or CSV file.')
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    setIsDragging(false)
    const droppedFile = e.dataTransfer.files[0]
    handleFileSelect(droppedFile)
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-20">
      <p className="text-xs uppercase tracking-widest text-slate-500 mb-3">
        AWS Cost Pilot
      </p>
      <h1 className="text-4xl font-serif text-[#0B1F3A] mb-10 leading-tight">
        Turn your AWS bill<br />into a plan.
      </h1>

      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-10 flex flex-col items-center gap-3 transition-colors ${
          isDragging ? 'border-[#D4A24C] bg-[#FAEEDA]' : 'border-slate-400 bg-white/40'
        }`}
      >
        {file ? (
          <>
            <p className="text-sm font-medium text-[#0B1F3A]">{file.name}</p>
            <p className="text-xs text-slate-500">Ready to analyze</p>
          </>
        ) : (
          <>
            <p className="text-sm font-medium text-[#0B1F3A]">Drop your AWS bill here</p>
            <p className="text-xs text-slate-500">PDF or CSV</p>
          </>
        )}

        <label className="mt-2 text-xs text-[#0B1F3A] underline cursor-pointer">
          or browse files
          <input
            type="file"
            accept=".pdf,.csv"
            className="hidden"
            onChange={(e) => handleFileSelect(e.target.files[0])}
          />
        </label>
      </div>

      <button
        disabled={!file}
        onClick={() => onAnalysisStart(file)}
        className={`mt-8 w-full py-3 rounded-lg text-sm font-medium transition-colors ${
          file
            ? 'bg-[#0B1F3A] text-white hover:bg-[#142b4d]'
            : 'bg-slate-200 text-slate-400 cursor-not-allowed'
        }`}
      >
        Analyze My Costs
      </button>
    </div>
  )
}

export default Dashboard