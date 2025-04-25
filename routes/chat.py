from fastapi import APIRouter
from pathlib import Path
import csv, random

router = APIRouter()
DATA_DIR = Path("data")
TEMPLATE_ID = "tmpl_varpair_v1"

def safe_load_csv(name):
    try:
        with open(DATA_DIR / f"{name}.csv", newline='', encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []

events = safe_load_csv("events")
true_causes = safe_load_csv("true_causes")
false_causes = safe_load_csv("false_causes")
templates_raw = safe_load_csv("templates")
templates = {row["tmpl_id"]: row for row in templates_raw} if templates_raw else {}

def pick_by_theme(rows, theme, k=1):
    pool = [r for r in rows if r["theme"] == theme]
    return random.sample(pool, k) if len(pool) >= k else []

def generate_task(tmpl_id=TEMPLATE_ID):
    if tmpl_id not in templates:
        return {"error": f"Template {tmpl_id} not found"}

    t = templates[tmpl_id]
    if not events or not true_causes or not false_causes:
        return {"error": "One or more CSV files are missing or empty"}

    ev_row = random.choice(events)
    theme = ev_row["theme"]
    good = pick_by_theme(true_causes, theme, k=2)
    bad_list = pick_by_theme(false_causes, theme, k=1)

    if len(good) < 2 or not bad_list:
        return {"error": "Not enough causes for theme"}

    bad = bad_list[0]
    variants = [good[0]["cause"], good[1]["cause"], bad["cause"]]
    random.shuffle(variants)
    correct_idx = variants.index(bad["cause"])

    return {
        "branch_id": t["branch_id"],
        "question": t["arrow_pattern"].format(event=ev_row["event"]),
        "buttons": variants,
        "correct": correct_idx,
        "commentary": t["commentary"].format(false=bad["cause"]),
        "bloom": t["bloom_level"],
        "fishbi": t["fishbi_lvl"]
    }

@router.get("/next-task")
async def next_task():
    return generate_task()
