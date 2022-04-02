from mojang import MojangAPI


def get_head(ign: str) -> str:
    return f"https://visage.surgeplay.com/renders/head/{MojangAPI.get_uuid(ign)}"


def get_body(ign: str, size: int) -> str:
    return f"https://visage.surgeplay.com/full/{size}/{MojangAPI.get_uuid(ign)}"


def get_avatar(ign: str) -> str:
    return f"https://visage.surgeplay.com/face/{MojangAPI.get_uuid(ign)}"
