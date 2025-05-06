import re

import quickfix as fix


class FixServerApp(fix.Application):
    def onCreate(self, session_id):
        print(f"Session created: {session_id}")

    def onLogon(self, session_id):
        print(f"Client logged in: {session_id}")

    def onLogout(self, session_id):
        print(f"Client logged out: {session_id}")

    def fromAdmin(self, message, session_id):
        print(f"Received admin message: {self.readable_string(message)}")

    def toAdmin(self, message, session_id):
        print(f"Sent admin message: {self.readable_string(message)}")

    def fromApp(self, message, session_id):
        print(f"Received application message: {self.readable_string(message)}")

    def toApp(self, message, session_id):
        print(f"Sent application message: {self.readable_string(message)}")

    def readable_string(self, message):
        formatted_message = re.sub(r'(?<!^)(\d+=)', r'|\1', str(message)) + '|'
        return formatted_message

if __name__ == "__main__":
    settings = fix.SessionSettings("utils/fix_server.cfg")
    application = FixServerApp()
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.FileLogFactory(settings)
    
    acceptor = fix.SocketAcceptor(application, store_factory, settings, log_factory)

    print("Starting FIX server...")
    acceptor.start()
    input("Press <ENTER> to quit.\n")
    acceptor.stop()
    print("FIX server stopped.")
