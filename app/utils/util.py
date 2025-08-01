from jose import jwt
from datetime import datetime, timedelta, timezone
import jose
from functools import wraps
from flask import request,jsonify
from jose.exceptions import JWTError, ExpiredSignatureError

SECRET_KEY = "super secret secrets"

def encode_token(customer_id):
  payload = {
    'exp':datetime.now(timezone.utc) + timedelta(days=0,hours=1,minutes=0,seconds=0),
    'iat':datetime.now(timezone.utc),
    'sub':str(customer_id)
  }

  token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
  return token

def token_required(f):
  @wraps(f)
  def decorated(*args,**kwargs):
    token = None

    if "Authorization" in request.headers:
      token = request.headers["Authorization"].split()[1]

      if not token:
        return jsonify({"Message":"missing token"}),400
      
      try:
        data = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        # print(data)
        customer_id = data['sub']
      except ExpiredSignatureError:
        return jsonify({"Message":"Token expired"}),400
      except JWTError:
        return jsonify({"Message":"Invalid token"}),400
      return f(*args, **kwargs)
    else:
      return jsonify({"Message":"You need to be logged in first to aaccess this reosource"}),400
  return decorated