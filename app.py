from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

# In-memory state simulating a Trello Board (Lists and Cards)
BOARD_STATE = {
    "name": "Project Alpha Kanban",
    "lists": [
        {
            "id": "todo",
            "title": "To Do",
            "cards": [
                {
                    "id": 1,
                    "title": "Define database schema",
                    "priority": "High",
                },
                {"id": 2, "title": "Setup OAuth2 provider", "priority": "Medium"},
            ],
        },
        {
            "id": "inprogress",
            "title": "In Progress",
            "cards": [
                {
                    "id": 3,
                    "title": "Implement core routing API",
                    "priority": "High",
                }
            ],
        },
        {
            "id": "done",
            "title": "Done",
            "cards": [
                {"id": 4, "title": "Initialize repository & CI", "priority": "Low"}
            ],
        },
    ],
}

# Counter for unique card IDs
CARD_ID_COUNTER = 5


@app.route("/")
def board():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ board.name }} - Trello Clone</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 30px; margin: 0; }
            h1 { color: #38bdf8; font-size: 24px; margin-bottom: 20px; }
            .board-container { display: flex; gap: 20px; overflow-x: auto; align-items: flex-start; padding-bottom: 20px; }
            .list-column { background: #1e293b; border-radius: 12px; width: 300px; min-width: 300px; padding: 16px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
            .list-header { font-size: 16px; font-weight: bold; color: #38bdf8; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
            .card { background: #0f172a; border-radius: 8px; padding: 12px; margin-bottom: 10px; border: 1px solid #334155; }
            .card-title { font-size: 14px; margin-bottom: 8px; color: #f8fafc; }
            .badge { font-size: 10px; padding: 2px 6px; border-radius: 4px; font-weight: bold; text-transform: uppercase; }
            .badge-High { background: #ef4444; color: #fef2f2; }
            .badge-Medium { background: #f59e0b; color: #fffbeb; }
            .badge-Low { background: #3b82f6; color: #eff6ff; }
            .card-form { margin-top: 12px; border-top: 1px solid #334155; padding-top: 12px; }
            input, select { width: 100%; box-sizing: border-box; background: #0f172a; border: 1px solid #334155; color: #f8fafc; padding: 8px; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }
            button { background: #38bdf8; color: #0f172a; border: none; padding: 8px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%; }
            button:hover { background: #0ea5e9; }
        </style>
    </head>
    <body>
        <h1>{{ board.name }}</h1>
        <div class="board-container">
            {% for lst in board.lists %}
                <div class="list-column">
                    <div class="list-header">
                        <span>{{ lst.title }}</span>
                        <span style="background: #334155; color: #94a3b8; padding: 2px 8px; border-radius: 9999px; font-size: 12px;">{{ lst.cards|length }}</span>
                    </div>
                    
                    <div class="cards-container">
                        {% for card in lst.cards %}
                            <div class="card">
                                <div class="card-title">{{ card.title }}</div>
                                <span class="badge badge-{{ card.priority }}">{{ card.priority }}</span>
                            </div>
                        {% endfor %}
                    </div>

                    <div class="card-form">
                        <form action="{{ url_for('add_card', list_id=lst.id) }}" method="POST">
                            <input type="text" name="title" placeholder="New card title..." required>
                            <select name="priority">
                                <option value="Low">Low Priority</option>
                                <option value="Medium">Medium Priority</option>
                                <option value="High">High Priority</option>
                            </select>
                            <button type="submit">Add Card</button>
                        </form>
                    </div>
                </div>
            {% endfor %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template, board=BOARD_STATE)


@app.route("/card/add/<list_id>", methods=["POST"])
def add_card(list_id):
    global CARD_ID_COUNTER
    title = request.form.get("title")
    priority = request.form.get("priority", "Medium")

    if title:
        for lst in BOARD_STATE["lists"]:
            if lst["id"] == list_id:
                lst["cards"].append(
                    {
                        "id": CARD_ID_COUNTER,
                        "title": title.strip(),
                        "priority": priority,
                    }
                )
                CARD_ID_COUNTER += 1
                break

    return redirect(url_for("board"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
