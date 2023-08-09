from enum import Enum

class Resource(str, Enum):
    PLAYLIST = "playlist"
    USER = "user"
    SONG = "song"
    ARTIST = "artist"

class Action(str, Enum):
    DELETE = "delete"
    READ = "read"
    EDIT = "edit"
    CREATE = "create"

class Owner(str, Enum):
    OWN = "own"
    ANY = "any"


PLAYLIST_READ_ANY = f"{Resource.PLAYLIST.value}:{Action.READ.value}:{Owner.ANY.value}"
PLAYLIST_EDIT_ANY = f"{Resource.PLAYLIST.value}:{Action.EDIT.value}:{Owner.ANY.value}"
PLAYLIST_DELETE_ANY = f"{Resource.PLAYLIST.value}:{Action.DELETE.value}:{Owner.ANY.value}"
PLAYLIST_CREATE_ANY = f"{Resource.PLAYLIST.value}:{Action.CREATE.value}:{Owner.ANY.value}"

#PLAYLIST_EDIT_OWN = f"{Resource.PLAYLIST.value}:{Action.EDIT.value}:{Owner.OWN.value}"

# class PermissionEnum(str, Enum):
#     PLAYLIST_EDIT_OWN = f"{Resource.PLAYLIST}:{Action.DELETE}:{Owner.OWN}"
#     PLAYLIST_DELETE_OWN = "playlist:delete:own"
#     PLAYLIST_DELETE_ANY = "playlist:delete:any"



#     # ... add other permissions as needed


