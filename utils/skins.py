from mojang import MojangAPI


def get_head(ign: str) -> str:
    return f"https://crafatar.com/renders/head/{MojangAPI.get_uuid(ign)}"


def get_body(ign: str) -> str:
    return f"https://crafatar.com/renders/body/{MojangAPI.get_uuid(ign)}"


def get_avatar(ign: str) -> str:
    return f"https://crafatar.com/avatars/{MojangAPI.get_uuid(ign)}"
