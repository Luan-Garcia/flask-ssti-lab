from flask import Flask, request, render_template_string, render_template

app = Flask(__name__)

@app.route('/safe')
def safe():
    name = request.args.get('name', 'Guest')
    return render_template('safe.html', user_name=name)

@app.route ('/vuln')
def vuln(): 
    name = request.args.get('name', 'Guest')

    html = f"<h1>Bem-vindo, {name}!</h1>"

    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
