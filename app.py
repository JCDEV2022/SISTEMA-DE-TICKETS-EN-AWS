from flask import Flask, render_template, request, redirect
import os
import pymysql

app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=int(os.environ.get("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )

lista_tickets = [
    {
        "id": 1,
        "titulo": "equipo no enciende",
        "tecnico": "juan",
        "estado": "pendiente"
    },
    {
        "id": 2,
        "titulo": "problema de red",
        "tecnico": "carlos",
        "estado": "resuelto"
    }
]
siguiente_id = 3

@app.route("/")
def home():

    return render_template("index.html")


@app.route("/crear-ticket", methods=["GET", "POST"])
def crear_ticket():

    global siguiente_id

    if request.method == "POST":

        titulo = request.form["titulo"]
        tecnico = request.form["tecnico"]
        estado = request.form["estado"]

        

        if not titulo and not tecnico:
          mensaje = "El título y el técnico son obligatorios."
          return render_template("crear_ticket.html",mensaje = mensaje)
        
        elif not titulo:
           mensaje = "El título es obligatorio."
           return render_template("crear_ticket.html",mensaje = mensaje)

        elif not tecnico:
         mensaje = "El técnico es obligatorio."
         return render_template("crear_ticket.html",mensaje = mensaje)

        

        nuevo_ticket = {
    "id": siguiente_id,
    "titulo": titulo,
    "tecnico": tecnico,
    "estado": estado
}

        lista_tickets.append(nuevo_ticket)
        siguiente_id += 1

        return redirect("/tickets")

    return render_template("crear_ticket.html")


@app.route("/tickets")
def tickets():

    conexion = obtener_conexion()

    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM tickets ORDER BY id")
            tickets = cursor.fetchall()

        return render_template("tickets.html", tickets=tickets)

    finally:
        conexion.close()

@app.route("/editar-ticket/<int:id>", methods=["GET", "POST"])
def editar_ticket(id):

    ticket = next((t for t in lista_tickets if t["id"] == id), None)

    if ticket is None:
        return "ticket no encontrado", 404

    if request.method == "POST":

        titulo = request.form["titulo"]
        tecnico = request.form["tecnico"]
        estado = request.form["estado"]

        if not titulo and not tecnico:
            mensaje = "El título y el técnico son obligatorios."
            return render_template(
                "editar_ticket.html",
                ticket=ticket,
                mensaje=mensaje
            )

        elif not titulo:
            mensaje = "El título es obligatorio."
            return render_template(
                "editar_ticket.html",
                ticket=ticket,
                mensaje=mensaje
            )

        elif not tecnico:
            mensaje = "El técnico es obligatorio."
            return render_template(
                "editar_ticket.html",
                ticket=ticket,
                mensaje=mensaje
            )

        ticket["titulo"] = titulo
        ticket["tecnico"] = tecnico
        ticket["estado"] = estado

        return redirect("/tickets")

    return render_template("editar_ticket.html", ticket=ticket)

@app.route("/eliminar-ticket/<int:id>", methods =["POST"])
def eliminar_ticket(id):

    ticket = next((t for t in lista_tickets if t["id"]== id),None)

    if ticket is None:
        return "ticket no encontrado", 404
    
    lista_tickets.remove(ticket)

    return redirect("/tickets")

    
if __name__ == "__main__":
    app.run(debug=True)