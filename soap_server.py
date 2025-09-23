from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

# Định nghĩa hàm SOAP
def say_hello(name):
    return {"message": f"Hello, {name}!"}

# Tạo dispatcher
dispatcher = SoapDispatcher(
    'my_dispatcher',
    location="http://127.0.0.1:8000/",
    action='http://127.0.0.1:8000/',  # SOAPAction
    namespace="http://example.com/soap/",
    prefix="ns0",
    documentation="Simple SOAP demo",
    trace=True,
    ns=True
)

# Đăng ký hàm sayHello
dispatcher.register_function(
    'sayHello',
    say_hello,
    returns={'message': str},
    args={'name': str}
)

# Tạo HTTP Server
class SOAPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.dispatcher = dispatcher  # Gán dispatcher vào serverS

print("SOAP server running at http://127.0.0.1:8000/?wsdl")
httpd = SOAPServer(("127.0.0.1", 8000), SOAPHandler)
httpd.serve_forever()
# Chạy server