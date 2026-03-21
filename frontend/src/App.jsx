import { useState } from 'react';
import './index.css';

function App() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    async function runScenario() {
        setError(null);
        setLoading(true);
        try {
            const resp = await fetch('/api/run-scenario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ scenario: 'sfb/data/scenarios/scenario_1.yaml', max_turns: 20 }),
            });

            if (!resp.ok) {
                throw new Error('API error ' + resp.status);
            }

            const data = await resp.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
            setResult(null);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="app">
            <header>
                <h1>Star Fleet Battles Web UI</h1>
                <p>React-based scenario runner for SFB simulator backend.</p>
            </header>

            <main>
                <button onClick={runScenario} disabled={loading}>
                    {loading ? 'Running...' : 'Run Scenario'}
                </button>

                {error && <div className="error">Error: {error}</div>}

                {result && (
                    <section className="result">
                        <h2>{result.scenario}</h2>
                        <p>{result.description}</p>
                        <p>
                            <strong>{result.result_message}</strong>
                        </p>

                        <h3>Game Events</h3>
                        <ul>
                            {result.events.map((evt, idx) => (
                                <li key={idx}>{`${evt.turn}.${evt.impulse}: ${evt.event_type} - ${evt.actor}`}</li>
                            ))}
                        </ul>

                        <h3>Map Snapshots</h3>
                        {result.snapshots.map((snap, idx) => (
                            <pre key={idx}>{`${snap.turn}.${snap.impulse} (${snap.phase}) \n${JSON.stringify(snap.entities, null, 2)}`}</pre>
                        ))}

                        <h3>Full Log</h3>
                        <pre>{result.full_log}</pre>
                    </section>
                )}
            </main>

            <footer>
                <small>Backend web API: /api/run-scenario</small>
            </footer>
        </div>
    );
}

export default App;
