"""Small reproducible *illustration* of a team project's group cuisine ranking.

This is NOT the live service ranking implementation, K-Skill client, allergy
checker, or a model trained from BC Card/eat.pl data. All input fixtures below
are fictional. Production source: BDAI9/2026-eatpl-group-venue-recommender.
"""
from __future__ import annotations

from collections import Counter


def rank_places(people: list[dict], places: list[dict]) -> dict:
    """Prioritize most-voted cuisine, then secondary fit, then sales rank.

    Input schema:
      person: {"styles": ["중식"], "budget": 15000, "atmospheres": ["조용한"],
               "allergies": ["갑각류"]}
      place: {"name": "...", "styles": ["중식"], "price": 13000,
              "atmospheres": [], "sales_rank": 20,
              "allergy_risk": {"갑각류": "unknown"|"high"|"medium"|"low"}}

    Unknown allergy information is *not* a safety guarantee.
    """
    if not people:
        raise ValueError("At least one participant is required")

    votes: Counter[str] = Counter()
    for person in people:
        votes.update(set(person.get("styles", [])))
    allergens = set().union(*(set(p.get("allergies", [])) for p in people))

    ranked = []
    excluded = []
    for place in places:
        styles = set(place.get("styles", []))
        matched = styles & set(votes)
        if votes and not matched:
            continue

        risks = place.get("allergy_risk", {})
        high = [a for a in sorted(allergens) if risks.get(a, "unknown") == "high"]
        if high:
            excluded.append({"name": place["name"], "reason": f"high risk: {', '.join(high)}"})
            continue

        priority = max((votes.get(style, 0) for style in matched), default=0)
        matched_people = sum(bool(styles & set(p.get("styles", []))) for p in people)
        budget_fit = sum(
            p.get("budget") is not None and place.get("price") is not None
            and place["price"] <= p["budget"]
            for p in people
        )
        atmosphere_fit = sum(
            bool(set(place.get("atmospheres", [])) & set(p.get("atmospheres", [])))
            for p in people
        )
        secondary = 3 * matched_people + 2 * budget_fit + atmosphere_fit
        unknown = [a for a in sorted(allergens) if risks.get(a, "unknown") == "unknown"]
        cautions = [f"Allergy information unknown: {', '.join(unknown)}"] if unknown else []
        sale = place.get("sales_rank")
        sale_sort = sale if isinstance(sale, (float, int)) and not isinstance(sale, bool) else float("inf")

        ranked.append({
            "name": place["name"],
            "cuisine_votes": priority,
            "secondary_score": secondary,
            "sales_rank": sale,
            "cautions": cautions,
            "_sort": (-priority, -secondary, sale_sort, place["name"]),
        })

    ranked.sort(key=lambda item: item["_sort"])
    for item in ranked:
        del item["_sort"]
    return {
        "votes": dict(votes),
        "results": ranked,
        "excluded": excluded,
        "message": "No eligible matching place: broaden search or verify constraints." if not ranked else "",
    }


if __name__ == "__main__":
    # Fictional fixtures, not real merchants or eat.pl data.
    participants = [
        {"styles": ["중식"], "budget": 15000, "allergies": ["갑각류"]},
        {"styles": ["중식"], "budget": 15000},
        {"styles": ["한식"], "budget": 10000, "atmospheres": ["조용한"]},
    ]
    candidates = [
        {"name": "가상 중식집", "styles": ["중식"], "price": 13000, "sales_rank": 90},
        {"name": "가상 한식집", "styles": ["한식"], "price": 8000,
         "atmospheres": ["조용한"], "sales_rank": 1},
        {"name": "가상 새우식당", "styles": ["중식"], "price": 8000,
         "allergy_risk": {"갑각류": "high"}, "sales_rank": 1},
    ]
    from pprint import pprint

    pprint(rank_places(participants, candidates), sort_dicts=False)
