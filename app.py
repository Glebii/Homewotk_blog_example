from flask import Flask, request, Response
from views import register_views
from services import SessionsService


app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SESSION_COOKIE"] = "session_token"


@app.after_request
def attach_session(res: Response):
    st = request.cookies.get(app.config.get("SESSION_COOKIE"))
    if not st:
        session = SessionsService.create_new_session()
        res.set_cookie(app.config.get("SESSION_COOKIE"), session.token)
    return res


register_views(app)

if __name__ == "__main__":
    app.run("localhost", 9999)
