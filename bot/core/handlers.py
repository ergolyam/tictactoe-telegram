import pyrogram.filters
import pyrogram.handlers.message_handler
from bot.funcs.base import (
    answer_inline,
    answer_message,
    board_size_selection,
    game_mode_selection,
    player_o_join,
    player_move
)

def init_handlers(app):
    app.add_handler(
        pyrogram.handlers.InlineQueryHandler(
            answer_inline,
        )
    )
    app.add_handler(
        pyrogram.handlers.message_handler.MessageHandler(
            answer_message,
            pyrogram.filters.command("ttt") &
                pyrogram.filters.group
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            board_size_selection,
            pyrogram.filters.regex(r"^board_size_(\d+)_([a-zA-Z0-9]+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            game_mode_selection,
            pyrogram.filters.regex(r"^game_mode_(\d+)_([a-zA-Z0-9]+)$")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            player_o_join,
            pyrogram.filters.regex(r"join_o_([a-zA-Z0-9]+)")
        )
    )
    app.add_handler(
        pyrogram.handlers.callback_query_handler.CallbackQueryHandler(
            player_move,
            pyrogram.filters.regex(r"^([a-zA-Z0-9]+)_(\d+)$")
        )
    )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
