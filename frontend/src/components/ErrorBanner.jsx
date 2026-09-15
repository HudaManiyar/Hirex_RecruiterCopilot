export default function ErrorBanner({ message, onRetry }) {
  return (
    <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
      <p>{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-2 font-medium text-red-700 underline hover:text-red-800"
        >
          Try again
        </button>
      )}
    </div>
  )
}
