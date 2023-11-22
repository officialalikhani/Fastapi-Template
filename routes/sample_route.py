from fastapi import APIRouter, Response
from security.auth import *
import traceback

router = APIRouter(tags=["SAMPLE"])


@app.get("/get-servers", dependencies=[Depends(has_permission)])
def set_config(
    response: Response,
    current_user: User = Depends(get_current_active_user),
):
    try:
        response.status_code = 200
        return {"success": True, "message": "OK", "data": "res"}
    except Exception:
        err = traceback.format_exc()
        response.status_code = 404
        return {"success": False, "message": "Error", "data": err}
