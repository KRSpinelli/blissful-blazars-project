"""

Authored by Dial (@dial),
Python Offical CodeJam '24
FINAL BUILD PUSHED 07/27/2024 10:50 PM EST
** THIS CODE IS UNMAINTAINED -- AND WILL BE PERMANENTLY BROKEN UPON ANY CODE-BREAKING CHANGES TO ITS LIBARIES. **
"""
import os
import random
import re
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
from src.game import Game

"Change this if you'd like - this labels log messages for debug mode"
logger = logutil.init_logger(os.path.basename(__file__))

VERDICT_EVENT_REGEX_AS_STR = "button_verdict_"
VERDICT_EVENT_REGEX = re.compile(fr"{VERDICT_EVENT_REGEX_AS_STR}")
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
    emoji=interactions.PartialEmoji.from_str("<:GameAdvance:1266888210886295603>")
)

RETRY_BUTTON = Button(
    custom_id="button_event_retry_round",
    style=ButtonStyle.BLUE,
    label="RETRY",
    emoji=interactions.PartialEmoji.from_str("<:GameRetry:1266887992287428608>")
)

END_GAME = Button(
    custom_id="button_event_end_game",
    style=ButtonStyle.SECONDARY,
    label="",
    emoji=interactions.PartialEmoji.from_str("<:GameAbort:1266887755242143898>")
)

VERDICT_BUTTONS = [
    Button(
        custom_id="button_verdict_false",
        style=ButtonStyle.DANGER,
        label="FALSE",
    ),
    Button(
        custom_id="button_verdict_mostly_false",
        style=ButtonStyle.DANGER,
        label="MOSTLY FALSE",
    ),

    END_GAME,

    Button(
        custom_id="button_verdict_mostly_true",
        style=ButtonStyle.GREEN,
        label="MOSTLY TRUE",
    ),
    Button(
        custom_id="button_verdict_true",
        style=ButtonStyle.GREEN,
        label="TRUE",
    )
]

VERDICT_BUTTONS_DISABLED = [
    Button(
        custom_id="button_verdict_false",
        style=ButtonStyle.GRAY,
        label="FALSE",
        disabled=True
    ),
    Button(
        custom_id="button_verdict_mostly_false",
        style=ButtonStyle.GRAY,
        label="MOSTLY FALSE",
        disabled=True
    ),

    Button(
        custom_id="button_event_end_game",
        style=ButtonStyle.SUCCESS,
        label="",
        emoji=interactions.PartialEmoji.from_str("<:GameAbort:1266887755242143898>")
    ),

    Button(
        custom_id="button_verdict_mostly_true",
        style=ButtonStyle.GRAY,
        label="MOSTLY TRUE",
        disabled=True
    ),
    Button(
        custom_id="button_verdict_true",
        style=ButtonStyle.GRAY,
        label="TRUE",
        disabled=True
    )
]

STATUS_INDICATION_BUTTONS = {

    "CORRECT": Button(
        custom_id="indicator_correct",
        style=ButtonStyle.SUCCESS,
        label="Correct",
        disabled=True
    ),
    "INCORRECT": Button(
        custom_id="indicator_correct",
        style=ButtonStyle.DANGER,
        label="Incorrect",
        disabled=True
    )

}


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
            await ctx.send(embed=interactions.Embed(
                title="Sorry! You're already in an active game!", color=0xE63D3D
            ),
                ephemeral=True,
            )
        else:
            game = Game(ctx.user.id)
            self.insert_user_game(ctx.user.id, game)
            game.start_new_round()
            _embed = interactions.Embed(
                title=f"**Credibility Connoisseur, how factual is this truly?**",
                description=f"Evaluate: *{game.get_question().get_question()}*",
                color=random.choice(["#f9d49d", "#e67f74", "#e593b9", "#eca3aa", "#9e53b0", "#efbf96", "#75667c"])
            )
            await ctx.send(embed=_embed, components=VERDICT_BUTTONS)

    async def present_prompt(self, ctx: interactions.ComponentContext):

        if self.user_exists(ctx.user.id):
            game = self.get_user_game(ctx.user.id)
            embed = interactions.Embed(
                title=f"**Credibility Connoisseur, how factual is this truly?**",
                description=f"Evaluate: *{game.get_question().get_question()}*",
                color=random.choice(["#f9d49d", "#e67f74", "#e593b9", "#eca3aa", "#9e53b0", "#efbf96", "#75667c"])
            )

            await ctx.send(embed=embed, components=VERDICT_BUTTONS)
        else:
            await ctx.respond(embed=interactions.Embed(
                title="Something Went Wrong. You either do not have an active game, "
                      "or your input was incorrectly recieved.",
                color=0xE63D3D,
            ),
                ephemeral=True,
            )

    @component_callback("button_event_end_game")
    async def exit(self, ctx: ComponentContext, ended_by: str = "User"):
        if self.user_exists(ctx.user.id):
            self.get_user_game(ctx.user.id)._end_game()
            await ctx.respond(embed=interactions.Embed(
                title=f"Game Ended by {ended_by}.", color=0xE63D3D,
                description=f"Final Score: ``{self.get_user_game(ctx.user.id).get_final_score()}``"
            ),
                ephemeral=True, )
            del self.user_games[str(ctx.user.id)]
        else:
            await ctx.respond(embed=
            interactions.Embed(
                title="Sorry! You're not in an active game!", color=0xE63D3D
            ),
                ephemeral=True,
            )

    @component_callback(VERDICT_EVENT_REGEX)
    async def verdict_callback(self, ctx: ComponentContext):
        match = VERDICT_EVENT_REGEX.match(ctx.custom_id)
        if match:
            if self.user_exists(ctx.user.id):
                users_game = self.get_user_game(ctx.user.id)
                users_game.attempt_answer(str(ctx.custom_id).replace(VERDICT_EVENT_REGEX_AS_STR, "").upper())

                if users_game.get_difference() == 0:

                    descriptor = users_game.get_question().get_description()
                    allow_new_round = users_game.start_new_round()
                    final_score = self.get_user_game(ctx.user.id).get_final_score()
                    final_score_str = f" Final Score: ``{final_score}``"
                    await ctx.edit_origin(components=VERDICT_BUTTONS_DISABLED)
                    await ctx.respond(
                        embed=interactions.Embed(
                            title="Correct!", color=0x91F35D,
                            description=f"*{descriptor[1::]}* \n\n{"Beginning Next Round!" if allow_new_round else f"Game Over!\n{final_score_str}"}"
                        ),
                        ephemeral=True, delete_after=60 if final_score == -1 else None
                    )
                    if final_score == -1:
                        await self.present_prompt(ctx)
                        del final_score, final_score_str
                    else:
                        del final_score, final_score_str
                        await self.exit(ctx, ended_by="Internal Service")
                else:
                    await ctx.respond(
                        embed=interactions.Embed(
                            title="Incorrect! Try again!", color=0xE63D3D,
                        ),
                        ephemeral=True,
                        delete_after=10,
                        components=END_GAME
                    )
            else:
                await ctx.respond(embed=
                interactions.Embed(
                    title="Something Went Wrong. You either do not have an active game, "
                          "or your input was incorrectly recieved.",
                    color=0xE63D3D,
                ),
                    ephemeral=True,
                )
        else:
            pass

    @component_callback("button_event_round_start")
    async def start_callback(self, ctx: ComponentContext):
        await self.my_callback(ctx)

    @component_callback("button_event_retry_round")
    async def my_callback(self, ctx: ComponentContext):
        if not self.user_exists(ctx.user.id):
            await ctx.send(embed=
            interactions.Embed(
                title="Sorry! You're not in an active game!", color=0xE63D3D
            ),
                ephemeral=True,
            )
        else:
            await self.present_prompt(ctx)
