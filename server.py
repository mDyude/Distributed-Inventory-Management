import redis
import grpc
import inventory_pb2
import inventory_pb2_grpc
from concurrent import futures
import time
import random
import redis
from threading import Lock

# lock the server to avoid having multiple clients accessing the server at the same time
serverLock = Lock()

class InventoryServiceServicer(inventory_pb2_grpc.InventoryServiceServicer):
    # add a product to the database
    def AddProduct(self, request, context):
        with serverLock:
            # assign a unique id for the product
            product_id = random.randrange(1, 10000)
            # eliminate haivng duplicate ids
            while product_id in dataDict.keys():
                product_id = random.randrange(1, 10000)
            
            try:
                # save the product in the database
                dataDict.hset(product_id, mapping={
                    "name": request.product_name,
                    "quantity": int(request.product_quantity),
                    "price": float(request.product_price)
                })
            
                return inventory_pb2.Status(status="Product added successfully \n")
            
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, "Error: " + str(e))

    # get the product by id
    def GetProductById(self, request, context):
        with serverLock:
            try:
                if not dataDict.exists(request.product_identifier):
                    context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")
                
                # get the product from the database
                product = dataDict.hgetall(request.product_identifier)
                
                # return the product
                return inventory_pb2.Product(
                    product_identifier = int(request.product_identifier),
                    product_name = product["name"],
                    product_quantity = int(product["quantity"]),
                    product_price = float(product["price"])
                )
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, "Error: " + str(e))
        
    # update the product quantity
    def UpdateProductQuantity(self, request, context):
        with serverLock:
            try:
                # check if the product exists
                # if not return a status code
                if not dataDict.exists(request.product_identifier):
                    context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")
                
                # update the product quantity
                dataDict.hset(request.product_identifier, "quantity", request.product_quantity)
                
                # return the updated product
                product = dataDict.hgetall(request.product_identifier)
                return inventory_pb2.Product(
                    product_identifier = int(request.product_identifier),
                    product_name = product["name"],
                    product_quantity = int(product["quantity"]),
                    product_price = float(product["price"])
                )
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, "Error: " + str(e))

    # delete the product from the database
    def DeleteProduct(self, request, context):
        with serverLock:
            try:
                # check if the product exists
                # if not, return a message
                if not dataDict.exists(request.product_identifier):
                    context.abort(grpc.StatusCode.NOT_FOUND, "Product not found")
                
                # delete the product from the database
                dataDict.delete(request.product_identifier)
                
                return inventory_pb2.Status(status="Product deleted successfully")
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, "Error: " + str(e))
    
    # stream all the products from the database
    # for intervals of 0.5 seconds
    def GetAllProducts(self, request, context):
        with serverLock:
            try:
                # get all the products from the database
                products = dataDict.keys()

                # return the products
                for product in products:            
                    yield inventory_pb2.Product(
                        product_identifier = int(product),
                        product_name = dataDict.hget(product, "name"),
                        product_quantity = int(dataDict.hget(product, "quantity")),
                        product_price = float(dataDict.hget(product, "price"))
                    )
                    time.sleep(0.5)
            except Exception as e:
                context.abort(grpc.StatusCode.INTERNAL, "Error: " + str(e))

            
if __name__ == '__main__':
    # ip and port for the server
    SERVER_IP = "localhost"
    SERVER_PORT = 50051

    # default ip and port for redis on my local machine
    REDIS_IP = "localhost"
    REDIS_PORT = 6379
    
    # the data is stored in a redis database as dictionary/hash 
    dataDict = redis.Redis(host=REDIS_IP, port=REDIS_PORT, decode_responses=True)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 1))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServiceServicer(), server)
    server.add_insecure_port(f"{SERVER_IP}:{SERVER_PORT}")
    server.start()
    # server.wait_for_termination()
    
    # prompt the user to quit the server
    action = input("q/Q to quit\n")
    if action == "q" or action == "Q":
        server.stop(0)
