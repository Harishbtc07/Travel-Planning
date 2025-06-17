from crewai import Agent
from tools import search_tool, scrape_tool, currency_tool

def create_agents(destination: str, budget_usd: int, trip_days: int):
    researcher = Agent(
        role="Destination Researcher",
        goal=f"Research cultural attractions and travel trends in {destination} for 2025",
        backstory="You are a travel expert specializing in Japanese culture, adept at "
                  "finding reliable sources for attractions and trends.",
        tools=[search_tool, scrape_tool],
        reasoning=True,
        verbose=True,
        memory=True,
        allow_delegation=True
    )

    activity_planner = Agent(
        role="Activity Planner",
        goal=f"Curate a list of cultural activities in {destination} tailored for a {trip_days}-day trip",
        backstory="You are a creative planner who designs engaging travel experiences, "
                  "focusing on cultural immersion for travelers.",
        verbose=True,
        memory=True
    )

    budget_analyst = Agent(
        role="Budget Analyst",
        goal=f"Create a budget breakdown for a {trip_days}-day trip to {destination} within ${budget_usd}",
        backstory="You are a financial expert skilled in travel budgeting, ensuring "
                  "cost-effective plans without compromising experience.",
        tools=[currency_tool],
        verbose=True,
        memory=True
    )

    itinerary_writer = Agent(
        role="Itinerary Writer",
        goal=f"Compile a detailed {trip_days}-day travel itinerary for {destination}",
        backstory="You are a meticulous writer who crafts clear, engaging travel "
                  "itineraries that balance activities and logistics.",
        verbose=True,
        memory=True
    )

    return researcher, activity_planner, budget_analyst, itinerary_writer