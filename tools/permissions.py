from users import USERS


def authorized(author):
    # Returns true if author is on the authorized users list
    if str(author) in USERS:
        return True
    return False
