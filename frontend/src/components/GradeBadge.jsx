const GRADE_STYLES = {
  A: 'border-grade-a/40 bg-grade-a/10 text-grade-a',
  B: 'border-grade-b/40 bg-grade-b/10 text-grade-b',
  C: 'border-grade-c/40 bg-grade-c/10 text-grade-c',
  D: 'border-grade-d/40 bg-grade-d/10 text-grade-d',
}

const SIZE_STYLES = {
  sm: 'h-8 w-8 text-sm',
  md: 'h-9 w-9 text-sm',
}

export default function GradeBadge({ grade, size = 'md' }) {
  return (
    <span
      className={`inline-flex shrink-0 items-center justify-center rounded-lg border font-semibold ${
        GRADE_STYLES[grade] ?? GRADE_STYLES.D
      } ${SIZE_STYLES[size] ?? SIZE_STYLES.md}`}
    >
      {grade}
    </span>
  )
}
