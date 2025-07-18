from flask import Flask
from routes.web_routes import web
from tcp_server import start_socket_server
import threading

app = Flask(
    __name__,
    static_folder="../web/static",
    template_folder="../web/template"
)

app.register_blueprint(web)

if __name__ == "__main__":
    threading.Thread(target=start_socket_server, daemon=True).start()
    app.run(debug=True, port=4444)
