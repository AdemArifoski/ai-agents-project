"""Block 2, first half: call the memory tools over MCP. TODO 6.

    python mcp_server.py &          # in one terminal
    PORT=8001 python mcp_server.py & # and a second instance
    python 01_mcp_client.py

Three things happen here and the third is the one to watch.
"""

from __future__ import annotations

import asyncio

from mcp.client import Client

SUBJECT = "A. Muller"


def text_of(result) -> str:
    content = getattr(result, "content", result)
    if isinstance(content, list) and content:
        return getattr(content[0], "text", str(content[0]))
    return str(content)


async def call(port: int, tool: str, **args):
    async with Client(f"http://127.0.0.1:{port}/mcp") as client:
        return await client.call_tool(tool, args)


async def main() -> int:
    """TODO 6. Three steps, and the third has a warning attached.

    1. Connect to :8000 and print the tool catalog. Seeing it arrive over
       HTTP is what makes the boundary real: these tools are not in this
       process.

    2. Call open_case and then remember on :8000. Watch
       artifacts/memory_store.json change while it runs.

    3. Redeem the SAME handle on :8001, the second instance, and recall from
       it.

    The warning: step 3 on its own does not prove the protocol is stateless.
    It would work under the old session-based protocol too, because each
    call opens its own connection and the state is on disk. It shows that a
    file is a file. 02_stateless.py is the demonstration that actually
    distinguishes the two, and it is the next thing you run.
    """
     # Connect to :8000 and list the tool catalog
    async with Client("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()

        print("Available tools:", [tool.name for tool in tools.tools])

        # Open a case and remember a fact
        opened = await client.call_tool(
            "open_case", {"subject": SUBJECT}
        )
        handle = text_of(opened)

        remembered = await client.call_tool(
            "remember",
            {
                "subject": SUBJECT,
                "kind": "identity",
                "fact": "A. Muller is the subject of this case."
            }
        )

        print("Handle:", handle)
        print("Remembered:", text_of(remembered))

    # Connect to :8001 and resolve the SAME handle
    async with Client("http://127.0.0.1:8001/mcp") as client:
        redeemed = await client.call_tool(
            "case_subject", {"handle": handle}
        )

        print("Redeemed subject:", text_of(redeemed))

        recalled = await client.call_tool(
            "recall",
            {
                "subject": SUBJECT,
                "query": "subject case"
            }
        )

        print("Recalled:", text_of(recalled))

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
