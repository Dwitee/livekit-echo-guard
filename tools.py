# tools.py
from typing import List, Dict, Optional
from livekit.agents import function_tool, RunContext

# Simple in-memory meeting state (per process)
DECISIONS: List[str] = []
RISKS: List[str] = []
ACTION_ITEMS: List[Dict[str, Optional[str]]] = []


@function_tool()
async def add_decision(context: RunContext, text: str) -> str:
    """
    Add a concise decision that was made in the meeting.
    Example: "We will ship the MVP on September 30th without social login."
    """
    DECISIONS.append(text.strip())
    return f"I've logged this as a decision: {text}"


@function_tool()
async def add_action_item(
    context: RunContext,
    owner: str,
    task: str,
    due: Optional[str] = None,
) -> str:
    """
    Add an action item with an owner and optional due date.
    Example:
      owner="Alice", task="Implement Stripe webhooks", due="next Friday"
    """
    ACTION_ITEMS.append(
        {"owner": owner.strip(), "task": task.strip(), "due": due.strip() if due else None}
    )
    if due:
        return f"Action item noted for {owner}: {task} (due {due})."
    return f"Action item noted for {owner}: {task}."


@function_tool()
async def add_risk(context: RunContext, text: str) -> str:
    """
    Add a risk or blocker.
    Example: "Backend integration might slip because API is unstable."
    """
    RISKS.append(text.strip())
    return f"I've logged this as a risk: {text}"


@function_tool()
async def get_summary(context: RunContext) -> str:
    """
    Return a concise, human-readable summary of decisions, action items,
    and risks captured so far. Use this when the user asks for a recap.
    """
    lines: List[str] = []

    if DECISIONS:
        lines.append("Decisions:")
        for i, d in enumerate(DECISIONS, start=1):
            lines.append(f"{i}. {d}")
    else:
        lines.append("No explicit decisions logged yet.")

    if ACTION_ITEMS:
        lines.append("")
        lines.append("Action items:")
        for i, a in enumerate(ACTION_ITEMS, start=1):
            due_part = f" (due {a['due']})" if a.get("due") else ""
            lines.append(f"{i}. {a['owner']}: {a['task']}{due_part}")
    else:
        lines.append("")
        lines.append("No action items logged yet.")

    if RISKS:
        lines.append("")
        lines.append("Risks and blockers:")
        for i, r in enumerate(RISKS, start=1):
            lines.append(f"{i}. {r}")
    else:
        lines.append("")
        lines.append("No risks or blockers logged yet.")

    return "\n".join(lines)