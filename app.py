import os.path
import pathlib
import requests
from database import Add_Client, Delete_Conteiner

from pip._vendor import cachecontrol
from flask import Flask, session, abort, redirect, request

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import subprocess

app = Flask("Google Login Flask App")
app.secret_key = "GoogleLoginTestCode"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "965585679534-5bda3akurikq2ocsbpuhdp054fsk78a3.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


conteiner_ids = []


def docker_run():
    cmd = f'docker run -d --name docker_theia3000 -p 3000:3000 -v "$(pwd):/home/project:cached" elswork/theia'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-1]
    print(result)
    return result


def docker_remove(id):
    cmd = f'docker rm -f {id}'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-1]
    print(result)
    return result


def login_is_required(func):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return func()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    print(id_info.get("email"))
    username = id_info.get("email")
    conteiner = docker_run() #это надо бы сделать как глобальную переменную, чтобы потом знать что удалять или как-то иначе
    conteiner_ids.append(conteiner)
    Add_Client(username, conteiner)
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    conteiner = conteiner_ids[0]
    docker_remove(conteiner)
    Delete_Conteiner(conteiner)
    conteiner_ids.pop(0)
    session.clear()
    return redirect('/')


@app.route("/")
def index():
    return "Hello World!  <a href='/login'><button> Login </button></a>"


@app.route("/protected_area")
@login_is_required
def protected_area():
    return "PROTECTED! <a href='/logout'><button> Logout </button></a> <br>" \
           "Conteiner <a href='/conteiner'><button> Conteiner </button></a>"


@app.route("/conteiner")
def conteiner():
    return redirect("http://127.0.0.1:3000")


if __name__ == "__main__":
    app.run(debug=True)
