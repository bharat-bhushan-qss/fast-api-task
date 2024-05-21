import requests
from fastapi import HTTPException, APIRouter, Depends, Query
from src.db.postgres_manager import get_db
from src.models.auth import UserBase, UserOut
from src.api.crud.auth import create_user, get_current_user, authenticate
from starlette.responses import RedirectResponse
from src.config import ( 
    AUTH0_DOMAIN, 
    API_AUDIENCE, 
    CLIENT_ID, 
    CLIENT_SECRET,
    REDIRECT_URI
    )


###################### Routes ##########################

v1_auth_router = APIRouter()

########################################### with JWT implmentation #########################################################


@v1_auth_router.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}


@v1_auth_router.post("/register", response_model=UserOut)
async def register(user: UserBase, db=Depends(get_db)):
    try:
        return await create_user(db, user)
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


########################################### with Auth0 implmentation #########################################################


@v1_auth_router.get("/login")
async def login():
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"
    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "audience": API_AUDIENCE
    }
    auth_url_with_params = auth_url + "?" + "&".join([f"{key}={value}" for key, value in auth_params.items()])
    print("Authorization URL:", auth_url_with_params)
    return RedirectResponse(url=auth_url_with_params)


@v1_auth_router.get("/callback")
async def callback(code: str = Query(...)):
    print(f"code: {code}")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"content-type": "application/json"}
    token_response = requests.post(token_url, json=token_data, headers=headers)
    token_response_data = token_response.json()
    if "access_token" not in token_response_data:
        raise HTTPException(status_code=400, detail="Failed to fetch token")
    access_token = token_response_data["access_token"]
    return RedirectResponse(url=f"/v1/userinfo?access_token={access_token}")


@v1_auth_router.get("/userinfo", response_model=UserOut)
async def userinfo(access_token: str):
    try:
        userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo_data = userinfo_response.json()
        print(f"userinfo_data: {userinfo_data}")
        return UserOut(access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
