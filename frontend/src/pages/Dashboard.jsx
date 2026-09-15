import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import StatCard from '../components/StatCard'
import CategoryPieChart from '../components/CategoryPieChart'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorBanner from '../components/ErrorBanner'
import { getStats, getErrorMessage } from '../api/client'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  async function loadStats() {
    setLoading(true)
    setError(null)
    try {
      const data = await getStats()
      setStats(data)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadStats()
  }, [])

  const categories = stats?.categories ?? []

  const summaryStats = [
    { label: 'Total Resumes Processed', value: stats ? String(stats.total_resumes) : '—' },
    { label: 'Number of Categories', value: stats ? String(categories.length) : '—' },
  ]

  return (
    <div className="mx-auto max-w-7xl px-8 py-12">
      <p className="text-xs font-semibold tracking-widest text-terracotta uppercase">HireX Copilot</p>
      <h1 className="mt-2 font-serif text-4xl text-ink">Your Recruitment Copilot for smarter hiring</h1>
      <p className="mt-4 max-w-2xl text-muted">
        HireX reads resumes and job descriptions the way a recruiter would — surfacing evidence, not a hidden
        score, so you stay the decision-maker.
      </p>
      <div className="mt-6 flex items-center gap-5">
        <Link
          to="/search"
          className="inline-flex items-center gap-2 rounded-full border border-terracotta px-5 py-2 text-sm font-medium text-terracotta transition-colors hover:bg-terracotta hover:text-white"
        >
          Start a search →
        </Link>
        <button
          type="button"
          onClick={loadStats}
          disabled={loading}
          className="text-sm font-medium text-terracotta hover:underline disabled:opacity-50"
        >
          {loading ? 'Refreshing…' : 'Refresh snapshot'}
        </button>
      </div>

      {error && (
        <div className="mt-6">
          <ErrorBanner message={error} onRetry={loadStats} />
        </div>
      )}

      {loading && !stats ? (
        <LoadingSpinner label="Loading dashboard snapshot…" />
      ) : (
        <>
          <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-2">
            {summaryStats.map((stat) => (
              <StatCard key={stat.label} label={stat.label} value={stat.value} />
            ))}
          </div>

          <h2 className="mt-12 text-xl font-semibold text-ink">Overview</h2>
          <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-xl border-t-4 border-terracotta bg-white p-6 shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
              <h3 className="text-sm font-semibold text-ink">Category Breakdown</h3>
              {categories.length === 0 ? (
                <p className="mt-4 text-sm text-muted">No candidate data yet.</p>
              ) : (
                <div className="mt-4">
                  <CategoryPieChart data={categories} />
                </div>
              )}
            </div>

            <div className="flex flex-col items-center justify-center rounded-xl border-t-4 border-terracotta bg-white p-6 text-center shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
              <h3 className="text-sm font-semibold text-ink">Grade Distribution &amp; Matched Skills</h3>
              <p className="mt-3 max-w-xs text-sm text-muted">
                These are evidence from a specific search, so they only appear once you run one against the
                candidate pool.
              </p>
              <Link
                to="/search"
                className="mt-4 inline-flex items-center gap-2 rounded-full border border-terracotta px-5 py-2 text-sm font-medium text-terracotta transition-colors hover:bg-terracotta hover:text-white"
              >
                Start a search →
              </Link>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
