"""
This file provides a template for future commands.
This file will not be loaded as a cog or module
"""
import os

import interactions

from interactions import (
    Modal,
    ParagraphText,
    ShortText,
    SlashContext,
    slash_command,
    modal_callback,
    ModalContext,
    component_callback,
    ComponentContext,
    Button,
    ButtonStyle,
)
from config import DEV_GUILD

"Highly recommended - we suggest providing proper debug logging"
from src import logutil
from src.game_logic import Game, Question, Verdict

"Change this if you'd like - this labels log messages for debug mode"
logger = logutil.init_logger(os.path.basename(__file__))

RESPONSE_MODAL = Modal(
    ShortText(
        label="Please Type your Answer.",
        custom_id="user_answer",
        required=True,
        placeholder="Type Answer Here",
    ),
    custom_id="modal_event_user_answer",
    title="Blissful Blazars",
)

NEXT_ROUND_BUTTON = Button(
    custom_id="button_event_round_start",
    style=ButtonStyle.BLURPLE,
    label="Start Round",
)


class QuizCog(interactions.Extension):

    user_games: dict = {}

    # TEMP FUNCTIONS - WILL BE OVERHAULED.
    def insert_user_game(self, user_id: str | int, game: Game) -> bool:

        if not self.user_games.get(f"{user_id}"):
            self.user_games[f"{user_id}"] = {"game": game}
            return True
        return False

    def get_user_game(self, user_id: str | int) -> Game:
        return (
            self.user_games.get(f"{user_id}")["game"]
            if self.user_games.get(f"{user_id}") is not None
            else None
        )

    def user_exists(self, id: str) -> bool:
        return not (not self.get_user_game(id))

    @interactions.slash_command(
        "start", description="begins ", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    async def _start_quiz(self, ctx: interactions.SlashContext):
        """Register as an extension command"""
        if self.user_exists(ctx.user.id):
            await ctx.send(
                interactions.Embed(
                    title="Sorry! You're already in an active game!", color=0xE63D3D
                ),
                ephemeral=True,
            )
        else:
            _game = Game()
            self.insert_user_game(ctx.user.id, _game)
            round_return = _game.start_new_round()
            _embed = interactions.Embed(
                title=f"**{round_return[0]}**", description=f"*{round_return[1]}*"
            )
            await ctx.send(embed=_embed, components=NEXT_ROUND_BUTTON)

    @modal_callback("modal_event_user_answer")
    async def on_modal_answer(self, ctx: ModalContext, **kwargs):
        if self.user_exists(ctx.user.id) and kwargs.get("user_answer") is not None:
            users_game = self.get_user_game(ctx.user.id)
            if users_game.check_answer(str(kwargs.get("user_answer")))[0] == True:
                await ctx.respond(
                    embed=interactions.Embed(
                        title="Sorry! You're not in an active game!", color=0xE63D3D
                    ),
                    ephemeral=True,
                )

        else:
            await ctx.respond(
                interactions.Embed(
                    title="Something Went Wrong. You either do not have an active game, "
                    "or your input was incorrectly recieved.",
                    color=0xE63D3D,
                ),
                ephemeral=True,
            )

    @component_callback("button_event_round_start")
    async def my_callback(self, ctx: ComponentContext):
        if not self.user_exists(ctx.user.id):
            await ctx.send(
                interactions.Embed(
                    title="Sorry! You're not in an active game!", color=0xE63D3D
                ),
                ephemeral=True,
            )
        else:
            await ctx.send_modal(RESPONSE_MODAL)
