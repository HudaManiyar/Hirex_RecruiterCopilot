import { useState } from 'react'
import GradeBadge from './GradeBadge'
import SkillPill from './SkillPill'

const GRADE_LABELS = {
  A: 'Strong match',
  B: 'Good match',
  C: 'Partial match',
  D: 'Weak match',
}

const GRADE_BORDER_CLASS = {
  A: 'border-grade-a',
  B: 'border-grade-b',
  C: 'border-grade-c',
  D: 'border-grade-d',
}

/**
 * Renders one CandidateEvaluation (see backend/app/models/ranking_schema.py).
 * variant="search"  -> labeled Matched/Missing rows + grade badge (flat list view)
 * variant="ranking" -> bare skill pills, no grade badge (grouped-by-grade column view)
 */
export default function CandidateCard({ evaluation, variant = 'search' }) {
  const [expanded, setExpanded] = useState(false)

  const {
    candidate_name,
    grade,
    confidence,
    matched_skills = [],
    missing_skills = [],
    evidence = [],
    reasoning,
  } = evaluation

  const displayName = candidate_name?.trim() ? candidate_name : 'Unknown candidate'
  const evidenceList = Array.isArray(evidence) ? evidence : evidence ? [evidence] : []
  const quote = evidenceList[0]
  const additionalEvidence = evidenceList.slice(1)
  const showGrade = variant === 'search'
  const showLabels = variant === 'search'

  return (
    <div
      className={`rounded-xl border-[1.5px] bg-white p-5 shadow-[0_1px_3px_rgba(0,0,0,0.08)] ${
        GRADE_BORDER_CLASS[grade] ?? GRADE_BORDER_CLASS.D
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-semibold text-ink">{displayName}</h3>
          {confidence && (
            <span className="mt-1.5 inline-block rounded-full border border-terracotta/30 px-2.5 py-0.5 text-[11px] text-terracotta">
              Confidence: {confidence}
            </span>
          )}
        </div>
        {showGrade && (
          <div className="flex shrink-0 flex-col items-center gap-1">
            <GradeBadge grade={grade} size="sm" />
            <span className="text-[11px] whitespace-nowrap text-slate-500">{GRADE_LABELS[grade] ?? ''}</span>
          </div>
        )}
      </div>

      {matched_skills.length > 0 && (
        <div className="mt-3 flex flex-wrap items-center gap-1.5 text-xs">
          {showLabels && <span className="font-medium text-slate-500">Matched:</span>}
          {matched_skills.map((skill) => (
            <SkillPill key={skill} label={skill} variant={showLabels ? 'matched' : 'neutral'} />
          ))}
        </div>
      )}

      {showLabels && missing_skills.length > 0 && (
        <div className="mt-2 flex flex-wrap items-center gap-1.5 text-xs">
          <span className="font-medium text-slate-500">Missing:</span>
          {missing_skills.map((skill) => (
            <SkillPill key={skill} label={skill} variant="missing" />
          ))}
        </div>
      )}

      {quote && (
        <blockquote className="mt-3 border-l-2 border-terracotta/40 pl-3 text-sm text-slate-600 italic">
          &ldquo;{quote}&rdquo;
        </blockquote>
      )}

      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        aria-expanded={expanded}
        className="mt-3 text-xs font-medium text-terracotta hover:underline"
      >
        {expanded ? 'Hide full evaluation' : 'View full evaluation'} {expanded ? '︿' : '⌄'}
      </button>

      {expanded && (
        <div className="mt-3 space-y-2 border-t border-slate-100 pt-3 text-sm text-slate-600">
          {reasoning && <p>{reasoning}</p>}
          {additionalEvidence.length > 0 &&
            additionalEvidence.map((item, index) => (
              <blockquote key={index} className="border-l-2 border-terracotta/40 pl-3 italic">
                &ldquo;{item}&rdquo;
              </blockquote>
            ))}
          {!reasoning && additionalEvidence.length === 0 && (
            <p className="text-slate-400 italic">No additional evaluation details available.</p>
          )}
        </div>
      )}
    </div>
  )
}
