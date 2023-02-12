from flask import Flask
from Fahorro import main
from Tiendaenlinea import main
from Farmaciasanpablo import main
app = Flask(__name__)

@app.route('/')
def hello_world():
	return('Hello World')

@app.route('/fahorro')
def fahorro():
	return main.fahorro()

@app.route('/tiendaenlinea')
def tiendaenlinea():
	return main.tiendaenlinea()

@app.route('/farmaciasanpablo')
def farmaciasanpablo():
	return main.farmaciasanpablo()

if __name__ == '__main__':
    
	app.run(debug=True)
