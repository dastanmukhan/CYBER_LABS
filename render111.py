from flask import Flask, request, jsonify, send_file, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Создание базы данных и таблицы для SQL-инъекции
def create_db():
    conn = sqlite3.connect('ctf.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, flag TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users (username, password, flag) VALUES ('admin', 'admin!', 'flag{second_flag}')")
    conn.commit()
    conn.close()

# Главная страница
@app.route("/")
def index():
    key = request.args.get("key")  # Теперь ищем параметр "key"

    if key == "flag":
        return redirect(url_for('stage_2'))  # Перенаправление на этап 2
    elif key == "hidden_treasure":
        return redirect(url_for('stage_30'))  # Перенаправление на этап 3
    elif key == "CTF{final_hidden_flag}":
        return "<h1>Поздравляем! 🎉</h1><p>Флаг: CTF{final_hidden_flag}</p>"

    return render_template_string("""
        <h1>Добро пожаловать в CTF!</h1>
        <p></p>
        <p>Например: <code>/?key=?</code></p>
        <!-- Иногда браузер скрывает самое важное... -->



































































        <script src="/static/hint.js"></script>
    """)

# Этап 2: Поиск флага через SQL-инъекцию
@app.route("/stage2")
def stage_2():
    username = request.args.get("username")
    password = request.args.get("password")

    # Уязвимость: Простой запрос без защиты от SQL-инъекций
    conn = sqlite3.connect('ctf.db')
    cursor = conn.cursor()

    # Это уязвимый запрос! Он подвержен SQL-инъекции
    query = f"SELECT flag FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    flag = cursor.fetchone()

    conn.close()

    if flag:
        return render_template_string(f"""
            <h1>Поздравляем!</h1>
            <p>Ты нашел второй флаг: {flag[0]}</p>
            <p>Теперь переходи к <a href="/stage_30">третий этап</a>.</p>
        """)
    else:
        return render_template_string("""
            <h1>Ошибка</h1>
            <p>Неправильное имя пользователя или пароль. Попробуй снова.>>>"!"<<<</p>
            <form action="/stage2" method="GET">
                                      <script src="FlaG{CTF_ASTANA_00x4}"></script>
                <input type="text" name="username" placeholder="Введите имя пользователя">
                <input type="password" name="password" placeholder="Введите пароль">
                <input type="submit" value="Отправить">

































                <script src="https://admin.com/"></script>
            </form>
        """)

# Этап 3: Получение флага через API
@app.route("/stage_30")
def stage_3():
    return render_template_string("""
        <h1>Финальный этап</h1>
        
                                  








































































        <script src="/static/auth.js"></script>
    """)

# Подсказка (скрытый JavaScript)
@app.route("/static/hint.js")
def hint_js():
    return 'var a = "ZmxhZw=="; console.log(atob(a));', 200, {'Content-Type': 'application/javascript'}

# Подсказка для API
@app.route("/static/auth.js")
def auth_js():
    return 'fetch("/secret/api/getflag", { headers: { "X-Secret-Key": "RkxBR19DT0RF" } });', 200, {'Content-Type': 'application/javascript'}

# API для финального флага
@app.route("/secret/api/getflag")
def secret_api():
     if request.headers.get("X-Secret-Key") == "FLAG_C0DE":
       return jsonify({"flag": "CTF{final_hidden_flag}"})
     return jsonify({"error": "Unauthorized access"}), 403

   


# Картинка для второго этапа
@app.route("/static/secret.png")
def secret_png():
    return send_file("secret.png", mimetype="image/png")

if __name__ == "__main__":
    create_db()  # Создаем базу данных для второго этапа
    app.run(debug=True)
