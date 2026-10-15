from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

BOARD_STATE = {
    "name": "Engineering Workspace",
    "lists": [
        {
            "id": "todo",
            "title": "To Do",
            "cards": [
                {"id": 1, "title": "Define database schema and relations", "priority": "High"},
                {"id": 2, "title": "Setup OAuth2 provider integration", "priority": "Medium"},
            ],
        },
        {
            "id": "inprogress",
            "title": "In Progress",
            "cards": [
                {"id": 3, "title": "Implement core API routing layer", "priority": "High"},
            ],
        },
        {
            "id": "done",
            "title": "Done",
            "cards": [
                {"id": 4, "title": "Initialize repository structure & CI/CD", "priority": "Low"},
            ],
        },
    ],
}

CARD_ID_COUNTER = 5

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ board.name }} — Workspace</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #f5f5f1;
    --surface: #ffffff;
    --column: #edeee8;
    --text: #30352f;
    --muted: #858980;
    --border: #dedfd7;
    --green: #687a64;
    --green-bg: #e7ece3;
    --red: #966b5c;
    --yellow: #8a7b4f;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
    font-family: "DM Sans", sans-serif;
    font-size: 13px;
    -webkit-font-smoothing: antialiased;
}

button, input, select { font: inherit; }

.topbar {
    height: 62px;
    padding: 0 5%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
}

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -0.4px;
}

.brand-mark {
    width: 29px;
    height: 29px;
    display: grid;
    place-items: center;
    background: #e9ede5;
    color: var(--green);
    border: 1px solid #dce2d6;
    border-radius: 7px;
    font-size: 15px;
}

.topbar-note {
    color: var(--muted);
    font-size: 12px;
}

main {
    max-width: 1500px;
    margin: auto;
    padding: 42px 5% 60px;
}

.heading {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 20px;
    margin-bottom: 30px;
}

.eyebrow {
    margin-bottom: 10px;
    color: var(--muted);
    font-family: "IBM Plex Mono", monospace;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

h1 {
    margin: 0;
    font-size: clamp(25px, 3vw, 32px);
    line-height: 1.25;
    font-weight: 500;
    letter-spacing: -1.1px;
}

.subtitle {
    margin: 9px 0 0;
    color: var(--muted);
    line-height: 1.6;
    font-size: 13px;
}

.summary {
    color: var(--muted);
    font-size: 12px;
    white-space: nowrap;
    padding-bottom: 3px;
}

.summary strong {
    color: var(--text);
    font-weight: 600;
}

.board {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: start;
    gap: 16px;
}

.column {
    min-width: 0;
    padding: 15px;
    background: var(--column);
    border: 1px solid #e2e3db;
    border-radius: 8px;
}

.column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    padding: 2px 1px 13px;
    border-bottom: 1px solid #dcded5;
}

.column-title {
    display: flex;
    align-items: center;
    gap: 9px;
    font-weight: 600;
    font-size: 13px;
}

.dot {
    width: 7px;
    height: 7px;
    flex-shrink: 0;
    border-radius: 50%;
    background: #a5a99e;
}

.column[data-id="inprogress"] .dot { background: #a58d64; }
.column[data-id="done"] .dot { background: #80977a; }

.count {
    min-width: 23px;
    padding: 4px 6px;
    text-align: center;
    border: 1px solid #dedfd7;
    border-radius: 5px;
    background: #f7f7f3;
    color: #777c72;
    font-family: "IBM Plex Mono", monospace;
    font-size: 10px;
}

.cards {
    display: flex;
    flex-direction: column;
    gap: 9px;
}

.card {
    padding: 13px 13px 11px;
    background: var(--surface);
    border: 1px solid #e5e5df;
    border-radius: 6px;
    transition: border-color .15s, transform .15s;
}

.card:hover {
    border-color: #c8cdc1;
    transform: translateY(-1px);
}

.card-title {
    margin-bottom: 16px;
    font-size: 13px;
    font-weight: 500;
    line-height: 1.65;
    overflow-wrap: anywhere;
}

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 9px;
    padding-top: 10px;
    border-top: 1px solid #f0f0eb;
}

.priority {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 7px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 600;
}

.priority::before {
    content: "";
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: currentColor;
}

.High { background: #f2e9e5; color: var(--red); }
.Medium { background: #f1eee2; color: var(--yellow); }
.Low { background: #e8eee5; color: var(--green); }

.actions {
    display: flex;
    gap: 11px;
    align-items: center;
}

.action {
    color: #777d73;
    font-size: 11px;
    font-weight: 500;
    text-decoration: none;
}

.action:hover { color: var(--green); }
.action.delete:hover { color: var(--red); }

.empty {
    padding: 18px 10px;
    border: 1px dashed #d4d7cd;
    border-radius: 6px;
    color: var(--muted);
    text-align: center;
    font-size: 12px;
}

.add-form {
    margin-top: 15px;
    padding-top: 13px;
    border-top: 1px solid #dcded5;
}

.add-form input,
.add-form select {
    display: block;
    width: 100%;
    min-height: 36px;
    margin-bottom: 8px;
    padding: 8px 10px;
    border: 1px solid #dedfd7;
    border-radius: 5px;
    outline: none;
    background: #f8f8f4;
    color: var(--text);
    font-size: 12px;
}

.add-form input::placeholder { color: #989c92; }

.add-form input:focus,
.add-form select:focus { border-color: #9da995; }

.add-form button {
    width: 100%;
    min-height: 35px;
    border: 1px solid #d9ded3;
    border-radius: 5px;
    background: #e5e9df;
    color: #52644e;
    font-weight: 600;
    font-size: 12px;
    cursor: pointer;
}

.add-form button:hover { background: #dce3d5; }

@media (max-width: 900px) {
    main { padding: 30px 22px; }
    .board {
        grid-template-columns: repeat(3, minmax(255px, 1fr));
        overflow-x: auto;
    }
}

@media (max-width: 600px) {
    .topbar { height: 56px; padding: 0 17px; }
    main { padding: 27px 16px 40px; }
    .heading { align-items: flex-start; flex-direction: column; gap: 12px; }
    .board { grid-template-columns: minmax(0, 1fr); gap: 13px; }
    .column { padding: 13px; }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        transition: none !important;
        transform: none !important;
    }
}
</style>
</head>

<body>
<header class="topbar">
    <div class="brand">
        <span class="brand-mark">n.</span>
        <span>workspace</span>
    </div>
    <span class="topbar-note">Engineering / Projects</span>
</header>

<main>
    <section class="heading">
        <div>
            <div class="eyebrow">PROJECT BOARD / 001</div>
            <h1>{{ board.name }}</h1>
            <p class="subtitle">Keep track of work, priorities, and progress.</p>
        </div>

        <div class="summary">
            <strong>{{ board.lists|length }}</strong> sections
            &nbsp;·&nbsp;
            <strong>{{ board.lists|map(attribute='cards')|map('length')|sum }}</strong> tasks
        </div>
    </section>

    <section class="board">
        {% for lst in board.lists %}
        <div class="column" data-id="{{ lst.id }}">
            <div class="column-header">
                <div class="column-title">
                    <span class="dot"></span>
                    <span>{{ lst.title }}</span>
                </div>
                <span class="count">{{ lst.cards|length }}</span>
            </div>

            <div class="cards">
                {% for card in lst.cards %}
                <article class="card">
                    <div class="card-title">{{ card.title }}</div>
                    <div class="card-footer">
                        <span class="priority {{ card.priority }}">
                            {{ card.priority }}
                        </span>

                        <div class="actions">
                            {% if not loop.last or lst.id != board.lists[-1].id %}
                            <a class="action"
                               href="{{ url_for('move_card', current_list_id=lst.id, card_id=card.id) }}">
                                Move →
                            </a>
                            {% endif %}
                            <a class="action delete"
                               href="{{ url_for('delete_card', list_id=lst.id, card_id=card.id) }}">
                                Delete
                            </a>
                        </div>
                    </div>
                </article>
                {% else %}
                <div class="empty">Nothing here yet</div>
                {% endfor %}
            </div>

            <form class="add-form"
                  action="{{ url_for('add_card', list_id=lst.id) }}"
                  method="POST">
                <input type="text" name="title"
                       placeholder="Add a task..."
                       maxlength="200" required autocomplete="off">
                <select name="priority">
                    <option value="Low">Low priority</option>
                    <option value="Medium" selected>Medium priority</option>
                    <option value="High">High priority</option>
                </select>
                <button type="submit">Add task +</button>
            </form>
        </div>
        {% endfor %}
    </section>
</main>
</body>
</html>
"""


@app.route("/")
def board():
    return render_template_string(HTML, board=BOARD_STATE)


@app.route("/card/add/<list_id>", methods=["POST"])
def add_card(list_id):
    global CARD_ID_COUNTER

    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "Medium")

    if not title:
        return redirect(url_for("board"))

    if priority not in {"Low", "Medium", "High"}:
        priority = "Medium"

    for lst in BOARD_STATE["lists"]:
        if lst["id"] == list_id:
            lst["cards"].append({
                "id": CARD_ID_COUNTER,
                "title": title,
                "priority": priority,
            })
            CARD_ID_COUNTER += 1
            break

    return redirect(url_for("board"))


@app.route("/card/move/<current_list_id>/<int:card_id>")
def move_card(current_list_id, card_id):
    lists = BOARD_STATE["lists"]

    for i, lst in enumerate(lists):
        if lst["id"] != current_list_id:
            continue

        if i + 1 >= len(lists):
            break

        card = next(
            (c for c in lst["cards"] if c["id"] == card_id),
            None,
        )

        if card:
            lst["cards"].remove(card)
            lists[i + 1]["cards"].append(card)

        break

    return redirect(url_for("board"))


@app.route("/card/delete/<list_id>/<int:card_id>")
def delete_card(list_id, card_id):
    for lst in BOARD_STATE["lists"]:
        if lst["id"] == list_id:
            lst["cards"] = [
                card for card in lst["cards"]
                if card["id"] != card_id
            ]
            break

    return redirect(url_for("board"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
