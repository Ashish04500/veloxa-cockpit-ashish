
import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [risks, setRisks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [lastUpdated, setLastUpdated] = useState(null)
  const [apiConnected, setApiConnected] = useState(false)
  const [question, setQuestion] = useState('')
  const [asking, setAsking] = useState(false)
  const [answerResult, setAnswerResult] = useState(null)
  const [askError, setAskError] = useState('')
  const [selectedRiskEvidence, setSelectedRiskEvidence] = useState(null)

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

  async function submitQuestion(event) {
    event.preventDefault()

    const trimmedQuestion = question.trim()
    if (!trimmedQuestion || asking) return

    setAsking(true)
    setAskError('')
    setAnswerResult(null)

    try {
      const response = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: trimmedQuestion }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || `Request failed: ${response.status}`)
      }

      setAnswerResult(data)
    } catch (err) {
      setAskError(err.message || 'Unable to get an answer.')
    } finally {
      setAsking(false)
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

        <section className="assistant-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">EVIDENCE-GROUNDED Q&A</p>
              <h2>Ask the CEO Intelligence Assistant</h2>
              <p className="subtitle">
                Ask about business decisions, operational risks and supporting records.
              </p>
            </div>
          </div>

          <form className="assistant-form" onSubmit={submitQuestion}>
            <textarea
              value={question}
              onChange={event => setQuestion(event.target.value)}
              placeholder="Example: What does Pria's reported resignation mean for Version 3?"
              maxLength={1000}
              rows={3}
              disabled={asking}
            />
            <div className="assistant-form-footer">
              <span>{question.length}/1000 characters</span>
              <button
                type="submit"
                disabled={asking || !question.trim()}
              >
                {asking ? 'Analyzing evidence...' : 'Ask question'}
              </button>
            </div>
          </form>

          {asking && (
            <p className="message">Searching approved evidence and preparing an answer...</p>
          )}

          {askError && (
            <div className="assistant-error">
              <strong>Unable to answer</strong>
              <p>{askError}</p>
            </div>
          )}

          {answerResult && (
            <div className="assistant-result">
              <div className="assistant-result-header">
                <span className="assistant-status">
                  {(answerResult.status || 'unknown').replaceAll('_', ' ').toUpperCase()}
                </span>
                {answerResult.confidence && (
                  <span className="assistant-confidence">
                    CONFIDENCE: {answerResult.confidence}
                  </span>
                )}
              </div>

              <div className="assistant-answer">
                <h3>Assessment</h3>
                <p>
                  {answerResult.answer ||
                    answerResult.reason ||
                    answerResult.message ||
                    'No answer text was returned.'}
                </p>
              </div>

              {answerResult.evidence?.length > 0 && (
                <details className="evidence-details">
                  <summary>
                    Supporting evidence ({answerResult.evidence.length} records)
                  </summary>

                  {answerResult.evidence.map((item, index) => (
                    <div
                      className="evidence-item"
                      key={`${item.source || 'source'}-${index}`}
                    >
                      <details>
                        <summary className="evidence-source-link">
                          {item.source || 'Source record'}
                        </summary>
                        <div className="evidence-meta">
                          {item.citation && <span>{item.citation}</span>}
                          <span>
                            {item.release_day || 'Release day unavailable'}
                            {item.location ? ` | ${item.location}` : ''}
                          </span>
                        </div>
                        <p>
                          {item.excerpt || item.evidence || item.text ||
                            'Evidence excerpt unavailable.'}
                        </p>
                      </details>
                    </div>
                  ))}

                </details>
              )}

              {answerResult.status === 'insufficient_evidence' && (
                <p className="assistant-note">
                  The available approved records are not sufficient to support this answer.
                </p>
              )}

              {answerResult.status === 'refused' && (
                <p className="assistant-note">
                  This request cannot be answered under the cockpit's privacy safeguards.
                </p>
              )}
            </div>
          )}
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
                      <span>HEURISTIC SCORE</span>
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

                  <p className="risk-method-note">
                    Rule-based prioritisation score, not a probability.
                    Evidence strength counts distinct source files, not
                    independent corroboration.
                  </p>

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
                        <button
                          type="button"
                          className="evidence-source-link"
                          aria-expanded={selectedRiskEvidence === item}
                          onClick={() =>
                            setSelectedRiskEvidence(current =>
                              current === item ? null : item
                            )
                          }
                        >
                          {item.source || 'Source record'}
                        </button>
                        <span>{item.citation}</span>
                        <p>{item.evidence}</p>
                      </div>
                    ))}

                    {selectedRiskEvidence && (
                      <div className="evidence-preview">
                        <div className="evidence-preview-header">
                          <strong>Evidence preview</strong>
                          <button
                            type="button"
                            onClick={() => setSelectedRiskEvidence(null)}
                          >
                            Close
                          </button>
                        </div>
                        <span>{selectedRiskEvidence.citation}</span>
                        <pre>
                          {selectedRiskEvidence.evidence ||
                            'Evidence excerpt unavailable.'}
                        </pre>
                        <p>
                          This is the evidence excerpt attached to this risk,
                          not the complete original source file.
                        </p>
                      </div>
                    )}
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
