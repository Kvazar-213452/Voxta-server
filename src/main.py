import threading
from flask import Flask
from routes.web_routes import web
from services.client_server import connect_to_socket_server
from utils.crypto_utils.SPX_CriptoLite import init_key_lite

app = Flask(
    __name__,
    static_folder="../web/static",
    template_folder="../web/template"
)

app.register_blueprint(web)
init_key_lite()

def start_socket_client():
    try:
        connect_to_socket_server()
    except Exception as e:
        print(f"[Socket client error]: {e}")

if __name__ == "__main__":
    socket_thread = threading.Thread(target=start_socket_client, daemon=True)
    socket_thread.start()
    
    try:
        app.run(debug=True, port=4444, use_reloader=False)
    except KeyboardInterrupt:
        pass
