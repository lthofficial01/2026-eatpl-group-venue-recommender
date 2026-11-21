"""Regression examples for the standalone illustrative ranking model."""
import unittest

from examples.group_ranker import rank_places


class GroupRankerTests(unittest.TestCase):
    def test_two_chinese_votes_beat_one_korean_even_with_budget_and_sales_advantage(self):
        people = [
            {"styles": ["중식"], "budget": 13000},
            {"styles": ["중식"], "budget": 13000},
            {"styles": ["한식"], "budget": 8000, "atmospheres": ["조용한"]},
        ]
        places = [
            {"name": "한식", "styles": ["한식"], "price": 7000,
             "atmospheres": ["조용한"], "sales_rank": 1},
            {"name": "중식", "styles": ["중식"], "price": 14000, "sales_rank": 99},
        ]
        result = rank_places(people, places)
        self.assertEqual(result["votes"], {"중식": 2, "한식": 1})
        self.assertEqual(result["results"][0]["name"], "중식")
        self.assertEqual(result["results"][0]["cuisine_votes"], 2)

    def test_allergy_high_exclusion_overrides_vote_priority(self):
        people = [{"styles": ["중식"], "allergies": ["갑각류"]},
                  {"styles": ["중식"]}, {"styles": ["한식"]}]
        places = [
            {"name": "새우 중식", "styles": ["중식"],
             "allergy_risk": {"갑각류": "high"}, "sales_rank": 1},
            {"name": "한식", "styles": ["한식"], "sales_rank": 50},
        ]
        result = rank_places(people, places)
        self.assertEqual([r["name"] for r in result["results"]], ["한식"])
        self.assertEqual(result["excluded"][0]["name"], "새우 중식")

    def test_tied_votes_use_secondary_score(self):
        people = [{"styles": ["중식"], "budget": 8000},
                  {"styles": ["한식"], "budget": 8000}]
        places = [
            {"name": "중식", "styles": ["중식"], "price": 15000, "sales_rank": 1},
            {"name": "한식", "styles": ["한식"], "price": 7000, "sales_rank": 99},
        ]
        self.assertEqual(rank_places(people, places)["results"][0]["name"], "한식")

    def test_unknown_allergy_is_warned_not_marked_safe(self):
        people = [{"styles": ["중식"], "allergies": ["갑각류"]}]
        result = rank_places(people, [{"name": "중식", "styles": ["중식"]}])
        self.assertIn("unknown", result["results"][0]["cautions"][0].lower())

    def test_no_matching_or_safe_candidate(self):
        people = [{"styles": ["중식"], "allergies": ["갑각류"]}]
        candidates = [{"name": "중식", "styles": ["중식"],
                       "allergy_risk": {"갑각류": "high"}}]
        result = rank_places(people, candidates)
        self.assertEqual(result["results"], [])
        self.assertTrue(result["message"])

    def test_empty_people_rejected(self):
        with self.assertRaises(ValueError):
            rank_places([], [{"name": "가상 매장", "styles": ["중식"]}])

    def test_multiple_cuisine_tags_cannot_sum_two_votes_twice(self):
        people = [{"styles": ["한식", "중식"]}, {"styles": ["중식"]}]
        places = [{"name": "복합", "styles": ["한식", "중식"]},
                  {"name": "중식", "styles": ["중식"]}]
        result = rank_places(people, places)
        self.assertEqual(result["results"][0]["cuisine_votes"], 2)
        self.assertEqual(result["results"][1]["cuisine_votes"], 2)


if __name__ == "__main__":
    unittest.main()
