from flask import g
from flask.views import MethodView

from services.follow import follow_entity, unfollow_entity, get_follow_status,
from api.middleware.auth import require_role


from api.responses import (
    response_with,
    SUCCESS_204,  
    ERROR_400,
)

decorator1 = None
decorator2 = None

# {entity_type}/{entity_id}/follow
class BaseFollowView(MethodView):
    decorators = [require_role('user')]
    entity_type = None

    def get(self, entity_id):
        print(f"Checking status for {self.entity_type} with ID of {entity_id}.")
        user_id = g.user_id
        try:
            status = get_follow_status(user_id, entity_id, self.entity_type)
            return response_with(SUCCESS_204, status)
        except Exception:
            return response_with(ERROR_400)


    def post(self, entity_id):
        print(f"Following {self.entity_type} with ID of {entity_id}.")
        user_id = g.user_id
        try:
            follow_entity(user_id, entity_id, self.entity_type)
            return response_with(SUCCESS_204)
        except Exception:
            return response_with(ERROR_400)

    def delete(self, entity_id):
        print(f"Unfollowing {self.entity_type} of ID {entity_id}.")
        user_id = g.user_id
        try:
            unfollow_entity(user_id, entity_id, self.entity_type)
            return response_with(SUCCESS_204)
        except Exception:
            return response_with(ERROR_400)

class UserFollowView(BaseFollowView):
    decorators = BaseFollowView.decorators + [decorator2]
    entity_type = "user"


class PlaylistFollowView(BaseFollowView):
    entity_type = "playlist"

class ArtistFollowView(BaseFollowView):
    entity_type = "artist" 


app = "dummy"
user_follow_view = UserFollowView.as_view('user_follow')
playlist_follow_view = PlaylistFollowView.as_view('playlist_follow')
artist_follow_view = ArtistFollowView.as_view('artist_view')

app.add_url_rule('/users/<int:entity_id>/follow', view_func=user_follow_view, methods=['POST'])