from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

todoList = [
    {'id': 1, 'description': 'SS1 Assignment 1', 'status': 'Done'},
    {'id': 2, 'description': 'SS1 Assignment 2', 'status': 'Doing'},
    {'id': 3, 'description': 'SS1 Final', 'status': 'Doing'}
]

@app.route('/')
def index():
    return render_template('index.html', todoList=todoList)
@app.route('/templates/styles.css')
def serve_css():
    return send_from_directory('templates', 'styles.css')

@app.route('/add', methods=['POST'])
def add_item():
    des = request.form['itemDescription']
    newId = len(todoList) + 1
    newItem = {'id': newId, 'description': des, 'status': 'Doing'}
    todoList.insert(0, newItem)
    return redirect(url_for('index'))

@app.route('/update/<int:itemId>', methods=['POST'])
def update_item(itemId):
    des = request.form['itemDescription']
    done = 'done' in request.form

    newStatus = 'Done' if done else 'Doing'

    for item in todoList:
        if item['id'] == itemId:
            item['description'] = des
            item['status'] = newStatus
            break

    return redirect(url_for('index'))

@app.route('/delete/<int:itemId>')
def delete_item(itemId):
    global todoList
    todoList = [item for item in todoList if item['id'] != itemId]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)