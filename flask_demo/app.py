# flask se encarga de levantar el servidor Web
from flask import Flask, request, render_template, redirect
# neo4j necesario para porner usar el motor de base de datos
from neo4j import GraphDatabase

# Se inicia seccición ingresando la credenciales, y la dirección.
driver = GraphDatabase.driver(
    uri="bolt://localhost:7687", auth=("neo4j", "1234"))
session = driver.session()

# creamos una instancia para trabajar con Flask
app = Flask(__name__)

# Indicamos que la url "/graph" ejecute la función "creategrpah()"
# Tambien indicamos que tipo de metodos va usar nuetro ruta "/graph". En este caos "GET", "POST"


@app.route("/graph", methods=["GET", "POST"])
def creategrpah():
    if request.method == "POST":
        if request.form["submit"] == "find_graph":

            query = """
        MATCH(a:Student)
        return a.name as name ,a.city as city
        """
            results = session.run(query)
            graphs = []
            for result in results:
                dc = {}
                name = result["name"]
                city = result["city"]
                dc.update({"Name": name, "City": city})
                graphs.append(dc)

            print(graphs)
            return render_template("results.html", list=graphs)

        elif request.form["submit"] == "find_property":
            name = request.form["name"]
            query = """
        MATCH(a:Student{name:$name})
        return a.name as name ,a.city as city
        """
            parameter = {"name": name}
            results = session.run(query, parameter)
            for result in results:
                name = result["name"]
                city = result["city"]

            return (f"{name} vive en {city}")

        elif request.form["submit"] == "find_friends":
            name_requested = request.form["friends"]
            query = """
                    match(a:Student{name:$name})
                    with [(a)--(b)|b.name]as names
                    unwind names as name
                    return name
                     """
            parameter = {"name": name_requested}
            results = session.run(query, parameter)
            friends = []
            for result in results:
                name = result["name"]
                friends.append(name)

            if(len(friends) > 0):
                return render_template("friends.html", list=friends, name=name_requested)
            else:
                return("No tiene amigos pipipi :c")

    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(port=5000)
