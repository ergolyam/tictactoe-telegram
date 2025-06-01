# tictactoe-telegram

Play Tic‑Tac‑Toe (and a couple of fun variants) right inside Telegram chats. The bot works entirely through inline queries and group commands, so no extra websites or apps are needed.

### Initial Setup

1. **Clone the repository**: Clone this repository using `git clone`.
2. **Create Virtual Env**: Create a Python Virtual Environment `venv` to download the required dependencies and libraries.
3. **Download Dependencies**: Download the required dependencies into the Virtual Environment `venv` using `uv`.

```shell
git clone https://github.com/grisha765/tictactoe-telegram.git
cd tictactoe-telegram
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv sync
```

## Usage

### Deploy

- Run the bot:
  ```bash
  .venv/bin/python bot
  ```

### Container

- Pull the container:
    ```bash
    podman pull ghcr.io/grisha765/tictactoe-telegram:latest
    ```

- Deploy using Podman:
    ```bash
    podman run \
    --name tictactoe-telegram \
    -e TG_TOKEN="your_telegram_bot_token" \
    ghcr.io/grisha765/tictactoe-telegram:latest
    ```

## Environment Variables

The following environment variables control the startup of the project:

| Variable       | Values                              | Description                                                             |
| -------------- | ----------------------------------- | ----------------------------------------------------------------------- |
| `LOG_LEVEL`    | `DEBUG`, `INFO`, `WARNING`, `ERROR` | Logging verbosity                                                       |
| `TG_ID`        | *integer*                           | Telegram API ID from [https://my.telegram.org](https://my.telegram.org) |
| `TG_HASH`      | *string*                            | Telegram API hash                                                       |
| `TG_TOKEN`     | *string*                            | Bot token issued by @BotFather                                          |

## Features

- Classic 3 × 3 as well as 5 × 5 and 7 × 7 boards
- Three game modes
- Standard – 3/4/5‑in‑a‑row wins
- Points – fill the entire board, victory by score
- Random – every turn the rules may change
- Inline play – type @YourBotUsername in any chat to start a board
- Group command /ttt – instantly launches a session in group chats
- Clean UI rendered with Telegram emoji and inline keyboards
- Multilingual – English and Russian out of the box (easily extendable)
- Stateless hosting – no database required; state is kept in‑memory with optional periodic cleanup
- Docker‑ready – zero‑dependency image shipped on each push to main

# Adding new languages

- Copy bot/config/lang/en.json and translate the values.
- Name the file with the locale code (e.g. es.json).
- Done – the get_translation helper picks it up at runtime.
