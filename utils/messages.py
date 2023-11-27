"""
Lists the messages available for Cephalon Seren.
"""

beginner = {
    'INTRO': (
        "Hi, {username}! Welcome to Shinobi of the Lotus. "
        "I\'m Cephalon Seren, a moderator bot in this server. "
        "Thanks for joining in!\n\n"
        "Tell me: are you here to join the Shinobi of the Lotus clan?\n"
        "Or maybe you want to join one of our clans in our alliance?\n"
        "Or maybe you\'re already a member of a clan in here?\n\n"
        "Please select an option."
        ),
    'DROPDOWN_OPTION_1': "I\'m joining the Shinobi of the Lotus clan.",
    'DROPDOWN_OPTION_2': "I\'m joining a clan in this alliance.",
    'DROPDOWN_OPTION_3': "I\'m already a member of one of the clans.",
    'OPTION_1_RESPONSE': (
        "Thanks for letting me know! I\'ll let an admin know and they\'ll "
        "be with you soon."
        ),
    'OPTION_2_RESPONSE': (
        "Great! In the server, you\'ll find {billboards}. Look through "
        "the list and see which ones you may be interested in. "
        "If you\'d like, you can even create your own!"
        ),
    'OPTION_3_RESPONSE': "Great! Enjoy your stay in the server.",
    'INVITE_INTEREST': "{username} has requested to be part of the clan.",
    'INVITE_ACCEPT': (
        "I\'ve added the roles to the member. They should "
        "now be able to access the clan-only channels."
        ),
    'INVITE_DECLINE': "I\'ve declined the member\'s request.",
    'INVITE_REJECTED': (
        "It seems like the admins didn\'t let you in. "
        "Please speak to one to find out why."
        )
}

requests = {
    'DRIFTER_REQUEST': (
        "Your request was delivered to our admins! If everything is "
        "cleared, they\'ll let you in."
        ),
    'DRIFTER_INTEREST': (
        "{username} has requested to enter the adult-only channels."
        ),
    'DRIFTER_ACCEPT': (
        "I\'ve added the role to the member. They should now be able "
        "to see the channels."
        ),
    'DRIFTER_DECLINE': "I\'ve declined the member\' request.",
    'DRIFTER_APPROVED': "You can now access the adult-only channels!",
    'DRIFTER_REJECTED': (
        "It seems like the admins didn\'t let you in. Please speak to "
        "one to find out why."
        ),
    'OPERATOR_ADD': (
        "I\'ve added the Operator role. You can access the alliance "
        "channels again!"
        ),
    'OPERATOR_REMOVE': (
        "I\'ve removed the Operator role. You\'ll only see the clan "
        "and adult-only channels now. If you want to re-add the role, "
        "just use this command again."
        )
}

admin = {
    'WARN_MESSAGE': (
        "Hello, {member}!\n\nJust a heads up from Cephalon Seren! "
        "I noticed a bit of a hiccup in your recent actions within our "
        "server. Don't sweat it, everyone's on a learning path here, "
        "but we do need to keep our server harmonious and respectful for "
        "all. So, consider this a friendly nudge to realign with our "
        "alliance's ethos.\n\nThe rules below are the one's I'm talking "
        "about:\n{rules}\nWe're an alliance that thrives on honor and "
        "respect, and part of that is adhering to the guidelines we've "
        "all agreed to. We're not about being heavy-handed, but if "
        "these hiccups continue, we might have to take a tougher stance, "
        "which could lead to a kick or even a ban.\n\nWe value you as part "
        "of the alliance. Everyone's welcome here, but we all need to "
        "follow the rules set in here. So let's get back on track!\n"
        ),
    'WARN_SENT': "I\'ve sent the message over to the member.",
    'WARN_CANCEL': "I\'ve cancelled the action."
}

clan_ad = {
    'CLAN_AD_0x0': "We're now open for invite requests.",
    'CLAN_AD_0x1': "We're pausing invite requests for now.",
    'CLAN_AD_0x2': "Our clan is full at the moment."
}

misc = {
    'UPLOAD_EMBLEM': (
        "To upload your clan emblem, use the slash command "
        "\"/billboard upload\" and drag and drop your clan emblem.")
}
