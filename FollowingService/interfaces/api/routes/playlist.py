

from flask import Blueprint, request, g, current_app

from api.responses import (
    response_with,
    SUCCESS_204,  
)
from services.follow import follow_entity
from api.middleware.auth import require_role


follows_bp = Blueprint("follows", __name__)

#POST /follows - follow an entity
@follows_bp.route('/follows', methods=['POST'])
@require_role('user')
def follow_entity_req(entity_id, entity_type):
    user_id = g.user_id 
    entity_type = "playlist"
    user_id = request.json.get('user_id')

    follow_entity(user_id, entity_id, entity_type)
    pass


# POST /playlists/{playlist_id}/follow

# DELETE /playlists/{playlist_id}/follow

# GET /playlists/{playlist_id}/follow?user_id

# GET playlists/{playlist_id}/followers

# GET users/{user_id}/follows?entity=playlists

# GET uesrs/me/follows?entity=playlists
