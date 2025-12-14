import hashlib

import flask
from flask import Flask, jsonify, request, session , url_for , redirect , render_template
from flask_cors import CORS  # To allow JS from another origin

import  logging
from date_base_cubing import user
from date_base_cubing.user import *
from date_base_cubing import event
from date_base_cubing import group
from date_base_cubing import result
import os


logging.basicConfig(
    level=logging.DEBUG,  # niveau de détail
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),  # fichier app.log
        logging.StreamHandler()                           # terminal
    ]
)

app = Flask(__name__)
CORS(app , supports_credentials=True)
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key =  os.getenv('MAKLETRESSCRET')


def hash_password(password: str) -> str:
    logging.info(f"hashing password {password}")
    return hashlib.sha512(password.encode("utf-8")).hexdigest()

def avg(list_time,AoWhat):
    list_avg_time= []
    list_list_avg = []
    for i in range(len(list_time)-(AoWhat-1)):
        for y in range(AoWhat):
            list_avg_time.append(list_time[y+i])
        list_list_avg.append(list_avg_time)
        print(list_avg_time)
        list_avg_time = []
    print(list_list_avg)
    avg_f_list = []
    for i in list_list_avg:
        worst = 0
        best = 0
        for y in i:
            if y > worst or worst == 0:
                worst = y
            if best == 0 or y < best:
                best = y
        print(f"{best} : {worst}")
        sum = 0
        for y in  i:
            sum += y
        sum -= worst
        sum -= best
        avg_f_list.append(sum/(AoWhat-2))
    return avg_f_list





def user_command(command, args):
    out = {}
    if command == "add":
        out = user.add_users(args[0], args[1], hash_password(args[2]), False, args[4])
    if command == "remove":
        out = user.del_users(args[0])
    if command == "get_user":
        out = user.get_users(args[0])
    if command == "get_users":
        out = user.get_all_users()
    if command == "get_user_by_name":
        out = user.get_users_by_name(args[0])
    if command == "connect":
        logging.info(f"connecting to {args[0]}")
        logging.info(f"gived password {args[1]}")
        #args 1 is username
        #args 2 is password
        use_password = hash_password(args[1])
        logging.info(f"hashing password {use_password}")
        _user = user.get_users_by_name(args[0])[0]
        logging.info(f"user {_user}")
        out = _user['password'] == use_password
        logging.info(f"{out}")
        if not out:
            logging.warn(f"user {args[0]} password {use_password} is incorrect or dosen't exist")

    return out


@app.route("/profil/<int:user_id>/detail")
def profile_page(user_id):
    current_user = session["user_id"]
    _user = user.get_users(user_id)[0]
    _username = _user['name']
    _user_wca = _user['wca']
    _usericon = _user['icon']
    logging.info(f"curentuser {current_user} , username {_username} , user_wca {_user_wca} , usericon {_usericon}")

    if user_id == current_user:
        logging.info(f"user{current_user} look is own page and got redirected to is profile page /profil")
        return redirect(url_for("profile_soy_page"))

    return render_template("profile.html", id=user_id , name = _username, wca = _user_wca, icon = _usericon )

@app.route("/profil")
def profile_soy_page():
    current_user = session["user_id"]
    user_id = current_user
    _user = user.get_users(user_id)[0]
    _username = _user['name']
    _user_wca = _user['wca']
    _usericon = _user['icon']

    logging.info(f"user{current_user} look is own page /profil")
    return render_template("profile.html", id=user_id , name = _username, wca = _user_wca, icon = _usericon )

@app.route("/profil/edit")
def profile_edit_page():
    current_user = session["user_id"]
    _user = user.get_users(current_user)[0]
    _username = _user['name']
    _user_wca = _user['wca']
    _usericon = _user['icon']
    _userpassword = _user['password']

    logging.info(f"user{current_user} edit is profil")

    return render_template("profile_edit.html", id=current_user, name=_username, wca=_user_wca, icon=_usericon , password = _userpassword )


@app.route("/index")
def index_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("index.html")

@app.route("/event_maker")
def event_maker_page():
    current_user = session["user_id"]
    logging.info(f"user{current_user} make a event")
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("event_maker.html")

@app.route("/get", methods=["GET"])
def index():
    logging.info(f"a user get if is connected")
    if "user_id" not in session:
        logging.info("not logged in")
        return jsonify({"logged_in": False})
    logging.info(f"user connect {True} , {session.get("username")} , {session.get("user_id")}")
    return jsonify({
        "logged_in": True,
        "username": session.get("username"),
        "user_id": session.get("user_id")
        })

@app.route("/")
def root():
    logging.info(f"user on home page")
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def login_page():
    logging.info(f"user on login page")
    if "user_id" in session:
        return redirect(url_for("index_page"))
    #Sinon affiche la page de login
    return render_template("login.html")

@app.route("/events/<int:event_id>/detail")
def event_view_page(event_id):
    current_user = session["user_id"]
    logging.info(f"user{current_user} view a event {event_id}")
    _event = event.get_event_by_id(event_id)[0]
    event_name= _event["name"]
    event_icon = _event["icon"]
    event_maker_id = _event["makerid"]
    event_rule = _event["rule"]
    if event_maker_id == current_user:
        logging.info(f"user{current_user} is the maker of event {event_id} and he got redirected to is event page")
        return redirect(url_for("event_edit_page", event_id=event_id))

    return render_template("event_viewer.html" , id=event_id, name=event_name, icon=event_icon, maker_id=event_maker_id , rule=event_rule)

@app.route("/events/<int:event_id>/edit")
def event_edit_page(event_id):
    _event = event.get_event_by_id(event_id)[0]
    current_user = session["user_id"]
    logging.info(f"user{current_user} edit a event {event_id},{_event}")
    event_name= _event["name"]
    event_icon = _event["icon"]
    event_maker_id = _event["makerid"]
    event_rule = _event["rule"]
    if event_maker_id != current_user:
        logging.info(f"user{current_user} try to edit event {event_id},{_event} but he is not the maker of event {event_maker_id},{event_id}")
        return redirect(url_for("event_view_page",event_id = event_id))

    return render_template("event_editor.html" , id=event_id, name=event_name, icon=event_icon, maker_id=event_maker_id , rule=event_rule)


@app.route("/register", methods=["GET"])
def regsiter_page():
    logging.info(f"user on register page")
    return render_template("register.html")

@app.route("/logout", methods=["GET"])
def logout_page():
    current_user = session["user_id"]
    logging.info(f"user {current_user}  logout")
    session.clear()
    return render_template("login.html")

@app.route("/events", methods=["GET"])
def event_page():
    current_user = session["user_id"]
    logging.info(f"user{current_user} on events page")
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("events_list.html")

@app.route("/group")
def group_page():
    current_user = session["user_id"]
    logging.info(f"user{current_user} on groups page")

    return render_template("group.html")

@app.route("/group/<int:group_id>/detail")
def group_detail_page(group_id):
    _group = group.get_group(group_id)[0]
    logging.info(f"group {_group} detail page {group_id}")
    current_user = session["user_id"]
    logging.info(f"user{current_user} on group {_group} detail page")
    _group_name = _group["name"]
    _group_icon = _group["icon"]
    _group_maker_id = _group["makerid"]
    logging.info(f"user{current_user} with info for {_group} ,{_group_name} ,{_group_icon} ,{_group_maker_id} ")
    _user = user.get_users(current_user)[0]
    logging.info(f"current user {_user} ")
    _user["id_user"] = current_user
    _user["id_group"] = group_id
    if _user in group.get_all_user_from_group(group_id):
        logging.info(f"user{current_user}  is redirected to the group management page")
        return redirect(url_for("group_management_page", group_id = group_id))

    return render_template("group_view.html", id = group_id , name = _group_name, icon = _group_icon, maker_id = _group_maker_id)

@app.route("/group/<int:group_id>/management")
def group_management_page(group_id):
    current_user = session["user_id"]
    logging.info(f"user{current_user} on group {group_id} management page")
    _group = group.get_group(group_id)[0]
    _group_name = _group["name"]
    _group_icon = _group["icon"]
    _group_maker_id = _group["makerid"]
    _user = user.get_users(current_user)[0]
    _user["id_user"] = current_user
    _user["id_group"] = group_id
    if _user not in group.get_all_user_from_group(group_id):
        logging.info(f"user{current_user}  is redirected to the group detail page")
        return redirect(url_for("group_detail_page", group_id=group_id))
    if current_user == _group_maker_id:
        logging.info(f"user{current_user}  is redirected to the group admin page")
        return redirect(url_for("group_admin_page", group_id=group_id))
    logging.info(f"user{current_user} use args {_group_name},{_group_icon} ,{_group_maker_id} for managment")
    return render_template("group_edit.html", id = group_id , name = _group_name, icon = _group_icon, maker_id = _group_maker_id)

@app.route("/group/maker")
def group_maker_page():
    current_user = session["user_id"]
    logging.info(f"user{current_user} on group maker page")


    return render_template("group_maker.html")

@app.route("/group/<int:group_id>/admin")
def group_admin_page(group_id):
    current_user = session["user_id"]
    logging.info(f"user{current_user} on group admin page")
    logging.info(f"user{current_user} on group {group_id} management page")
    _group = group.get_group(group_id)[0]
    _group_name = _group["name"]
    _group_icon = _group["icon"]
    _group_maker_id = _group["makerid"]
    _user = user.get_users(current_user)[0]
    if current_user != _group_maker_id:
        logging.info(f"user{current_user}  is redirected to the group admin page")
        return redirect(url_for("group_admin_page", group_id=group_id))
    return render_template("group_admin.html" ,  id = group_id , name = _group_name, icon = _group_icon, maker_id = _group_maker_id)

@app.route("/group/maker")
def  group_maker():
    current_user = session["user_id"]
    logging.info(f"user{current_user} is making a group")
    return render_template("group_maker.html")

@app.route("/user/result/<int:user_id>/<int:event_id>")
def result_page(user_id,event_id):


    return render_template("result.html", id_user = user_id , id_event = event_id )
@app.route("/group/result/<int:group_id>/<int:event_id>")
def result_group_page(group_id,event_id):


    return render_template("result_group.html", id_group = group_id , id_event = event_id )




#api command
@app.route('/api/v0/user/add', methods=['POST'])
def add():
    out = ""
    data = request.get_json()
    logging.info(f"add user : {data}")
    out = user_command("add", data.get("args", []))
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/user/remove', methods=['POST'])
def remove():
    out = ""
    data = request.get_json()
    logging.info(f"remove user : {data}")
    out = user_command("remove", data.get("args", []))
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/user/get', methods=['POST'])
def get():
    out = ""
    data = request.get_json()
    logging.info(f"get user : {data}")
    out = user_command("get_user", data.get("args", []))
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/user/get_all', methods=['POST'])
def get_all():
    out = ""
    data = request.get_json()
    logging.info(f"get all user : {data}")
    out = user_command("get_users", data.get("args", []))
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/user/connect', methods=['POST'])
def connect():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"connect user : {args}")
    if get_users_by_name(args[0]) != []:
        logging.info(f"user exist in database {args[0]}")
        valid = user_command("connect", args)
        logging.info(valid)
        if valid:
            logging.info(f"user {args[0]} connected")
            _user = user.get_users_by_name(args[0])[0]
            session["username"] = _user["name"]
            session["user_id"] = _user["id"]
            logging.info(f"{session} connected")
            logging.info(f"{jsonify({
                "logged_in": True,
                "username": _user["name"],
                "user_id": _user["id"]
            })}")
            return jsonify({
                "logged_in": True,
                "username": _user["name"],
                "user_id": _user["id"]
            })
    logging.info(f"{jsonify({"logged_in": False})}")
    return jsonify({"logged_in": False})

@app.route('/api/v0/user/edit', methods=['POST'])
def edit_user():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"edit user : {args}")
    user_to_edit = session.get("user_id")
    password = args[2]
    if password == "":
        password = user.get_users(user_to_edit)[0]["password"]
    else:
        password = hash_password(password)
    out = user.edit_users(user_to_edit, args[0], args[1], password, False, args[3])
    logging.info(out)
    return jsonify(out)
@app.route('/api/v0/event/add', methods=['POST'])
def add_event():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"add event : {args}")
    out = event.add_event(args[0],args[1],args[2],args[3])
    logging.info(out)
    return jsonify(out)
@app.route('/api/v0/event/remove', methods=['POST'])
def remove_event():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"remove event : {args}")
    out = event.del_events(args[0])
    logging.info(out)
    logging.info(jsonify({"redirect": url_for("event_page")}))
    return jsonify({"redirect": url_for("event_page")})
@app.route('/api/v0/event/get', methods=['POST'])
def get_event():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get event : {args}")
    out = event.get_event_by_id(args[0])
    logging.info(out)
    return jsonify(out)
@app.route('/api/v0/event/get_all', methods=['POST'])
def get_all_event():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get all event : {args}")
    out = event.get_all_events()
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/event/get_by_name' , methods=['POST'])
def get_by_name():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get event by name: {args}")
    out = event.get_event_by_name(args[0])
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/event/edit' , methods=['POST'])
def edit_event():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"edit event : {args}")
    whoconnect = session.get("user_id")
    event_id = args[0]
    eventmakerid = event.get_event_by_id(event_id)[0]["makerid"]
    out = []
    if whoconnect == eventmakerid :
        out =  event.edit_events(event_id,args[1],args[2],args[3])
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/group/add' , methods=['POST'])
def add_group():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"add group : {args}")
    out = group.add_group(args[0],args[1],current_user)
    group.add_user_to_group(out["id"],current_user)
    logging.info(out)
    return jsonify(out)

@app.route('/api/v0/group/get' , methods=['POST'])
def get_group():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get group : {args}")
    out = group.get_group(args[0])
    logging.info(out)
    return jsonify(out)
@app.route('/api/v0/group/get_all' , methods=['POST'])
def get_all_group():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get all group : {args}")
    out = group.get_all_groups()
    logging.info(out)
    return jsonify(out)
@app.route('/api/v0/group/add_user' , methods=['POST'])
def add_user():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"add user group: {args}")
    out = group.add_user_to_group(args[0],int(args[1]))
    logging.info(out)
    return jsonify(out)
@app.route("/api/v0/group/del" , methods=['POST'])
def del_group():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"del_group : {args}")
    out = group.del_group(args[0])
    logging.info(out)
    return jsonify(out)
@app.route("/api/v0/group/get_all_user_from_group" , methods=['POST'])
def get_all_user_from_group():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get all user from group : {args}")
    out = group.get_all_user_from_group(args[0])
    logging.info(out)
    return jsonify(out)


@app.route("/api/v0/group/get_all_event_from_group" , methods=['POST'])
def get_all_events_from_group():
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get all events from event: {args}")
    out = group.get_all_event_from_group(args[0])
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/group/add_event" , methods=['POST'])
def add_event_group():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"add event group: {args}")
    out = group.add_event_to_group(args[0],args[1])
    logging.info(out)
    return jsonify(out)
@app.route("/api/v0/group/del_event" , methods=['POST'])
def del_event_group():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"del_event group: {args}")
    out = group.del_event_from_group(args[0],args[1])
    logging.info(out)
    return jsonify(out)
@app.route("/api/v0/group/del_user" , methods=['POST'])
def del_user_from_group():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"del_user group: {args}")
    out = group.del_user_from_group(args[0],args[1])
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/group/edit_group" , methods=['POST'])
def edit_group():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"edit group: {args}")
    out = group.edit_group(args[0],args[1],args[2], current_user)
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/result/add_result" , methods=['POST'])
def add_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"add result: {args}")
    out = result.add_result(args[0],args[1],current_user)
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/result/remove" , methods=['POST'])
def remove_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"remove result: {args}")
    out = result.del_result(args[0])
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/result/get" , methods=['POST'])
def get_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get result: {args}")
    out = result.get_result(args[0])
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/result/get_all" , methods=['POST'])
def get_all_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"get all result: {args}")
    out = result.get_all_result()
    logging.info(out)
    return jsonify(out)


@app.route("/api/v0/result/get_user_result" , methods=['POST'])
def get_user_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"user resulr: {args}")
    out = result.get_all_result_from_user_in_event(args[0],args[1])
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/result/get_user_best_result" , methods=['POST'])
def get_user_best_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"user resulr: {args}")
    out = result.get_all_result_from_user_best_in_event(args[0],args[1])
    logging.info(out)
    return jsonify(out)

@app.route("/api/v0/result/get_group_result" , methods=['POST'])
def get_group_result():
    current_user = session.get("user_id")
    data = request.get_json()
    args = data.get("args", [])
    logging.info(f"group result: {args}")
    out = result.get_all_result_from_group(args[1] , args[0])
    logging.info(out)
    return jsonify(out)



print(avg([3303,2709,4706,2366,3833,3834,299,299],5))

if __name__ == "__main__":
    app.run(debug=True)
