import random
from langchain_core.tools import StructuredTool, Tool
from langchain_community.tools import DuckDuckGoSearchRun
from huggingface_hub import list_models
from retriever import extract_guest_info

# 1. Guest RAG Tool (Using StructuredTool to handle multi-argument inputs gracefully)
guest_info_tool = StructuredTool.from_function(
    func=extract_guest_info,
    name="guest_info_retriever",
    description="Retrieves detailed information about gala guests based on their name, relation, or description query."
)

# 2. Web Search Tool
search_tool = DuckDuckGoSearchRun()

# 3. Weather Info Tool
def get_weather_info(location: str) -> str:
    """Fetches dummy weather information for a given location."""
    weather_conditions = [
        {"condition": "Rainy", "temp_c": 15},
        {"condition": "Clear", "temp_c": 25},
        {"condition": "Windy", "temp_c": 20}
    ]
    data = random.choice(weather_conditions)
    return f"Weather in {location}: {data['condition']}, {data['temp_c']}°C"

weather_info_tool = Tool(
    name="get_weather_info",
    func=get_weather_info,
    description="Fetches dummy weather information for a given location."
)

# 4. Hugging Face Hub Stats Tool
def get_hub_stats(author: str) -> str:
    """Fetches the most downloaded model from a specific author on the Hugging Face Hub."""
    try:
        models = list(list_models(author=author, sort="downloads", direction=-1, limit=1))
        if models:
            model = models[0]
            return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
        return f"No models found for author {author}."
    except Exception as e:
        return f"Error fetching models for {author}: {str(e)}"

hub_stats_tool = Tool(
    name="get_hub_stats",
    func=get_hub_stats,
    description="Fetches the most downloaded model from a specific author on the Hugging Face Hub."
)