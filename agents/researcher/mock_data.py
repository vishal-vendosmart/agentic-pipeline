#!/usr/bin/env python3
"""
Mock DataForSEO responses for testing when API is not available
"""

import json
from datetime import datetime

def get_mock_keyword_data():
    """Return realistic mock keyword research data"""
    
    return {
        'suggestions': [
            {'keyword': 'AI procurement software', 'location_code': 2840, 'language_code': 'en', 'search_volume': 2400, 'cpc': 12.50, 'competition': 0.45, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 2400}]},
            {'keyword': 'procurement automation software', 'location_code': 2840, 'language_code': 'en', 'search_volume': 880, 'cpc': 10.20, 'competition': 0.38, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 880}]},
            {'keyword': 'AI purchasing system', 'location_code': 2840, 'language_code': 'en', 'search_volume': 590, 'cpc': 11.80, 'competition': 0.42, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 590}]},
            {'keyword': 'smart procurement tools', 'location_code': 2840, 'language_code': 'en', 'search_volume': 720, 'cpc': 9.50, 'competition': 0.35, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 720}]},
            {'keyword': 'manufacturing automation software', 'location_code': 2840, 'language_code': 'en', 'search_volume': 1900, 'cpc': 14.30, 'competition': 0.52, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 1900}]},
            {'keyword': 'AI in procurement', 'location_code': 2840, 'language_code': 'en', 'search_volume': 1600, 'cpc': 8.90, 'competition': 0.40, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 1600}]},
            {'keyword': 'procurement software for SMEs', 'location_code': 2840, 'language_code': 'en', 'search_volume': 390, 'cpc': 13.20, 'competition': 0.28, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 390}]},
            {'keyword': 'automated purchasing software', 'location_code': 2840, 'language_code': 'en', 'search_volume': 480, 'cpc': 10.80, 'competition': 0.33, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 480}]},
            {'keyword': 'AI sourcing tools', 'location_code': 2840, 'language_code': 'en', 'search_volume': 320, 'cpc': 11.40, 'competition': 0.30, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 320}]},
            {'keyword': 'intelligent procurement', 'location_code': 2840, 'language_code': 'en', 'search_volume': 1100, 'cpc': 9.70, 'competition': 0.37, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 1100}]},
            {'keyword': 'procurement AI platform', 'location_code': 2840, 'language_code': 'en', 'search_volume': 260, 'cpc': 12.90, 'competition': 0.25, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 260}]},
            {'keyword': 'machine learning procurement', 'location_code': 2840, 'language_code': 'en', 'search_volume': 540, 'cpc': 10.50, 'competition': 0.36, 'monthly_searches': [{'year': 2026, 'month': 7, 'search_volume': 540}]},
        ],
        'difficulty': [
            {'keyword': 'AI procurement software', 'keyword_difficulty': 45, 'serp_features': ['featured_snippet', 'people_also_ask']},
            {'keyword': 'procurement automation software', 'keyword_difficulty': 38, 'serp_features': ['people_also_ask']},
            {'keyword': 'AI purchasing system', 'keyword_difficulty': 42, 'serp_features': ['featured_snippet']},
            {'keyword': 'smart procurement tools', 'keyword_difficulty': 35, 'serp_features': []},
            {'keyword': 'manufacturing automation software', 'keyword_difficulty': 52, 'serp_features': ['people_also_ask', 'videos']},
            {'keyword': 'AI in procurement', 'keyword_difficulty': 40, 'serp_features': ['featured_snippet', 'people_also_ask']},
            {'keyword': 'procurement software for SMEs', 'keyword_difficulty': 28, 'serp_features': []},
            {'keyword': 'automated purchasing software', 'keyword_difficulty': 33, 'serp_features': ['people_also_ask']},
            {'keyword': 'AI sourcing tools', 'keyword_difficulty': 30, 'serp_features': []},
            {'keyword': 'intelligent procurement', 'keyword_difficulty': 37, 'serp_features': ['people_also_ask']},
            {'keyword': 'procurement AI platform', 'keyword_difficulty': 25, 'serp_features': []},
            {'keyword': 'machine learning procurement', 'keyword_difficulty': 36, 'serp_features': ['people_also_ask', 'videos']},
        ]
    }

if __name__ == '__main__':
    data = get_mock_keyword_data()
    print(json.dumps(data, indent=2))
