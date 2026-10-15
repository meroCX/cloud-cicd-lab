from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

# In-memory state simulating a Trello Board
BOARD_STATE = {
    "name": "Engineering Workspace",
    "lists": [
        {
            "id": "todo",
            "title": "To Do",
            "cards": [
                {
                    "id": 1,
                    "title": "Define database schema and relations",
                    "priority": "High",
                },
                {
                    "id": 2,
                    "title": "Setup OAuth2 provider integration",
                    "priority": "Medium",
                },
            ],
        },
        {
            "id": "inprogress",
            "title": "In Progress",
            "cards": [
                {
                    "id": 3,
                    "title": "Implement core API routing layer",
                    "priority": "High",
                }
            ],
        },
        {
            "id": "done",
            "title": "Done",
            "cards": [
                {
                    "id": 4,
                    "title": "Initialize repository structure & CI/CD",
                    "priority": "Low",
                }
            ],
        },
    ],
}

CARD_ID_COUNTER = 5


@app.route("/")
def board():
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ board.name }} | Trello</title>
        <style>
            * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Noto Sans, Ubuntu, sans-serif; }
            body { background-color: #0079bf; margin: 0; padding: 0; height: 100vh; display: flex; flex-direction: column; color: #172b4d; }
            
            /* Navbar */
            header { background: rgba(0,0,0,0.15); padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; }
            h1 { margin: 0; font-size: 18px; font-weight: 700; color: #ffffff; }

            /* Board Layout */
            .board-container { display: flex; align-items: flex-start; gap: 12px; padding: 20px; overflow-x: auto; flex-grow: 1; }
            
            /* Column Design */
            .list-column { background-color: #f1f2f4; border-radius: 12px; width: 280px; min-width: 280px; max-height: 100%; display: flex; flex-direction: column; padding: 12px; box-shadow: 0px 1px 1px #091e4226, 0px 0px 1px #091e420f; }
            .list-header { font-size: 14px; font-weight: 600; color: #172b4d; padding: 4px 8px 12px 8px; display: flex; justify-content: space-between; align-items: center; }
            .card-count { background: #091e420f; color: #44546f; font-size: 12px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }

            /* Card Design */
            .cards-container { display: flex; flex-direction: column; gap: 8px; overflow-y: auto; padding: 2px; }
            .card { background: #ffffff; border-radius: 8px; padding: 8px 12px; box-shadow: 0px 1px 1px #091e4226, 0px 0px 1px #091e420f; transition: background 0.1s ease; border: 2px solid transparent; }
            .card:hover { border-color: #388bfc; }
            .card-title { font-size: 14px; line-height: 20px; color: #172b4d; font-weight: 400; word-break: break-word; margin-bottom: 8px; }
            
            /* Badges & Actions */
            .card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 4px; }
            .badge { font-size: 11px; font-weight: 600; padding: 2px 6px; border-radius: 4px; display: inline-block; }
            .badge-High { background: #ffebe6; color: #c11000; }
            .badge-Medium { background: #fffae6; color: #7f5f00; }
            .badge-Low { background: #e6fcff; color: #006644; }

            .card-actions { display: flex; gap: 4px; }
            .btn-action { text-decoration: none; font-size: 11px; font-weight: 500; padding: 4px 8px; border-radius: 4px; color: #44546f; background: #091e420f; transition: background 0.15s, color 0.15s; }
            .btn-action:hover { background: #091e4214; color: #172b4d; }
            .btn-delete:hover { background: #ffebe6; color: #ae2e24; }

            /* Card Form */
            .card-form { margin-top: 12px; border-top: 1px solid #091e4214; padding-top: 12px; }
            input, select { width: 100%; box-sizing: border-box; background: #ffffff; border: 1px solid #8590a2; color: #172b4d; padding: 8px; border-radius: 4px; margin-bottom: 8px; font-size: 13px; outline: none; }
            input:focus, select:focus { border-color: #388bfc; }
            button[type="submit"] { background: #0c66e4; color: #ffffff; border: none; padding: 8px 12px; border-radius: 4px; font-weight: 600; font-size: 13px; cursor: pointer; width: 100%; transition: background 0.15s ease; }
            button[type="submit"]:hover { background: #0055cc; }
        </style>
    </head>
    <body>
        <header>
            <h1>{{ board.name }}</h1>
        </header>

        <div class="board-container">
            {% for lst in board.lists %}
                <div class="list-column">
                    <div class="list-header">
                        <span>{{ lst.title }}</span>
                        <span class="card-count">{{ lst.cards|length }}</span>
                    </div>
                    
                    <div class="cards-container">
                        {% for card in lst.cards %}
                            <div class="card">
                                <div class="card-title">{{ card.title }}</div>
                                <div class="card-footer">
                                    <span class="badge badge-{{ card.priority }}">{{ card.priority }}</span>
                                    <div class="card-actions">
                                        {% if loop.index0 < board.lists|length - 1 %}
                                            <a href="{{ url_for('move_card', current_list_id=lst.id, card_id=card.id) }}" class="btn-action" title="Move to next section">Move &rarr;</a>
                                        {% endif %}
                                        <a href="{{ url_for('delete_card', list_id=lst.id, card_id=card.id) }}" class="btn-action btn-delete" title="Delete card">Delete</a>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    </div>

                    <div class="card-form">
                        <form action="{{ url_for('add_card', list_id=lst.id) }}" method="POST">
                            <input type="text" name="title" placeholder="+ Add a card..." required autocomplete="off">
                            <select name="priority">
                                <option value="Low">Low Priority</option>
                                <option value="Medium" selected>Medium Priority</option>
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


@app.route("/card/move/<current_list_id>/<int:card_id>")
def move_card(current_list_id, card_id):
    lists = BOARD_STATE["lists"]
    target_card = None
    source_list = None

    for i, lst in enumerate(lists):
        if lst["id"] == current_list_id:
            source_list = lst
            for card in lst["cards"]:
                if card["id"] == card_id:
                    target_card = card
                    break
        if target_card:
            if i + 1 < len(lists):
                next_list = lists[i + 1]
                source_list["cards"].remove(target_card)
                next_list["cards"].append(target_card)
            break

    return redirect(url_for("board"))


@app.route("/card/delete/<list_id>/<int:card_id>")
def delete_card(list_id, card_id):
    for lst in BOARD_STATE["lists"]:
        if lst["id"] == list_id:
            lst["cards"] = [c for c in lst["cards"] if c["id"] != card_id]
            break

    return redirect(url_for("board"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
