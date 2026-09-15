import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: { 'Content-Type': 'application/json' },
})

// Turns an axios error (network failure, FastAPI HTTPException, or a 422
// validation error) into one human-readable string for display.
export function getErrorMessage(error) {
  if (!error?.response) {
    return `Could not reach the API at ${apiClient.defaults.baseURL}. Make sure the backend is running.`
  }
  const detail = error.response.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((d) => d.msg).filter(Boolean).join('; ')
  }
  return error.message || 'Something went wrong. Please try again.'
}

// -> JDAnalysis (app/models/jd_schema.py)
export async function analyzeJD(jdText) {
  const { data } = await apiClient.post('/api/jd/analyze', { jd_text: jdText })
  return data
}

// -> RankingResponse (app/models/ranking_schema.py)
export async function rankCandidates(jobRequirement, topK = 5) {
  const { data } = await apiClient.post('/api/ranking/rank', {
    job_requirement: jobRequirement,
    top_k: topK,
  })
  return data
}

// -> { jd_analysis: JDAnalysis, candidate_evaluations: CandidateEvaluation[] }
export async function generateReport(jdText, topK = 5) {
  const { data } = await apiClient.post('/api/report/generate', {
    jd_text: jdText,
    top_k: topK,
  })
  return data
}

// -> { total_resumes: number, categories: { category, count }[], source_breakdown: { real, synthetic } }
export async function getStats() {
  const { data } = await apiClient.get('/api/stats')
  return data
}

export default apiClient
