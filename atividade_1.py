from flask import Flask

app = Flask(__name__)

@app.route('/') 
def decorator_explicacao():
    return "É uma funcionalidade que permite modificar ou estender o comportamento de uma função (geralmente rota) mas sem alterar o codigo original"    

if __name__ == '__main__':
    app.run(debug=True) 