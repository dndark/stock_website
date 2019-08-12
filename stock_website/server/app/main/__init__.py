from flask import render_template
from flask import Blueprint
from flask import url_for
from flask import redirect, request

main = Blueprint('main', __name__,static_folder='static', static_url_path="/static")

@main.before_request
def clear_trailing():
    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])
      
@main.route('/', defaults={'path': ''})

@main.route('/<path:path>')
def index2(path):
  return render_template('index.html')