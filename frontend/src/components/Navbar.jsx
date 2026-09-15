import { NavLink } from 'react-router-dom'

const LINKS = [
  { to: '/', label: 'Dashboard' },
  { to: '/search', label: 'Search Candidates' },
  { to: '/rankings', label: 'Rankings' },
  { to: '/jd-analyzer', label: 'JD Analyzer' },
]

export default function Navbar() {
  return (
    <header className="bg-terracotta">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-8 py-4">
        <div className="flex items-center gap-2 text-white">
          <span aria-hidden="true">✦</span>
          <span className="font-serif text-xl">HireX</span>
        </div>
        <ul className="flex items-center gap-1 text-sm font-medium">
          {LINKS.map((link) => (
            <li key={link.to}>
              <NavLink
                to={link.to}
                end={link.to === '/'}
                className={({ isActive }) =>
                  `inline-block rounded-full px-4 py-2 transition-colors ${
                    isActive
                      ? 'bg-white text-terracotta'
                      : 'text-white/90 hover:text-white'
                  }`
                }
              >
                {link.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  )
}
