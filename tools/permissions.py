from users import USERS


def authorized(ctx):
    # Returns true if author is on the authorized users list
    if str(ctx.author) in USERS:
        return True
    return False
