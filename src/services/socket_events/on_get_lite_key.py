from utils.debug import log_func
from utils.crypto_utils.SPX_CriptoLite import get_key_lite
import socketio

def setup_events(sio: socketio.Client) -> None:
    @sio.event
    def get_lite_key(data) -> None:
        public_key = get_key_lite()["publicKey"]
        
        response = {"data": public_key}
        if 'requestId' in data:
            response['requestId'] = data['requestId']
            
        sio.emit("get_pub_lite_key_SIS_return", response)