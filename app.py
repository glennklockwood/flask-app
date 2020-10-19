import sqlite3
import flask
import werkzeug

app = flask.Flask(__name__)

def get_db_conn():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_conn()
    post = conn.execute("SELECT * FROM posts WHERE id = ?",
        (post_id,)).fetchone()
    conn.close()
    if post is None:
        werkzeug.abort(404)
    return post

@app.route("/")
def show_index():
    conn = get_db_conn()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()

    return flask.render_template('index.html', posts=posts)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = get_post(post_id)
    return flask.render_template("post.html", post=post)
