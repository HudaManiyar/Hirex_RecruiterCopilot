import { useState } from 'react'
import { analyzeJD, getErrorMessage } from '../api/client'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'
import { SAMPLE_JD_TEXT } from '../data/sampleInputs'

function ListSection({ title, items, icon, iconClass }) {
  if (!items || items.length === 0) return null

  return (
    <div>
      <h2 className="text-lg font-semibold text-ink">{title}</h2>
      <div className="mt-3 space-y-3">
        {items.map((item) => (
          <div key={item} className="flex items-start gap-3 rounded-lg bg-peach/50 px-4 py-3 text-sm text-slate-600">
            <span aria-hidden="true" className={`mt-0.5 ${iconClass}`}>
              {icon}
            </span>
            <span>{item}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function JDAnalyzer() {
  const [jdText, setJdText] = useState(SAMPLE_JD_TEXT)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleAnalyze(e) {
    e?.preventDefault()
    if (!jdText.trim() || loading) return

    setLoading(true)
    setError(null)
    try {
      const data = await analyzeJD(jdText)
      setResult(data)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-6xl px-8 py-12">
      <h1 className="font-serif text-3xl text-ink">JD Analyzer</h1>
      <p className="mt-2 text-muted">
        Paste a job description to check clarity, inclusive language, and requirement quality — before
        candidates ever see it.
      </p>

      <form onSubmit={handleAnalyze} className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div>
          <label htmlFor="jd-text" className="text-xs font-medium text-muted">
            Job description
          </label>
          <textarea
            id="jd-text"
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            rows={12}
            className="mt-2 w-full resize-y rounded-lg border border-slate-300 p-4 text-sm text-ink outline-none focus:border-terracotta"
          />
          <button
            type="submit"
            disabled={loading || !jdText.trim()}
            className="mt-3 rounded-full bg-terracotta px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-terracotta/90 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Analyzing…' : 'Analyze Job Description'}
          </button>
        </div>

        <div className="flex flex-col items-center justify-center p-6 text-center">
          {loading ? (
            <LoadingSpinner label="Analyzing job description…" />
          ) : result ? (
            <>
              <h3 className="text-sm font-semibold text-ink">Quality Score</h3>
              <div className="mt-4 flex h-32 w-32 flex-col items-center justify-center rounded-full bg-terracotta">
                <span className="font-serif text-4xl font-bold text-white">{result.quality_score}</span>
                <span className="text-xs font-medium text-white/80">/10</span>
              </div>
            </>
          ) : (
            <p className="text-sm text-muted">Run an analysis to see the quality score.</p>
          )}
        </div>
      </form>

      {error && (
        <div className="mt-6">
          <ErrorBanner message={error} onRetry={handleAnalyze} />
        </div>
      )}

      {result && (
        <div className="mt-10 grid grid-cols-1 gap-8 md:grid-cols-2">
          <ListSection title="Strengths" items={result.strengths} icon="✓" iconClass="text-grade-a" />
          <ListSection title="Weaknesses" items={result.weaknesses} icon="✕" iconClass="text-grade-d" />
          <ListSection title="Missing Elements" items={result.missing_elements} icon="ⓘ" iconClass="text-terracotta" />
          <ListSection title="Ambiguous Phrases" items={result.ambiguous_phrases} icon="❝" iconClass="text-grade-c" />
        </div>
      )}
    </div>
  )
}
