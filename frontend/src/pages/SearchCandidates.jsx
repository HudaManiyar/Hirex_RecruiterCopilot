import { useState } from 'react'
import CandidateCard from '../components/CandidateCard'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'
import { rankCandidates, getErrorMessage } from '../api/client'
import { SAMPLE_SEARCH_QUERY } from '../data/sampleInputs'

const TOP_K = 5
const GRADE_ORDER = ['A', 'B', 'C', 'D']

// The ranking endpoint returns structured evaluations only, no prose answer —
// this is a client-side summary of the grades, not an LLM-generated one.
function summarize(evaluations) {
  if (evaluations.length === 0) return 'No candidates matched this query.'
  const parts = GRADE_ORDER.map((grade) => ({
    grade,
    count: evaluations.filter((e) => e.grade === grade).length,
  })).filter((g) => g.count > 0)
  const breakdown = parts.map((g) => `${g.count} grade ${g.grade}`).join(', ')
  return `${evaluations.length} candidate${evaluations.length === 1 ? '' : 's'} evaluated: ${breakdown}.`
}

export default function SearchCandidates() {
  const [query, setQuery] = useState(SAMPLE_SEARCH_QUERY)
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSearch(e) {
    e?.preventDefault()
    if (!query.trim() || loading) return

    setLoading(true)
    setError(null)
    try {
      const data = await rankCandidates(query, TOP_K)
      setResults(data.evaluations)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-8 py-12">
      <h1 className="font-serif text-3xl text-ink">Recruiter Copilot</h1>
      <p className="mt-2 text-muted">Ask a plain-language question about your candidate pool.</p>

      <form
        className="mt-6 flex items-center gap-3 rounded-full border border-terracotta/30 bg-peach/40 px-4 py-2"
        onSubmit={handleSearch}
      >
        <span aria-hidden="true" className="text-terracotta">
          🔍
        </span>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 bg-transparent text-sm text-ink outline-none placeholder:text-slate-400"
          placeholder="Ask about your candidate pool..."
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="rounded-md border border-slate-300 bg-white px-4 py-1.5 text-sm font-medium text-ink hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Searching…' : 'Search'}
        </button>
      </form>
      <p className="mt-2 text-xs text-slate-400">
        e.g. &ldquo;Who has strong data analysis and Python experience?&rdquo;
      </p>

      {error && (
        <div className="mt-6">
          <ErrorBanner message={error} onRetry={handleSearch} />
        </div>
      )}

      {loading && <LoadingSpinner label="Searching candidate pool…" />}

      {!loading && results && (
        <>
          <div className="mt-6 rounded-xl border-t-4 border-terracotta bg-white p-5 shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
            <p className="text-xs font-semibold tracking-wide text-terracotta uppercase">✦ Result Summary</p>
            <p className="mt-2 text-sm text-slate-600 italic">{summarize(results)}</p>
          </div>

          <h2 className="mt-8 text-sm font-medium text-muted">Closest matches</h2>
          <div className="mt-4 space-y-4">
            {results.map((evaluation, index) => (
              <CandidateCard
                key={`${evaluation.source_file ?? evaluation.candidate_name}-${index}`}
                evaluation={evaluation}
                variant="search"
              />
            ))}
          </div>
        </>
      )}

      {!loading && !results && !error && (
        <p className="mt-8 text-sm text-muted">Run a search to see matching candidates.</p>
      )}
    </div>
  )
}
