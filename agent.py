from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS

from transcription_reader import get_creator_transcriptions, list_available_creators
from dotenv import load_dotenv
load_dotenv()


# Shared configuration
model = OpenAIChat(id="gpt-4.1-mini")
db = SqliteDb(db_file="tmp/storage.db")

# Tools separadas por tipo de agente
search_tools = [TavilyTools()]
copywriter_tools = [
    TavilyTools(),
    list_available_creators,
    get_creator_transcriptions
]

# Agent for trend research
trend_scout = Agent(
    model=model,
    name="trend_scout",
    add_history_to_context=True,
    num_history_runs=5,
    db=db,
    tools=search_tools,
    instructions=open("prompts/trend_scout.md").read()
)

# Agent for Instagram/TikTok Reels
reels_copywriter = Agent(
    model=model,
    name="reels_copywriter",

    add_history_to_context=True,
    num_history_runs=10,
    db=db,

    tools=copywriter_tools,

    instructions=open("prompts/reels.md").read()
)

# Agent for LinkedIn posts
linkedin_copywriter = Agent(
    model=model,
    name="linkedin_copywriter",

    add_history_to_context=True,
    num_history_runs=10,
    db=db,

    tools=copywriter_tools,

    instructions=open("prompts/linkedin.md").read()
)

agent_os = AgentOS(
    description="Suite de criação de conteúdo: pesquisa de tendências + copywriting para Reels e LinkedIn",
    agents=[trend_scout, reels_copywriter, linkedin_copywriter],
)
app = agent_os.get_app()

if __name__ == "__main__":
    import os
    is_docker = os.environ.get("DOCKER", "false").lower() == "true"
    agent_os.serve(
        app="agent:app",
        host="0.0.0.0" if is_docker else "127.0.0.1",
        reload=not is_docker
    )
