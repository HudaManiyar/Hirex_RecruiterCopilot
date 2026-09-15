export default function SkillPill({ label, variant = 'matched' }) {
  const styles =
    variant === 'matched'
      ? 'border-grade-a/40 bg-grade-a/5 text-grade-a'
      : variant === 'missing'
        ? 'border-slate-300 bg-slate-50 text-slate-500'
        : 'border-terracotta/30 bg-terracotta/5 text-terracotta'

  return (
    <span className={`inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium ${styles}`}>
      {variant === 'matched' && <span aria-hidden="true">✓</span>}
      {label}
    </span>
  )
}
