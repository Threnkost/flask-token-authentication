from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)
from flask import (
    Flask,
    request,
    make_response,
    render_template,
)
from hashlib import (
    sha256
)
import os
from time import (
    time
)
from models.token import Token
from models.user import User
from models.base import Base


def create_token(min_expires: int, user_for):
    creation_time = time()
    expires_at    = time() + min_expires * 60
    token         = sha256(str(creation_time).encode("utf-8")).hexdigest()
    
    token_instance = Token(
        user=user_for,
        token=token,
        created_at=creation_time,
        expires_at=expires_at
    )
    
    token_data = {
        "instance": token_instance,
        "user": user_for,
        "token": token,
        "expires_at": expires_at,
        "creation_time": creation_time
    }
    return token_data

def is_token_valid(token):
    token_instance = session.query(Token).filter_by(token=token).one_or_none()
    
    if not token_instance:
        return False
    
    if time() >= token_instance.expires_at:
        return False
    
    return True

def is_app_json():
    return request.content_type and request.content_type == "application/json"


engine = create_engine("sqlite:///mydb.db", echo=True)
app = Flask(__name__)
Session = sessionmaker(bind=engine)
session = Session()


def token_required(func):
    def wrapper(*args, **kwargs):
        context = {}
        token = None
        bearer_token = ""

        if "Authorization" in request.headers:
            bearer_token = request.headers["Authorization"]

        elif request.args.get('token'):
            context['message'] = request.form.get('token')
            context['status']  = 200
            bearer_token = request.args.get('token')
    
        split = bearer_token.split(" ")
        if split[0] != "Bearer":
            context['message'] = "Wrong token format."
            context['status']  = 400
                
            return make_response(context) if (
                is_app_json()
            ) else render_template("unauthorized.html", context=context)
        token = split[1]
        
        if not token:
            context['message'] = "Token is missing."
            context['status']  = 401
            
            return make_response(context) if (
                is_app_json()
            ) else render_template("unauthorized.html", context=context)
                    
        if not is_token_valid(token):
            context['message'] = "Token is not valid."
            context['status']  = 401
            
            return make_response(context) if (
                is_app_json()
            ) else render_template("unauthorized.html", context=context)

        return func()
    
    return wrapper


@app.route('/api')
@token_required
def get_api():
    return "api"


if __name__ == '__main__':

    if os.path.exists("mydb.db"):
        os.remove("mydb.db")

    Base.metadata.create_all(bind=engine)
    
    user1 = User(
        username="admin",
        password=sha256("123".encode("utf-8")).hexdigest()
    )
    
    token = create_token(10, 1)
    
    session.add(user1)
    session.add(token["instance"])
    session.commit()
    session.close()
    
    app.run()