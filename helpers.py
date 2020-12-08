import os
from dotenv import load_dotenv
load_dotenv()

check_mark = ":white_check_mark:"
check_mark_unicode = u"\u2705"
x_mark = ":x:"
popper = ":tada:"
pencil = ":pencil:"
OKGREEN = '\033[92m'
OKCYAN = '\033[96m'
UNDERLINE = '\033[4m'
YELLOW = '\033[33m'
ENDC = '\033[0m'

admin_override_ids = os.getenv('OVERRIDE_ADMIN_IDS')
admin_override_ids = [int(admin_id.strip()) for admin_id in admin_override_ids.split(',')] if admin_override_ids is not None else []

def is_admin(ctx):
    return ctx.author.id in admin_override_ids or ctx.author.guild_permissions.administrator
    