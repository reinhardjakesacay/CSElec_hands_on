from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rejaas070300'
app.config['MYSQL_DB'] = 'hrm_project'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hrm_project.institutions")
    institutions = cur.fetchall()
    cur.close()

    return render_template('index.html', institutions=institutions)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        institution_name = request.form['institution_name']
        cur.execute("INSERT INTO institutions (institution_name) VALUES (%s)", (institution_name))
        mysql.connection.commit()
        cur.close()

        return render_template('institution_edit.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        institution_name = request.form['institution_name']
        cur.execute("UPDATE institutions SET institution_name=%s WHERE id=%s", (institution_name, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM institutions WHERE id = %s", (id,))
        institutions = cur.fetchone()
        cur.close()

        return render_template('institution_edit.html', institutions=institutions)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM institutions WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)