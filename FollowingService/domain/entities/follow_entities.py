


class FollowRecord:
    def __init__(self, follower:'FollowerEntity', followee:'FolloweeEntity'):
        self.follower = follower
        self.followee = followee

    @property 
    def followee_type(self):
        return self.followee.type


class FollowerEntity:
    def __init__(self, id):
        self.id = id

class FolloweeEntity:
    def __init__(self, id):
        self.id = id


class UserFollowerEntity(FollowerEntity):
    type = "user"
    def __init__(self, id):
        super().__init__(id)



class UserFolloweeEntity(FolloweeEntity):
    type = "user"
    def __init__(self, id):
        super().__init__(id)

class PlaylistFolloweeEntity(FolloweeEntity):
    type = "playlist"
    def __init__(self, id):
        super().__init__(id)

class ArtistFolloweeEntity(FolloweeEntity):
    type = "artist"
    def __init__(self, id):
        super().__init__(id)


FOLLOWABLE_TYPE_REGISTRY = {
    "user": UserFolloweeEntity,
    "playlist": PlaylistFolloweeEntity,
    "artist": ArtistFolloweeEntity
}


