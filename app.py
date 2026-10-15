from datetime import datetime
import os
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simulated system state reflecting a real deployment artifact
DEPLOYMENT_INFO = {
    "version": "2.1.0-release",
    "environment": os.getenv("FLASK_ENV", "production"),
    "deployed_at": datetime.utcnow().isoformat(),
    "status": "healthy",
    "active_services": [
        "auth-gateway",
        "transaction-processor",
        "notification-worker",
    ],
}


@app.route("/")
def dashboard():
  html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Pipeline Status Dashboard</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; margin: 0; }
            .card { background: #1e293b; border-radius: 12px; padding: 24px; max-width: 600px; margin: auto; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
            h1 { color: #38bdf8; font-size: 24px; margin-top: 0; }
            .status-badge { display: inline-block; background: #22c55e; color: #052e16; padding: 4px 12px; border-radius: 9999px; font-weight: bold; font-size: 14px; }
            ul { padding-left: 20px; }
            li { margin-bottom: 8px; color: #cbd5e1; }
            .meta { margin-top: 20px; font-size: 12px; color: #94a3b8; border-top: 1px solid #334155; padding-top: 12px; }
            code { background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #38bdf8; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Pipeline Status Dashboard</h1>
            <p>System State: <span class="status-badge">{{ info.status.upper() }}</span></p>
            <p><strong>Version:</strong> <code>{{ info.version }}</code></p>
            <p><strong>Environment:</strong> {{ info.environment }}</p>
            <p><strong>Active Services:</strong></p>
            <ul>
                {% for service in info.active_services %}
                    <li>{{ service }}</li>
                {% endfor %}
            </ul>
            <div class="meta">Deployed at: {{ info.deployed_at }} UTC</div>
        </div>
    </body>
    </html>
    """
  return render_template_string(html_template, info=DEPLOYMENT_INFO)


@app.route("/api/health")
def health_check():
  """Dedicated health-check endpoint for automated CI/CD post-deployment verification."""
  return jsonify(DEPLOYMENT_INFO), 200


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=False)
