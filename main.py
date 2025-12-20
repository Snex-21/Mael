from handlers.bot import Mael
import handlers.claves.config as cg
import threading
from server.server import run_flask

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    Bot = Mael(api_tg=cg.tg_api, api_hash=cg.api_hash, api_id=cg.api_id)
    Bot.run()