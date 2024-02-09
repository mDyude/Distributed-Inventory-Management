import grpc
import calculator_pb2
import calculator_pb2_grpc

def run(num1, num2):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        response = stub.Add(calculator_pb2.AddRequest(num1=num1, num2=num2))
        print(f"Result: {response.result}")
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        response = stub.AddMult(calculator_pb2.AddMultRequest(num1=num1, num2=num2))
        print(f"Result of Add: {response.num1}") 
        print(f"Result of Mult: {response.num2}") 


if __name__ == '__main__':
    # Get user Input 
    num1 = int(input("Please input num1: "))
    num2 = int(input("Please input num2: "))
    run(num1, num2)

