from utils import *
import openai
import json
from Bard import Chatbot
import requests

skillCheck_ = Blueprint('skillCheck', __name__)

UPLOAD_FOLDER = "static/Uploads/profile-picture"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

openai.api_key = "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"
answers = []
questions = []


@skillCheck_.route("/skillcheck", methods = ["GET", "POST"])
@login_required
def settings():
    user = UserModel.query.filter_by(id = session["id"]).first()
    userdata = {
        "username": session["username"],
        "user": user
    }
    if request.method == "POST":
        skill = request.form.get("skill")
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "10 {skill} mcq questions along with their answers in json".format(skill=skill)}])
    print(completion)
    try:
        questions1 = json.loads(completion.choices[0].message.content)
        for i in questions1['questions'] if ("questions" in questions1) else questions1:
            questions.append(i)
            answers.append(i['answer'])
        print(questions)
        data = {
            "userdata": userdata,
            "questions": questions1['questions'] if ("questions" in questions1) else questions1
        }
        return render_template("/skill-check/skillCheck.html", data=data)
    except:
        return render_template("error/apifail.html")

@skillCheck_.route("/answers", methods = ["GET", "POST"])
def check():
    print(questions)
    user = UserModel.query.filter_by(id = session["id"]).first()
    userdata = {
        "username": session["username"],
        "user": user
    }
    data = {
            "userdata": userdata
        }
    score = 0
    for q in questions:
        answer = request.form.get(q['question'])
        print(answer, q['answer'])
        if answer == q['answer']:
            score += 1
    return render_template('/skill-check/score.html', score=score, data=data)

@skillCheck_.route("/jobsearch", methods = ["GET", "POST"])
@login_required
def jobsearch():
    user = UserModel.query.filter_by(name = session["username"]).first()
    data = {
        "username": session["username"],
        "user": user
    }
    return render_template("/skill-check/jobsearch.html",  data = data)
    
@skillCheck_.route("/jobs", methods = ["GET", "POST"])
@login_required
def jobs():
   
    skill = 'Web development'
    if request.method == "POST":
        skill = request.form.get("skill")
    user = UserModel.query.filter_by(id = session["id"]).first()
    userdata = {
        "username": session["username"],
        "user": user
    }
    url = "http://api.adzuna.com/v1/api/jobs/in/search/1?app_id=7391aa45&app_key=5ea1bd3421b58dfb952d05730ee549e2&results_per_page=25&what_or={}&where={}&distance={}&max_days_old={}"
    r = requests.get(url.format(skill, 'Mumbai', 1, 1)).json()
    data = {
            "userdata": userdata,
            "jobs": r['results']
        }
    return render_template("/skill-check/jobs.html", data=data)


