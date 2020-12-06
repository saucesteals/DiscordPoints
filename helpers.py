check_mark = ":white_check_mark:"
x_mark = ":x:"
popper = ":tada:"

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator
    