check_mark = ":white_check_mark:"
x_mark = ":x:"
popper = ":tada:"
pencil = ":pencil:"
OKGREEN = '\033[92m'
OKCYAN = '\033[96m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
YELLOW = '\033[33m'
ENDC = '\033[0m'

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator
    