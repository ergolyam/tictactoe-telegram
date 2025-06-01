import random, uuid
from bot.funcs.invite import ttt_start, join_ttt_o, update_buttons
from bot.funcs.game import move_ttt
from bot.core.common import Common
from bot.core.trans import get_translation
from bot.config import logging_config
logging = logging_config.setup_logging(__name__)

sessions = Common.sessions
selected_squares = Common.selected_squares
session_cleanup_tasks = Common.session_cleanup_tasks


def gen_session(message, chat_id):
    session_id = uuid.uuid4().hex[:12]
    sessions[session_id] = {
        "x": {"id": None, "name": None},
        "o": {"id": None, "name": None},
        "next_move": random.choice(["X", "O"]),
        "x_points": 0,
        "o_points": 0,
        "combos": [],
        "message_id": None,
        "chat_id": chat_id,
        "board_size": 3,
        "game_mode": 0,
        "random_mode": None,
        "lang": message.from_user.language_code
    }
    selected_squares[session_id] = None
    return sessions, session_id


async def answer_inline(_, inline_query):
    sessions, session_id = gen_session(inline_query, None)
    (
        sessions[session_id]["x"]["id"],
        sessions[session_id]["x"]["name"],
        results
    ) = await ttt_start(
        session_id,
        sessions,
        inline_query,
        get_translation
    )

    await inline_query.answer(results, cache_time=1)


async def answer_message(_, message):
    sessions, session_id = gen_session(message, message.chat.id)
    (
        sessions[session_id]["x"]["id"],
        sessions[session_id]["x"]["name"],
        message_id
    ) = await ttt_start(
        session_id,
        sessions,
        message,
        get_translation
    )
    sessions[session_id]["message_id"] = message_id


async def board_size_selection(client, callback_query):
    size = int(callback_query.data.split('_')[2])
    session_id = str(callback_query.data.split('_')[3])
    if sessions.get(session_id) == None:
        await callback_query.answer(
            get_translation(
                callback_query.from_user.language_code,
                'complete'
            )
        )
        return
    
    if sessions[session_id]["x"]["id"] != callback_query.from_user.id:
        await callback_query.answer(
            get_translation(
                sessions[session_id]["lang"],
                "unavailable"
            )
        )
        return

    if sessions[session_id].get("board_size") == size:
        await callback_query.answer(
            f"{get_translation(sessions[session_id]["lang"], "already_selected")}"
            f" {get_translation(sessions[session_id]["lang"], "board_size").lower()}"
            f" {size}x{size}."
        )
        return

    if size == 3:
        sessions[session_id]["game_mode"] = 0
        logging.debug(
            f"Session {session_id}: selected board size {size}"
            f", mod is selected {sessions[session_id]["game_mode"]}"
        )
    
    sessions[session_id]["board_size"] = size
    await update_buttons(
        client,
        session_id,
        sessions[session_id],
        callback_query,
        size,
        sessions[session_id]["game_mode"],
        get_translation,
    )
    await callback_query.answer(
        f"{get_translation(sessions[session_id]["lang"], "select")}"
        f" {get_translation(sessions[session_id]["lang"], "board_size").lower()}:"
        f" {size}x{size}."
    )


async def game_mode_selection(client, callback_query):
    mode = int(callback_query.data.split('_')[2])
    session_id = str(callback_query.data.split('_')[3])
    if sessions.get(session_id) == None:
        await callback_query.answer(
            get_translation(
                callback_query.from_user.language_code,
                'complete'
            )
        )
        return

    if sessions[session_id]["x"]["id"] != callback_query.from_user.id:
        await callback_query.answer(
            get_translation(
                sessions[session_id]["lang"],
                "unavailable"
            )
        )
        return

    if sessions[session_id].get("game_mode") == mode:
        await callback_query.answer(
            f"{get_translation(sessions[session_id]["lang"], "already_selected")}"
            f" {get_translation(sessions[session_id]["lang"], "game_mode").lower()}"
        )
        return

    sessions[session_id]["game_mode"] = mode
    await update_buttons(
        client,
        session_id,
        sessions[session_id],
        callback_query,
        sessions[session_id]["board_size"],
        mode,
        get_translation,
    )
    await callback_query.answer(
        f"{get_translation(sessions[session_id]["lang"], "select")}"
        f" {get_translation(sessions[session_id]["lang"], "game_mode").lower()}:"
        f" {get_translation(sessions[session_id]["lang"], f"mode_{mode}").lower()}"
    )

def save_points(session_id, x_points=None, o_points=None, combos=None):
    if x_points != None:
        sessions[session_id]["x_points"] = x_points
    if o_points != None:
        sessions[session_id]["o_points"] = o_points
    if combos != None:
        sessions[session_id]["combos"].extend(combos)


async def player_o_join(client, callback_query):
    session_id = callback_query.data.split('_')[-1]
    await join_ttt_o(
        session_id,
        sessions,
        client,
        callback_query,
        get_translation,
        session_cleanup_tasks,
        random,
    )


async def player_move(client, callback_query):
    session_id, position = callback_query.data.split('_')
    session_id = str(session_id)
    session = sessions.get(session_id)
    if session != None:
        await move_ttt(
            client,
            callback_query,
            sessions[session_id],
            int(position),
            session_id,
            get_translation,
            save_points,
        )
    else:
        await callback_query.answer(
            get_translation(
                callback_query.from_user.language_code,
                'complete'
            )
        )


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")

