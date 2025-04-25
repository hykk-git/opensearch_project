import jwt
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

# AUTHENTICATION_BACKENDS 오버라이딩
class OIDCBackend(OIDCAuthenticationBackend):
    def get_userinfo(self, access_token, id_token, payload):
        # Access token 디코딩
        try:
            decoded_access = jwt.decode(access_token, options={"verify_signature": False})
            print("access token: ", decoded_access)
        except Exception as e:
            print("access token error:", e)

        # payload만 리턴하면 /userinfo를 호출하지 않음
        return payload
    
        # /userinfo를 호출할 때 사용  
        # return super().get_userinfo(access_token, id_token, payload)
