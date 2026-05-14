import jwt
from fastapi import Header, HTTPException

SECRET = "mysecret"

def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"]
        )

        if "write:risk_test" not in payload["scope"]:
            raise HTTPException(
                status_code=403,
                detail="Invalid Scope"
            )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )