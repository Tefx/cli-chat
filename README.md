# cli-chat

cli-chat is a command-line tool that allows you to have a conversation with ChatGPT from your terminal.

## Installation

```bash
# pip install cli-chat
```

Or, if you don't want to install:

1. Clone the repository.
2. Run `poetry install` to install the dependencies.

## Usage

To start a conversation, run the following command in your terminal:
```bash
# cli-chat
```
or
```bash
# poetry run cli-chat
```


### Notes:

1. You will need a valid API key from [here](https://platform.openai.com/account/api-keys) to use the tool.
2. The key will be stored in a file named `.key` in current directory. If you want to change the key or 
3. stop using the script, simply remove this file.
4. You can use the arrow keys to navigate through the history of your conversation.
5. To end the conversation, simply type "thanks", "thx", or something similar.
6. If you don't want to render the answer as markdown in the terminal, put `[nm]` in front of your question. 
For example, if you want to ask "How are you?" without rendering the answer as markdown, you would type `[nm]How are you?` instead.
7. Auth suggestions and common key-bindings should also work, thanks to [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit).

## Example

![Example](docs/example-1.png)

![Example](./docs/example-2.png)