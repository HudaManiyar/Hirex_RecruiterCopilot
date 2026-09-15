export default function StatCard({ label, value }) {
  return (
    <div className="rounded-xl border-t-4 border-terracotta bg-white px-5 py-4 shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
      <p className="text-[11px] font-semibold uppercase tracking-wide text-terracotta/80">{label}</p>
      <p className="mt-2 text-2xl font-bold text-ink">{value}</p>
    </div>
  )
}
