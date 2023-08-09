
def get_auth_header(jwt_token):
    return {
        "Authorization": f"Bearer {jwt_token}"
    }