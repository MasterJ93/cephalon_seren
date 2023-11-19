"""
Contains views related to admin-only commands.
"""

import discord

class WarnView(discord.ui.View):
    """
    Contains a view for the "warn" command.
    """
    def __init__(self,
                 interaction: discord.Interaction,
                 guild: discord.Guild,
                 member: discord.Member):
        super().__init__()
        self.interaction=interaction
        self.guild=guild
        self.member=member

        self.confirm=False
        self.values=[]
        self.message = ('Here are the rules you\'ve selected:' +
                        '')

        # rules_dropdown = RulesDropdown()
        # self.add_item(rules_dropdown)
        # self.values=rules_dropdown.values

    # This is to allow `rule_section` to access this variable.
    options = [
            discord.SelectOption(
                label='1. Adhere to Discord ToS'
            ),
            discord.SelectOption(
                label='2. No insults or hate speech'
            ),
            discord.SelectOption(
                label='3. No political/religious talk'
            ),
            discord.SelectOption(
                label='4. No spamming/advertising'
            ),
            discord.SelectOption(
                label='5. No one under 18 in adult-only channels'

            ),
            discord.SelectOption(
                label='6. No spoilers outside of spoiler channels'
            )
    ]

    @discord.ui.select(
            placeholder='What rule(s) did they violate?',
            min_values=1,
            max_values=6,
            options=options)
    async def rule_selection(self,
                             interaction: discord.Interaction,
                             select: discord.ui.Select):
        """The dropdown menu that shows the TL;DR versions of the rules."""
        print(select.values)

        # Sort the items in ascending order.
        sorted_values = sorted(select.values, key=self.sorting_key)
        self.values = sorted_values

        # Loop through the list to grab each rule.
        rules = ''
        for rule in sorted_values:
            rules += f'> {rule}\n'

        print(rules)

        # Look for the Send Message button, then enable it.
        # We're using `#type: ignore` to stop Pylance from complaining.
        send_button = [child for child in self.children
                       if child.custom_id=='send_message'][0] #type: ignore
        send_button.disabled = False #type: ignore

        # Edit the message to refresh.
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Send Message',
                       style=discord.ButtonStyle.blurple,
                       custom_id='send_message',
                       disabled=True)
    async def send_message(self,
                           interaction: discord.Interaction,
                           button: discord.ui.Button):
        """When the \"Send Message\" button is selected."""
        self.confirm=True
        print(self.values)
        self.stop()

    @discord.ui.button(label='Cancel',
                       style=discord.ButtonStyle.red,
                       custom_id='cancel_button')
    async def cancel_button(self,
                           interaction: discord.Interaction,
                           button: discord.ui.Button):
        """When the \"Cancel\" button is selected."""
        self.confirm=False
        self.stop()

    def sorting_key(self, key):
        """
        Custom key method to extract the numberic part of the 
        selection.
        """
        number = int(key.split(".")[0])
        return number
