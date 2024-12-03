from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todoList = [
    {'id': 1, 'description': 'SS1 Assignment 1', 'status': 'Done'},
    {'id': 2, 'description': 'SS1 Assignment 2', 'status': 'Doing'},
    {'id': 3, 'description': 'SS1 Final', 'status': 'Doing'}
]

@app.route('/')
def index():
    return render_template('index.html', todoList=todoList)

@app.route('/add', methods=['POST'])
def add_item():
    description = request.form['itemDescription']
    new_id = len(todoList) + 1
    new_item = {'id': new_id, 'description': description, 'status': 'Doing'}
    todoList.insert(0, new_item)
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    description = request.form['itemDescription']
    done = 'done' in request.form

    new_status = 'Done' if done else 'Doing'

    for item in todoList:
        if item['id'] == item_id:
            item['description'] = description
            item['status'] = new_status
            break

    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    global todoList
    todoList = [item for item in todoList if item['id'] != item_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)