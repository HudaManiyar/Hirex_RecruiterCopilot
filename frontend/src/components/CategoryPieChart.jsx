import { CATEGORY_PALETTE } from '../data/chartPalette'

function polarToCartesian(cx, cy, r, angleDeg) {
  const rad = ((angleDeg - 90) * Math.PI) / 180
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) }
}

function describeSlice(cx, cy, r, startAngle, endAngle) {
  const start = polarToCartesian(cx, cy, r, endAngle)
  const end = polarToCartesian(cx, cy, r, startAngle)
  const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1
  return `M ${cx} ${cy} L ${start.x} ${start.y} A ${r} ${r} 0 ${largeArcFlag} 0 ${end.x} ${end.y} Z`
}

/** Renders a category breakdown as a pie chart + legend. data: { category, count }[] */
export default function CategoryPieChart({ data }) {
  const total = data.reduce((sum, d) => sum + d.count, 0)
  if (total === 0) return null

  const size = 200
  const cx = size / 2
  const cy = size / 2
  const r = size / 2 - 4

  let cursor = 0
  const slices = data.map((d, i) => {
    const startAngle = cursor
    cursor += (d.count / total) * 360
    return {
      ...d,
      color: CATEGORY_PALETTE[i % CATEGORY_PALETTE.length],
      path: describeSlice(cx, cy, r, startAngle, cursor),
      percent: (d.count / total) * 100,
    }
  })

  return (
    <div className="flex flex-col items-center gap-6 sm:flex-row sm:items-start">
      <svg viewBox={`0 0 ${size} ${size}`} className="h-48 w-48 shrink-0">
        {slices.length === 1 ? (
          <circle cx={cx} cy={cy} r={r} fill={slices[0].color} stroke="white" strokeWidth="2" />
        ) : (
          slices.map((s) => (
            <path key={s.category} d={s.path} fill={s.color} stroke="white" strokeWidth="2">
              <title>{`${s.category}: ${s.count} (${s.percent.toFixed(1)}%)`}</title>
            </path>
          ))
        )}
      </svg>

      <ul className="w-full space-y-2">
        {slices.map((s) => (
          <li key={s.category} className="flex items-center gap-2.5 text-sm">
            <span
              className="h-3 w-3 shrink-0 rounded-full"
              style={{ backgroundColor: s.color }}
              aria-hidden="true"
            />
            <span className="flex-1 text-ink">{s.category}</span>
            <span className="text-muted">{s.count}</span>
            <span className="w-10 text-right text-xs text-muted">{s.percent.toFixed(0)}%</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
