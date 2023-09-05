
from flask import Blueprint, request, g, current_app

from api.responses import (
    response_with,
    SUCCESS_204,  
)
from services.follow import follow_entity
from api.middleware.auth import require_role

follows_bp = Blueprint("follows", __name__)


@follows_bp.route('/follows", ')


#POST /follows - follow an entity
@follows_bp.route('/follows', methods=['POST'])
@require_role('user')
def follow_entity_req(entity_id, entity_type):
    user_id = g.user_id 
    entity_type = "playlist"
    user_id = request.json.get('user_id')
    try:
        follow_entity(user_id, entity_id, entity_type)
        return response_with(SUCCESS_204)
    except Exception:
        pass



# DELETE /follows/{follow_id} - unfollow an entity

# GET /users/{user_id}/follows

# GET /users/{user_id}/follows/{entity_id}?type=<enum>

# GET /follows/recent

