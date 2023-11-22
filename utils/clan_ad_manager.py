"""
Manages the clan ads temporarily when using the "/billboard Create Ad"
Slash Command.
"""

class ClanAdManager():
    """Accesses the clan ads within the \"clan_ad_db.py\" file."""
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_user_id(self, user_id=None):
        """
        Determines whether to use `id` or `self.user_id`, depending on if `user_id` is
        not `None`.
        """
        return user_id if user_id is not None else self.user_id

    def create(self, user_id=None, name="", description="", requirements="",
               clan_emblem_url="", invite_status="", message_id=0):
        pass

    def find(self, user_id=None):
        pass

    def read(self, key=None, user_id=None):
        pass

    def update(self, user_id=None, **kwargs):
        pass

    def delete(self, user_id=None):
        pass
