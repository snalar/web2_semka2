from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Путь к файлу для хранения комментариев
COMMENTS_FILE = 'comments.txt'

# Функция для чтения комментариев из файла
def read_comments_from_file():
    comments = []
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                name, comment = line.strip().split('|', 1)
                comments.append({'name': name, 'comment': comment})
    return comments

# Функция для записи комментария в файл
def write_comment_to_file(name, comment):
    with open(COMMENTS_FILE, 'a', encoding='utf-8') as file:
        file.write(f"{name}|{comment}\n")

@app.route('/')
def main():
    # Читаем комментарии из файла при загрузке страницы
    comments = read_comments_from_file()
    return render_template('main.html', comments=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    name = request.form.get('name')
    comment = request.form.get('comment')
    if name and comment:
        # Сохраняем комментарий в файл
        write_comment_to_file(name, comment)
    return jsonify({'status': 'success', 'comments': read_comments_from_file()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)