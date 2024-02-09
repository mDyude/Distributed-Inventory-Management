import grpc
import inventory_pb2
import inventory_pb2_grpc

def addProduct(name, quantity, price):
    try:
        # connect to the server
        with grpc.insecure_channel(f"{SERVER_IP}:{SERVER_PORT}") as channel:
            stub = inventory_pb2_grpc.InventoryServiceStub(channel)
            
            # call the AddProduct method on the server side
            response = stub.AddProduct(inventory_pb2.Product(
                product_name=name,
                product_quantity=quantity,
                product_price=price
            ))
            
            print(f"Operation Result: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
        
# id is the product identifier used to search for the product
# print the product info
def getProduct(id):
    try:
        with grpc.insecure_channel(f"{SERVER_IP}:{SERVER_PORT}") as channel:
            stub = inventory_pb2_grpc.InventoryServiceStub(channel)
            response = stub.GetProductById(inventory_pb2.ProductIdentifier(
                product_identifier = id
            ))
            
            print("\nID: ", response.product_identifier,
                    "\nName: ", response.product_name,
                    "\nQuantity: ", response.product_quantity,
                    "\nPrice: ", response.product_price)
    except Exception as e:
        print(f"Error: {e}")

# send request to update the product quantity
# print the updated product info
def updateProductQ(id, new_quantity):
    try:
        with grpc.insecure_channel(f"{SERVER_IP}:{SERVER_PORT}") as channel:
            stub = inventory_pb2_grpc.InventoryServiceStub(channel)
            
            response = stub.UpdateProductQuantity(inventory_pb2.Quantity(
                product_identifier = id,
                product_quantity = new_quantity
            ))
            
            print("\nUpdated Product Info: \nID: ", response.product_identifier,
                    "\nName: ", response.product_name,
                    "\nQuantity: ", response.product_quantity,
                    "\nPrice: ", response.product_price)
            
    except Exception as e:
        print(f"Error: {e}")

# send request to delete the product from the server
# print the result
def deleteProduct(id):
    try:
        with grpc.insecure_channel(f"{SERVER_IP}:{SERVER_PORT}") as channel:
            stub = inventory_pb2_grpc.InventoryServiceStub(channel)
            
            response = stub.DeleteProduct(inventory_pb2.ProductIdentifier(
                product_identifier = id
            ))
            
            print(f"Operation Result: {response.status}")
            
    except Exception as e:      
        print(f"Error: {e}")

# send request and get all the products from the server
def getAllProducts():
    try:
        with grpc.insecure_channel(f"{SERVER_IP}:{SERVER_PORT}") as channel:
            stub = inventory_pb2_grpc.InventoryServiceStub(channel)
            response_iterator = stub.GetAllProducts(inventory_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
            # iterate through the response
            for product in response_iterator:
                print("\nID:", product.product_identifier, 
                    "\nName:", product.product_name, 
                    "\nQuantity:", product.product_quantity,
                    "\nPrice:", product.product_price)
    except Exception as e:
        print(f"Error: {e}")
        
def getNumInput(inNum):
    while True:
        user_input = input(inNum)
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == '__main__':
    SERVER_IP = "localhost"
    SERVER_PORT = 50051
    
    while True:
        # prompt the user for the action
        action = input("\n What do you want to do? \n \
            a/A: Add Product \n \
            g/G: Get Product by ID \n \
            u/U: Update Product Quantity by ID \n \
            d/D: Delete Product by ID \n \
            f/F: Get all Products (if you don't know the ID, choose this one!) \n \
            q/Q: Quit \n\n")
        
        # switch cases
        match action:
            # quit
            case "q" | "Q":
                break
            
            # add
            case "a" | "A":
                name = input("Enter Product Name: ")
                quantity = int(getNumInput("Enter Product Quantity: "))
                price = getNumInput("Enter Product Price: ")
                addProduct(name, quantity, price)
            
            # get
            case "g" | "G":
                p_id = int(getNumInput("(GET) Enter the Product ID: "))
                getProduct(p_id)
                
            # update
            case "u" | "U":
                p_id = int(getNumInput("(UPDATE) Enter the Product ID: "))
                quantity = int(getNumInput("Enter New Quantity: "))
                updateProductQ(p_id, quantity)
            
            # delete
            case "d" | "D":
                p_id = int(getNumInput("(DELETE) Enter the Product ID: "))
                deleteProduct(p_id)
            
            # fetch (all)
            case "f" | "F":
                getAllProducts()