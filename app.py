from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route("/")
def home():
    todos = Todo.query.all()
    return render_template("index.html",todo_list = todos)

@app.route("/reload",methods=['POST'])
def reload():
    todos = Todo.query.all()
    return jsonify({'data': render_template("content.html",todo_list=todos)})

@app.route("/add",methods=['POST'])
def add():
    title = request.form["data"]
    todo = Todo(title=title,complete=False)
    db.session.add(todo)
    db.session.commit()
    todos = Todo.query.all()
    print(todos)
    return jsonify({'data': render_template("content.html",todo_list=todos)})

@app.route("/update",methods=['POST'])
def update():
    id = request.form["data"]
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    todos = Todo.query.all()
    print(todos)
    return jsonify({'data': render_template("content.html",todo_list=todos)})

@app.route("/delete",methods=['POST'])
def delete():
    id = request.form["data"]
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    todos = Todo.query.all()
    print(todos)
    return jsonify({'data': render_template("content.html",todo_list=todos)})


if __name__ == "__main__":
    db.create_all()
    app.run()
