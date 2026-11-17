
import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [risks, setRisks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [lastUpdated, setLastUpdated] = useState(null)
  const [apiConnected, setApiConnected] = useState(false)

  const currentHour = new Date().getHours()

  const greeting =
    currentHour < 12
      ? 'Good morning.'
      : currentHour < 17
        ? 'Good afternoon.'
        : 'Good evening.'

  async function fetchRisks() {
    try {
      const response = await fetch('/api/risks')

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const data = await response.json()

      setApiConnected(true)
      setError('')
      setRisks(data.risks || [])
      setLastUpdated(new Date())
    } catch (err) {
      setApiConnected(false)
      setError(err.message || 'Unable to load risk data.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    let active = true

    fetch('/api/risks')
      .then(response => {
        if (!response.ok) {
          throw new Error(`API request failed: ${response.status}`)
        }
        return response.json()
      })
      .then(data => {
        if (!active) return

        setApiConnected(true)
        setRisks(data.risks || [])
        setLastUpdated(new Date())
      })
      .catch(err => {
        if (active) {
          setApiConnected(false)
          setError(err.message || 'Unable to load risk data.')
        }
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [])

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">V</div>
          <div>
            <h2>VELOXA</h2>
            <span>EXECUTIVE INTELLIGENCE</span>
          </div>
        </div>

        <div className="topbar-right">
          <span className="live-indicator">
            <span className="live-dot"></span>
            {apiConnected ? 'API CONNECTED' : 'API DISCONNECTED'}
          </span>

          <button
            className="refresh-button"
            onClick={() => {
              setLoading(true)
              fetchRisks()
            }}
            disabled={loading}
          >
            ↻ {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="welcome-section">
          <div>
            <p className="eyebrow">CEO COMMAND CENTER / OVERVIEW</p>
            <h1>{greeting}</h1>
            <p className="subtitle">
              Here is your current business risk overview.
            </p>
          </div>

          <div className="update-info">
            <span>LAST UPDATED</span>
            <strong>
              {lastUpdated
                ? lastUpdated.toLocaleTimeString()
                : 'Not available'}
            </strong>
          </div>
        </section>

        <section className="summary-grid">
          <div className="summary-card">
            <span className="summary-label">PRIORITY RISKS</span>
            <strong>{risks.length}</strong>
            <small>Identified risk areas</small>
          </div>

          <div className="summary-card">
            <span className="summary-label">HIGH IMPACT</span>
            <strong>
              {risks.filter(risk => risk.impact === 'High').length}
            </strong>
            <small>Require executive attention</small>
          </div>

          <div className="summary-card">
            <span className="summary-label">EVIDENCE SOURCES</span>
            <strong>
              {
                new Set(
                  risks.flatMap(risk =>
                    risk.evidence.map(item => item.source)
                  )
                ).size
              }
            </strong>
            <small>Distinct supporting documents</small>
          </div>
        </section>

        <section className="risk-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">INTELLIGENCE BRIEFING</p>
              <h2>Top business risks</h2>
              <p className="subtitle">
                Ranked by impact, urgency and supporting evidence.
              </p>
            </div>

            <span className="provisional-label">
              PROVISIONAL RANKING
            </span>
          </div>

          {loading && (
            <p className="message">Loading risk intelligence...</p>
          )}

          {error && (
            <div className="error-message">
              <strong>Unable to load risks</strong>
              <p>{error}</p>
              <button
                onClick={() => {
                  setLoading(true)
                  fetchRisks()
                }}
              >
                Try again
              </button>
            </div>
          )}

          {!loading && !error && risks.length === 0 && (
            <p className="message">
              No risk records were returned by the API.
            </p>
          )}

          {!loading && !error && (
            <div className="risk-list">
              {risks.map(risk => (
                <article className="risk-card" key={risk.risk_id}>
                  <div className="risk-card-header">
                    <div className="risk-title-group">
                      <span className="priority-label">
                        PRIORITY {risk.priority}
                      </span>
                      <h3>{risk.title}</h3>
                      <span className="risk-id">{risk.risk_id}</span>
                    </div>

                    <div className="score-box">
                      <strong>
                        {risk.score}<small>/22</small>
                      </strong>
                      <span>RISK SCORE</span>
                    </div>
                  </div>

                  <div className="risk-metrics">
                    <div>
                      <span>IMPACT</span>
                      <strong
                        className={
                          risk.impact === 'High' ? 'high' : 'medium'
                        }
                      >
                        {risk.impact}
                      </strong>
                    </div>

                    <div>
                      <span>CONFIDENCE</span>
                      <strong>{risk.confidence}</strong>
                    </div>

                    <div>
                      <span>URGENCY</span>
                      <strong>{risk.urgency}/5</strong>
                    </div>

                    <div>
                      <span>EVIDENCE STRENGTH</span>
                      <strong>{risk.evidence_strength}/3</strong>
                    </div>
                  </div>

                  <div className="risk-content">
                    <h4>Why this matters</h4>
                    <p>{risk.explanation}</p>
                  </div>

                  <div className="action-panel">
                    <span>RECOMMENDED CEO ACTION</span>
                    <p>{risk.recommended_action}</p>
                  </div>

                  <div className="uncertainty-panel">
                    <strong>What we don't know</strong>
                    <p>{risk.uncertainty}</p>
                  </div>

                  <details className="evidence-details">
                    <summary>
                      View supporting evidence ({risk.evidence.length} records)
                    </summary>

                    {risk.evidence.map((item, index) => (
                      <div
                        className="evidence-item"
                        key={`${item.citation}-${index}`}
                      >
                        <strong>{item.source}</strong>
                        <span>{item.citation}</span>
                        <p>{item.evidence}</p>
                      </div>
                    ))}
                  </details>
                </article>
              ))}
            </div>
          )}
        </section>

        <footer className="dashboard-footer">
          <span>VELOXA CEO COCKPIT</span>
          <span>
            Evidence-backed intelligence · Heuristic risk scoring
          </span>
        </footer>
      </main>
    </div>
  )
}

export default App
