"""Flask service wrapper for Star Fleet Battles simulator.

Run with:
  python webapp.py

Then open http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
from app import run_scenario_data
import os

app = Flask(__name__, static_folder='frontend/dist', static_url_path='')


@app.route('/api/run-scenario', methods=['GET', 'POST'])
def api_run_scenario():
    # POST expects JSON body; GET supports simple query params for quick browser usage
    if request.method == 'GET':
        scenario = request.args.get(
            'scenario', 'sfb/data/scenarios/scenario_1.yaml')
        max_turns = int(request.args.get('max_turns', 20))
    else:
        payload = request.get_json(force=True, silent=True) or {}
        scenario = payload.get(
            'scenario', 'sfb/data/scenarios/scenario_1.yaml')
        max_turns = int(payload.get('max_turns', 20))

    data = run_scenario_data(scenario, max_turns=max_turns)
    return jsonify(data)


@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({'status': 'ok', 'message': 'SFB backend is healthy'})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    # Production deploy serves built files from frontend/dist
    if app.static_folder and os.path.exists(app.static_folder):
        if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        index_file = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_file):
            return send_from_directory(app.static_folder, 'index.html')

    # Fallback during development when dist is not built
    return '''
<html><body>
<h1>SFB Web UI (not built)</h1>
<p>Frontend build not found at <code>frontend/dist</code>.</p>
<p>Run <code>cd frontend && npm install && npm run build</code>, then refresh.</p>
<p>Or use <code>npm run dev</code> from <code>frontend/</code> and open the Vite URL.</p>
</body></html>'''


if __name__ == '__main__':
    print('Starting SFB web service on http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
