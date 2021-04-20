import asyncio

from fastapi import Depends
from fastapi.routing import APIRouter, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse

from app import schemas, models
from app.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


html_sse = """
    <html>
    <body>
        <script>
            var evtSource = new EventSource("/cookie/stream");
            console.log("evtSource: ", evtSource);
            evtSource.onmessage = function(e) {
                document.getElementById('response').innerText = e.data;
                console.log(e);
                if (e.data == 20) {
                    console.log("Closing connection after 20 numbers.")
                    evtSource.close()
                }
            }
        </script>
        <h1>Response from server:</h1>
        <div id="response"></div>
    </body>
</html>
"""


async def cookiegen(request, db):
    while True:
        # get last added cookie
        cookie = (
            db.query(models.Cookie)
            .order_by(models.Cookie.id.desc())
            .first()
        )
        if cookie:
            message = cookie.message
        else:
            message = "no fortune cookies for you"
        if await request.is_disconnected():
            break
        yield message
        await asyncio.sleep(0.5)


@router.get("/")
def home():
    return HTMLResponse(content=html_sse, status_code=200)


@router.get("/stream")
async def get_latest_cookie(request: Request, db: Session = Depends(get_db)):
    event_generator = cookiegen(request, db)
    return EventSourceResponse(event_generator)


@router.post("/create", response_model=schemas.Cookie)
def create_cookie(
    cookie: schemas.CookieCreate, db: Session = Depends(get_db)
) -> models.Cookie:
    cookie = models.Cookie(message=cookie.message)
    db.add(cookie)
    db.commit()
    db.refresh(cookie)
    return cookie
