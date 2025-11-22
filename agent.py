# agent.py
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google, noise_cancellation

from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import add_decision, add_action_item, add_risk, get_summary

# Load LIVEKIT_* and GOOGLE_API_KEY from .env
load_dotenv()


class MeetingAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            # Google Gemini Live realtime voice model
            llm=google.realtime.RealtimeModel(
                model="gemini-2.0-flash-exp",  # default is fine; explicit for clarity
                voice="Puck",
                temperature=0.7,
            ),
            tools=[add_decision, add_action_item, add_risk, get_summary],
        )


async def entrypoint(ctx: agents.JobContext):
    # connect this worker to the room (required when running as a worker)
    await ctx.connect()

    # Session orchestrates audio in/out & the agent
    session = AgentSession()

    await session.start(
        room=ctx.room,
        agent=MeetingAssistant(),
        room_input_options=RoomInputOptions(
            # basic background noise cancellation
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Initial greeting & explanation of capabilities
    await session.generate_reply(instructions=SESSION_INSTRUCTION)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))