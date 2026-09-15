import { useState } from 'react'
import GradeBadge from '../components/GradeBadge'
import CandidateCard from '../components/CandidateCard'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'
import { rankCandidates, getErrorMessage } from '../api/client'
import { SAMPLE_JD_TEXT } from '../data/sampleInputs'

const COLUMNS = [
  { grade: 'A', label: 'Strong match', border: 'border-t-grade-a' },
  { grade: 'B', label: 'Good match', border: 'border-t-grade-b' },
  { grade: 'C', label: 'Partial match', border: 'border-t-grade-c' },
  { grade: 'D', label: 'Weak match', border: 'border-t-grade-d' },
]

const TOP_K = 8

export default function Rankings() {
  const [jobRequirement, setJobRequirement] = useState(SAMPLE_JD_TEXT)
  const [evaluations, setEvaluations] = useState([])
  const [hasRun, setHasRun] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function runRanking(e) {
    e?.preventDefault()
    if (!jobRequirement.trim() || loading) return

    setLoading(true)
    setError(null)
    try {
      const data = await rankCandidates(jobRequirement, TOP_K)
      setEvaluations(data.evaluations)
      setHasRun(true)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  const byGrade = (grade) => evaluations.filter((e) => e.grade === grade)

  return (
    <div className="mx-auto max-w-7xl px-8 py-12">
      <h1 className="font-serif text-3xl text-ink">Candidate Rankings</h1>
      <p className="mt-2 text-muted italic">Evidence-backed grades. You make the call.</p>

      <form onSubmit={runRanking} className="mt-6 space-y-3">
        <label htmlFor="job-requirement" className="text-xs font-medium text-muted">
          Job requirement
        </label>
        <textarea
          id="job-requirement"
          value={jobRequirement}
          onChange={(e) => setJobRequirement(e.target.value)}
          rows={3}
          className="w-full resize-y rounded-lg border border-slate-300 p-3 text-sm text-ink outline-none focus:border-terracotta"
        />
        <button
          type="submit"
          disabled={loading || !jobRequirement.trim()}
          className="rounded-full bg-terracotta px-5 py-2 text-sm font-medium text-white transition-colors hover:bg-terracotta/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Ranking…' : 'Rank Candidates'}
        </button>
      </form>

      {error && (
        <div className="mt-4">
          <ErrorBanner message={error} onRetry={runRanking} />
        </div>
      )}

      <div className="mt-6 flex flex-wrap items-center gap-4 border-b border-slate-200 pb-4 text-xs text-muted">
        {COLUMNS.map((c) => (
          <span key={c.grade} className="flex items-center gap-1.5">
            <GradeBadge grade={c.grade} size="sm" /> = {c.label}
          </span>
        ))}
      </div>

      {loading ? (
        <LoadingSpinner label="Ranking candidates…" />
      ) : !hasRun ? (
        <p className="mt-8 text-sm text-muted">Enter a job requirement and click &ldquo;Rank Candidates&rdquo; to see results.</p>
      ) : evaluations.length === 0 ? (
        <p className="mt-8 text-sm text-muted">No candidates matched this requirement.</p>
      ) : (
        <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-4">
          {COLUMNS.map((col) => {
            const items = byGrade(col.grade)
            return (
              <div
                key={col.grade}
                className={`rounded-xl border-t-4 bg-white p-4 shadow-[0_1px_3px_rgba(0,0,0,0.08)] ${col.border}`}
              >
                <div className="flex items-center gap-2">
                  <GradeBadge grade={col.grade} size="sm" />
                  <span className="text-sm font-semibold text-ink">{col.label}</span>
                  <span className="ml-auto text-xs text-slate-400">{items.length}</span>
                </div>
                <div className="mt-4 space-y-4">
                  {items.map((evaluation, index) => (
                    <CandidateCard
                      key={`${evaluation.source_file ?? evaluation.candidate_name}-${index}`}
                      evaluation={evaluation}
                      variant="ranking"
                    />
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
