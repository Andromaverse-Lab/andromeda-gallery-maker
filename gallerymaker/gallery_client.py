import discord
from .gallery import create_gallery
import logging
from discord import app_commands
from .collections import AndromedaCollections

LOG = logging.getLogger(__name__)

GUILDS = [
    discord.Object(id=977279710713245766)
]

class GalleryClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

        create_gallery_cmd = discord.app_commands.Command(
            name="create-gallery",
            description="Creates a gallery of 4 Andromeda Labs tokens",
            callback=self.create_gallery
        )
        self.tree.add_command(create_gallery_cmd)

        # These are needed so we don't delete the commands from the
        # stargaze-floor-bot. The commands not in the right server
        # will yield warnings, but they shouldn't break anything.
        u1 = discord.app_commands.Command(
            name="listcollections",
            description="List tracked Stargaze collections with their floor price",
            callback=self.not_me,
        )
        self.tree.add_command(u1)

        u2 = discord.app_commands.Command(
            name="querytraitfloor",
            description="Query the floor pricing for a specific trait",
            callback=self.not_me,
        )
        self.tree.add_command(u2)

    async def setup_hook(self):
        for guild in GUILDS:
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        LOG.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def not_me(self, interaction):
        pass

    @discord.app_commands.describe(
        collection_0='C0', token_0="T0",
        collection_1='C1', token_1="T1",
        collection_2='C2', token_2="T2",
        collection_3='C3', token_3="T3",
    )
    async def create_gallery(self,
        interaction: discord.Interaction, 
        collection_0: AndromedaCollections, token_0: int, 
        collection_1: AndromedaCollections, token_1: int, 
        collection_2: AndromedaCollections, token_2: int, 
        collection_3: AndromedaCollections, token_3: int
    ):
        """Creates a gallery of 4 Andromeda Labs tokens."""
        tokens = [
            {"name": collection_0, "id": token_0},
            {"name": collection_1, "id": token_1},
            {"name": collection_2, "id": token_2},
            {"name": collection_3, "id": token_3},
        ]

        LOG.info("Received request")
        gallery = create_gallery(tokens)
        filename = "gallery.png"
        gallery.save(filename=filename)

        file = discord.File(filename)
        await interaction.response.send_message(file=file)
