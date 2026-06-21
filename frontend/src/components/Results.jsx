import ReactMarkdown from 'react-markdown'

function Results({ result, onReset }) {
  if (!result) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-20">
        <p className="text-sm text-slate-500">No results to show.</p>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-20">
      <p className="text-xs uppercase tracking-widest text-slate-500 mb-3">
        Cost Analysis
      </p>
      <h1 className="text-3xl font-serif text-[#0B1F3A] mb-8">
        Your savings plan is ready.
      </h1>

      <div className="bg-white border border-slate-200 rounded-lg p-8 prose prose-slate prose-headings:font-serif prose-headings:text-[#0B1F3A] prose-h2:text-lg prose-h2:mt-6 prose-h2:mb-3 prose-strong:text-[#0B1F3A]">
        <ReactMarkdown>{result.analysis}</ReactMarkdown>
      </div>

      <div className="flex gap-3 mt-8">
        <button
          onClick={onReset}
          className="flex-1 py-3 rounded-lg text-sm font-medium border border-slate-300 text-[#0B1F3A] hover:bg-slate-50 transition-colors"
        >
          Analyze Another Bill
        </button>
      </div>
    </div>
  )
}

export default Results