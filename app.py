from utils import *

###################### Import Blueprints ######################
from views.projects.views import projects_
from views.authentication.views import authentication_
from views.settings.views import settings_
from views.skillCheck.views import skillCheck_
from views.friends.views import friends_
from views.jobsandinternships.views import jobsandinternships_
###############################################################

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] =  timedelta(minutes=10)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*5

###################### Register Blueprints ######################
app.register_blueprint(projects_)
app.register_blueprint(authentication_)
app.register_blueprint(settings_)
app.register_blueprint(skillCheck_)
app.register_blueprint(friends_)
app.register_blueprint(jobsandinternships_)
#################################################################

db.init_app(app)
login.init_app(app)
login.login_view = "authentication.login"

@app.before_first_request
def create_all():
    db.create_all()

@app.errorhandler(404)
def page_not_found_(e):
    return render_template("error/404.html"), 404

@app.errorhandler(405)
def page_not_foun_(e):
    return render_template("error/404.html"), 405

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    user = UserModel.query.filter_by(name = session["username"]).first()
    data = {
        "username": session["username"],
        "user": user
    }
    return render_template("index.html",  data = data)

@app.route("/user-profile/<id>", methods = ["GET"])
@login_required
def user_profile(id):
    user = UserModel.query.filter_by(name = id).first()
    projects = ProjectsModel.query.filter_by(user_name = id)
    friend1 = FriendModel.query.filter_by(user1 = id, status = 1).all()
    friend2 = FriendModel.query.filter_by(user2 = id, status = 1).all()
    all_users = UserModel.query.all()
    data = {
        "projects": projects,
        "my_id": session["id"],
        "user": user,
        "all_users": all_users,
        "friend1": friend1,
        "friend2": friend2,
        "my_name": session["username"]
    }
    return render_template("user-profile.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)