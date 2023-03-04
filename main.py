from flask import Flask
from Fahorro import main as fr
from Tiendaenlinea import main as tl
from Farmaciasanpablo import main as fp
app = Flask(__name__)

@app.route('/')
def hello_world():
	return('Hello World')

@app.route('/fahorro')
def fahorro():
	return fr.fahorro()

@app.route('/tiendaenlinea')
def tiendaenlinea():
	return tl.tiendaenlinea()

@app.route('/farmaciasanpablo')
def farmaciasanpablo():
	return fp.farmaciasanpablo()

if __name__ == '__main__':   
	app.run(debug=True)
