import shutil
from pathlib import Path

from cli_chat.bot import Bot
from cli_chat.console import Console
from cli_chat.command import CommandManager

from appdirs import user_config_dir
from typer import Typer


def read_key(key_path: Path, console: Console):
    if not key_path.exists():
        console.info("No OpenAI key found. Please go to https://beta.openai.com/account/api-keys to get one.")
        update_key()

    with key_path.open() as f:
        return f.read().strip()


app = Typer(add_completion=False)
config_app = Typer(add_completion=False, no_args_is_help=True)
config_dir = Path(user_config_dir("cli_chat"))
console = Console(history_dir=config_dir / "history")


@app.callback(invoke_without_command=True)
def main():
    api_key = read_key(config_dir / "key", console)
    Bot(openai_api_key=api_key,
        console=console,
        command_manager=CommandManager(),
        )()


@config_app.command(help="Update the OpenAI key.")
def update_key():
    api_key = console.prompt(
        "Please key in a valid OpenAI Key: ",
        is_password=True,
    )
    with (config_dir / "key").open("w") as f:
        f.write(api_key)
    console.info("Key updated.")


@config_app.command(help="Remove the OpenAI key.")
def remove_key():
    if (config_dir / "key").exists():
        (config_dir / "key").unlink()
        console.info("Key removed.")
    else:
        console.error("No key found.")


@config_app.command(help="Clear the input history.")
def clear_history():
    shutil.rmtree(config_dir / "history")
    console.info("History cleared.")
