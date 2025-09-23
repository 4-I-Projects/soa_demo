from zeep import Client

client = Client(wsdl="service.wsdl")
response = client.service.sayHello("Huy")
print("Response:", response)
