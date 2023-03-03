from pathlib import Path

from cli_chat.bot import Bot
from cli_chat.console import Console
from cli_chat.command import CommandManager


def read_key(key_path: str, console: Console):
    key_path = Path(key_path)
    if not key_path.exists():
        key = console.info(
            "Cannot find key, maybe this is the first time you use, please key in a valid OpenAI Key:"
        )
        with key_path.open("w") as f:
            f.write(key)

    with key_path.open() as f:
        return f.read().strip()


def main():
    console = Console(history_file=".history")
    api_key = read_key(".key", console)
    Bot(openai_api_key=api_key,
        console=console,
        command_manager=CommandManager(),
        )()
