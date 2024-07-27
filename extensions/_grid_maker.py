
import os
import typing
from typing import Union, TypedDict

import interactions

from config import DEV_GUILD
from src.emoji_grid import EmojiGrid, UnsupportedEmoji, InvalidCoordinates







class GridMaker(interactions.Extension):



    PERMITTED_EMOJIS = [interactions.SlashCommandChoice(name="🟥", value="🟥"),
                        interactions.SlashCommandChoice(name="🟧", value="🟧"),
                        interactions.SlashCommandChoice(name="🟨", value="🟨"),
                        interactions.SlashCommandChoice(name="🟩", value="🟩"),
                        interactions.SlashCommandChoice(name="🟦", value="🟦"),
                        interactions.SlashCommandChoice(name="🟪", value="🟪"),
                        interactions.SlashCommandChoice(name="🟫", value="🟫"),
                        interactions.SlashCommandChoice(name="⬛", value="⬛"),
                        interactions.SlashCommandChoice(name="⬜", value="⬜")]

    user_grids: dict = {}

    def insert_user_grid(self, user_id: str | int, grid: EmojiGrid) -> bool:
        if not self.user_grids.get(f"{user_id}"):
            self.user_grids[f"{user_id}"] = {"grid": grid}
            return True
        return False

    def get_user_grid(self, user_id: str | int) -> EmojiGrid:
        return self.user_grids.get(f"{user_id}")['grid'] if self.user_grids.get(f"{user_id}") is not None else None

    def user_exists(self, id: str) -> bool:
        return not (not self.get_user_grid(id))


    @interactions.slash_command(
        "grid", description="test command", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    @interactions.slash_option(
        "row",
        "Amount of Rows",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
        max_value=30,
        min_value= 3,
    )
    @interactions.slash_option(
        "col",
        "Amount of Columns",
        opt_type=interactions.OptionType.INTEGER,
        required=False,
        max_value=30,
        min_value=3,
    )
    @interactions.slash_option(
        "fill",
        "Color to use by default.",
        opt_type=interactions.OptionType.STRING,
        required=False,
        choices= PERMITTED_EMOJIS,
    )
    async def _generate_grid(self, ctx: interactions.SlashContext, rows: int = 10, cols: int = 10 ,
                             fill: str = EmojiGrid.BLACK):
        """Register as an extension command"""
        grid_entry: EmojiGrid = EmojiGrid(rows, cols, fill)
        if [grid_entry.rows, grid_entry.cols] == [rows, cols]:
            if not self.user_exists(ctx.user.id):
                self.insert_user_grid(ctx.user.id, grid_entry)
            else:
                await ctx.respond("You already have a grid!")

        await ctx.send(str(self.get_user_grid(ctx.user.id)))

    @interactions.slash_command(
        "update", description="Updates color at a position.", scopes=[DEV_GUILD] if DEV_GUILD else None
    )
    @interactions.slash_option(
        "row",
        "target row",
        opt_type=interactions.OptionType.INTEGER,
        required=True,
        min_value=1,
    )
    @interactions.slash_option(
        "col",
        "target col",
        opt_type=interactions.OptionType.INTEGER,
        required=True,
        min_value=1,
    )
    @interactions.slash_option(
        "color",
        "Color to fill position with",
        opt_type=interactions.OptionType.STRING,
        required=True,
        choices= PERMITTED_EMOJIS,
    )
    async def _update(self, ctx: interactions.SlashContext, row: int, col: int, color: str):
        if self.user_exists(ctx.user.id):
            user_grid = self.get_user_grid(ctx.user.id)
            user_grid.update(row, col, color)
            if user_grid.get(row, col) != color:
                await ctx.respond("Could not Update position..", ephemeral=True)
            else:
                await ctx.respond(str(user_grid), ephemeral=False)
        else:
            await ctx.respond("You need to create a grid first! Do /grid to create one.", ephemeral=True)

