from langchain.tools import tool
import requests

# Replace with your actual API keys
SERPAPI_API_KEY = "2b832ce5d6c917c07478b99498d34635404eef913d7e0cee5dd81612fff8380b"
GOOGLE_PLACES_API_KEY = "AIzaSyDaSGtnyYjLHA7zv2uXU6BXN2YvgWyfj0c"

@tool
def search_competitors_enhanced(location: str) -> str:
    """
    Searches for clothing store competitors in the given location using SerpAPI and Google Places API.
    """
    def _try_serpapi_search(location: str) -> str:
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": f"clothing stores in {location}",
            "api_key": SERPAPI_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("organic_results", [])
            if results:
                return "\n".join(f"- {item['title']}" for item in results[:5])
        return "No results from SerpAPI."

    def _try_google_places_search(location: str) -> str:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"clothing stores in {location}",
            "key": GOOGLE_PLACES_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                return "\n".join(f"- {item['name']} ({item['formatted_address']})" for item in results[:5])
        return "No results from Google Places API."

    # Try SerpAPI first, fallback to Google Places
    serpapi_result = _try_serpapi_search(location)
    if "No results" not in serpapi_result:
        return f"🧵 Top Competitors from Google Search:\n{serpapi_result}"

    google_result = _try_google_places_search(location)
    return f"🧵 Top Competitors from Google Places:\n{google_result}"


@tool
def generate_market_analysis(location: str) -> str:
    """
    Generates a market analysis for a clothing store in the given location.
    """
    return f"""
📊 Market Analysis for Clothing Store in {location}:

- 📍 Prime Areas: MG Road, Commercial Street, Indiranagar (adjust as per real data)
- 🧍‍♂️ Target: Young professionals, students, tourists
- 💸 Rent Estimate: ₹100–150/sqft in high-footfall areas
- 🛍️ High Competition: Reliance Trends, FabIndia, Biba, H&M
- 🌱 Gaps: Affordable sustainable fashion, gender-neutral clothing
- 📈 Opportunity: Mid-range brands, vernacular fashion trends, social media marketing
    """.strip()


@tool
def get_location_insights(location: str) -> str:
    """
    Provides location insights like traffic, crowd type, and business environment.
    """
    insights = {
        "Bangalore": {
            "foot_traffic": "Very High in Indiranagar, Koramangala, MG Road",
            "demographics": "Young professionals, tech workers, students",
            "business_trend": "Booming in fashion and food retail"
        },
        "Chennai": {
            "foot_traffic": "High in T Nagar, Nungambakkam",
            "demographics": "Families, working professionals",
            "business_trend": "Steady growth, traditional + western fusion"
        }
        # Add more cities as needed
    }

    data = insights.get(location, {
        "foot_traffic": "Unknown",
        "demographics": "Unknown",
        "business_trend": "Unknown"
    })

    return f"""
📍 Location: {location}
🚶 Foot Traffic: {data['foot_traffic']}
👥 Demographics: {data['demographics']}
📈 Business Environment: {data['business_trend']}
    """.strip()
