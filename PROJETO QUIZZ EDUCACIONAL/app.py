from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager, login_user,
    logout_user, login_required, current_user
)

from config import Config
from models import db, User, Question


# -----------------------------
# APP
# -----------------------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# -----------------------------
# LOGIN MANAGER
# -----------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# -----------------------------
# BANCO + ADMIN PADRÃO
# -----------------------------
with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@email.com").first()
    if not admin:
        admin = User(
            nome="Administrador",
            email="admin@email.com",
            password=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()


# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def index():
    questoes = Question.query.all()
    return render_template("index.html", questoes=questoes)


# -----------------------------
# QUIZ
# -----------------------------
@app.route("/quiz/<int:id>", methods=["GET", "POST"])
def quiz(id):
    questao = Question.query.get_or_404(id)

    if request.method == "POST":
        resposta = request.form.get("resposta")
        correta = resposta == questao.correta

        return render_template(
            "resultado.html",
            correta=correta,
            correta_real=questao.correta
        )

    return render_template("quiz.html", questao=questao)


# -----------------------------
# LOGIN ADMIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.is_admin and check_password_hash(user.password, senha):
            login_user(user)
            return redirect(url_for("admin"))

        flash("Email ou senha inválidos")

    return render_template("login.html")


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# -----------------------------
# ADMIN
# -----------------------------
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    if request.method == "POST":
        correta = request.form["correta"].upper()

        if correta not in ["A", "B", "C", "D"]:
            flash("A resposta correta deve ser A, B, C ou D")
            return redirect(url_for("admin"))

        q = Question(
            pergunta=request.form["pergunta"],
            opcao_a=request.form["a"],
            opcao_b=request.form["b"],
            opcao_c=request.form["c"],
            opcao_d=request.form["d"],
            correta=correta
        )
        db.session.add(q)
        db.session.commit()

    questoes = Question.query.all()
    return render_template("admin.html", questoes=questoes)


# -----------------------------
# DELETE QUESTÃO
# -----------------------------
@app.route("/admin/delete/<int:id>")
@login_required
def delete(id):
    if not current_user.is_admin:
        return redirect(url_for("index"))

    q = Question.query.get_or_404(id)
    db.session.delete(q)
    db.session.commit()

    return redirect(url_for("admin"))


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
