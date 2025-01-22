from flask import Flask, render_template, request, url_for, flash
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def validate_form(data):
    errors = []
    if len(data.get('first_name', '')) < 3:
        errors.append("Имя должно содержать не менее 3 символов.")
    if len(data.get('last_name', '')) < 3:
        errors.append("Фамилия должна содержать не менее 3 символов.")
    if 'birth_date' in data:
        birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d')
        age = (datetime.now() - birth_date).days // 365
        if age < 18:
            errors.append("Возраст должен быть старше 18 лет.")
    return errors


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        hobbies = request.form['hobbies']
        avatar = request.files['avatar']

        # Валидация
        errors = validate_form(request.form)
        if 'avatar' not in request.files or avatar.filename == '':
            errors.append("Необходимо загрузить аватар.")

        # Вывод ошибок
        if errors:
            for error in errors:
                flash(error)
            return render_template('register.html')

        # Сохранение аватара
        filename = secure_filename(avatar.filename)
        avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        avatar.save(avatar_path)

        return render_template('account.html',
                               first_name=first_name,
                               last_name=last_name,
                               birth_date=birth_date,
                               hobbies=hobbies,
                               avatar_url=url_for('static', filename=f'uploads/{filename}')
                               )

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)