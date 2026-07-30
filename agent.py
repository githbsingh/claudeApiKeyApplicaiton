import os
import sys
from pathlib import Path
import datetime
from dotenv import load_dotenv
from google.adk.agents import Agent, LoopAgent
from google.adk.tools import agent_tool

# Load environment variables from the workspace .env file, overriding any stale values already in memory.
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH, override=True)


def _get_google_api_key():
    placeholder_values = {"", "YOUR_GOOGLE_API_KEY_HERE", "YOUR_GEMINI_API_KEY_HERE", "changeme"}
    candidates = [os.getenv("GOOGLE_API_KEY"), os.getenv("GEMINI_API_KEY")]

    for value in candidates:
        if value and value not in placeholder_values:
            os.environ["GOOGLE_API_KEY"] = value
            os.environ["GEMINI_API_KEY"] = value
            return value

    return None


API_KEY = _get_google_api_key()
MODEL = os.getenv("MODEL", "gemini-3.5-flash")

if not API_KEY:
    print("Warning: No Google API key found. Add GOOGLE_API_KEY or GEMINI_API_KEY to .env before sending a prompt.")
else:
    print("Google API key loaded from .env for agent startup.")

# Sub-Agent : Blog Planner
blog_planner = Agent(
    name="BlogPlanner",
    model=MODEL,
    description="A sub-agent that generates a blog post outline based on a given topic.",
    instruction="""
You are a technical content strategist. Produce a clear Markdown outiline with:
- Title
- Short Intro
- 4-6 main sections (each with 2-3 bullets)
- Conclusion

if `codebase_context` exists in state, weave in specific secstion/snippets.
Return only the outline in Markdown. 
""",
    output_key="blog_outline",
)

class OutlineValidationChecker(Agent):
    def __init__(self, name="OutlineValidationChecker", model=MODEL):
        super().__init__(
            name=name,
            model=model,
            description="Validates that the outline is usable.",
            instruction="""
Check the outline in state `blog_outline`. If it has a title, intro, 4-6 main sections, and a conclusion,
respond exactly "ok".
Otherwise respond exactly "retry" and list missing pieces.
""",
            output_key="validation_result",
        )

robust_blog_planner = LoopAgent(
    name="RobustBlogPlanner",
    description="Retries Planning if Validation fails.",
    sub_agents=[blog_planner, OutlineValidationChecker()],
    max_iterations=3,
)

# ── Sub-Agent: Writer ────────────────────────────────────────────────────────
blog_writer = Agent(
   name="BlogWriter",
   model=MODEL,
   description="Writes a technical blog post from the outline.",
   instruction="""
Write a complete Markdown article from the outline in `blog_outline`.

Guidelines:
- Audience: software engineers; skip basics and focus on practical insight.
- Explain both the 'how' and 'why'.
- Include concise code snippets when helpful.
- Follow the outline’s structure (H2/H3).
- Output only the final article in Markdown (no fence around the whole post).
""",
   output_key="blog_post",
)

class BlogPostValidationChecker(Agent):
   def __init__(self):
       super().__init__(
           name="BlogPostValidationChecker",
           model=MODEL,
           description="Validates the final post.",
           instruction="""
Check `blog_post` for: intro, clear sections matching the outline, conclusion, and technical clarity.
If passes, respond "ok". Else respond "retry" with the specific fixes.
""",
           output_key="validation_result",
       )

robust_blog_writer = LoopAgent(
   name="RobustBlogWriter",
   description="Retries writing if validation fails.",
   sub_agents=[blog_writer, BlogPostValidationChecker()],
   max_iterations=3,
)

# Expose planner/writer as tools so the root agent can call them explicitly
planner_tool = agent_tool.AgentTool(agent=robust_blog_planner)
writer_tool  = agent_tool.AgentTool(agent=robust_blog_writer)


# ── Root Agent: Plan → Write ────────────────────────────────────────────────
root_agent = Agent(
   name="Blogger",
   model=MODEL,
   description="Minimal multi-agent blogger that plans and writes.",
   instruction=f"""
If the user gives a topic:
1) Call the planner tool to generate the outline.
2) Call the writer tool to produce the full draft.
3) End with 3 alternate titles and 2 tweet-length hooks.

Date: {datetime.datetime.now().strftime("%Y-%m-%d")}
""",
   tools=[
       planner_tool, # calls RobustBlogPlanner
       writer_tool,  # calls RobustBlogWriter
   ],
)


