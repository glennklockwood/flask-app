import sqlite3
import flask
import werkzeug.exceptions

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

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
        werkzeug.exceptions.abort(404)
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

@app.route("/posts/<int:post_id>/edit", methods=("GET", "POST"))
def edit_post(post_id):
    post = get_post(post_id)

    if flask.request.method == "POST":
        title = flask.request.form["title"]
        content = flask.request.form["content"]
        if not title:
            flask.flash("Title is required!")
        else:
            conn = get_db_conn()
            conn.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?",
                (title, content, post_id))
            conn.commit()
            conn.close()
            return flask.redirect(flask.url_for("show_index"))

    return flask.render_template("edit.html", post=post)

@app.route("/posts/<int:post_id>/delete", methods=("POST",))
def delete_post(post_id):
    post = get_post(post_id)
    conn = get_db_conn()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    flask.flash("%s was successfully deleted." % post['title'])
    return flask.redirect(flask.url_for("show_index"))

@app.route("/create", methods=("GET", "POST"))
def create_post():
    if flask.request.method == "POST":
        title = flask.request.form['title']
        content = flask.request.form['content']

        if not title:
            flask.flash("Title is required!")
        else:
            conn = get_db_conn()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
                (title, content))
            conn.commit()
            conn.close()
            return flask.redirect(flask.url_for("show_index"))

    return flask.render_template('create.html')
