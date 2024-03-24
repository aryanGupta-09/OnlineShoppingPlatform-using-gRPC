import grpc
import market_pb2
import market_pb2_grpc
import threading
from concurrent import futures
import uuid

def register_seller(stub, sellerAddress, uuid):
    request = market_pb2.RegisterSellerRequest(sellerAddress=sellerAddress, uuid=uuid)
    response = stub.RegisterSeller(request)
    print(f"Register seller status: {response.status}")

def sell_item(stub, itemName, category, quantity, description, sellerAddress, price, uuid):
    request = market_pb2.SellItemRequest(
        itemName=itemName,
        category=category,
        quantity=quantity,
        description=description,
        sellerAddress=sellerAddress,
        price=price,
        uuid=uuid
    )
    response = stub.SellItem(request)
    print(f"Sell item status: {response.status}, Item ID: {response.itemId}")

def update_item(stub, itemId, newPrice, newQuantity, sellerAddress, uuid):
    request = market_pb2.UpdateItemRequest(
        itemId=itemId,
        newPrice=newPrice,
        newQuantity=newQuantity,
        sellerAddress=sellerAddress,
        uuid=uuid
    )
    response = stub.UpdateItem(request)
    print(f"Update item status: {response.status}")

def delete_item(stub, itemId, sellerAddress, uuid):
    request = market_pb2.DeleteItemRequest(itemId=itemId, sellerAddress=sellerAddress, uuid=uuid)
    response = stub.DeleteItem(request)
    print(f"Delete item status: {response.status}")

def display_seller_items(stub, sellerAddress, uuid):
    request = market_pb2.DisplaySellerItemsRequest(sellerAddress=sellerAddress, uuid=uuid)
    response = stub.DisplaySellerItems(request)
    
    for item in response.sellerItems:
        print(f"Item ID: {item.itemId}, Item Name: {item.itemName}, Category: {item.category}, Quantity: {item.quantity}, Description: {item.description}, Price: {item.price}, Rating: {item.rating}")


class SellerServer(market_pb2_grpc.MarketServicer):
    
    def NotifySeller(self, request, context):
        item = request.item
        if request.action == "buy":
            print(f"\nItem {item.itemId} has been bought by {request.buyerAddress}, remaining Quantity: {item.quantity}")
        return market_pb2.NotifySellerResponse(status="Notification received")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServicer_to_server(SellerServer(), server)
    server.add_insecure_port('[::]:50052') # replace with address of current machine
    server.start()
    server.wait_for_termination()

def main():
    serverThread = threading.Thread(target=serve)
    serverThread.start()
    serverAddress= "localhost:50051" # replace with market's address
    sellerAddress= "localhost:50052" # replace with address of current machine
    seller_uuid= str(uuid.uuid1())

    with grpc.insecure_channel(serverAddress) as channel:
        stub = market_pb2_grpc.MarketStub(channel)

        while True:
            print("Choose an option:")
            print("1. Register Seller")
            print("2. Sell Item")
            print("3. Update Item")
            print("4. Delete Item")
            print("5. Display Seller Items")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                register_seller(stub, sellerAddress, seller_uuid)
           
            elif choice == '2':
                itemName = input("Enter item name: ")
                category = input("Enter category (ELECTRONICS, FASHION, ANY): ")
                quantity = int(input("Enter quantity: "))
                description = input("Enter item description: ")
                price = float(input("Enter price: "))
                sell_item(stub, itemName, category, quantity, description, sellerAddress, price, seller_uuid)
           
            elif choice == '3':
                itemId = int(input("Enter item ID to update: "))
                newPrice = float(input("Enter new price: "))
                newQuantity = int(input("Enter new quantity: "))
                update_item(stub, itemId, newPrice, newQuantity, sellerAddress, seller_uuid)

            elif choice == '4':
                itemId = int(input("Enter item ID to delete: "))
                delete_item(stub, itemId, sellerAddress, seller_uuid)

            elif choice == '5':
                display_seller_items(stub, sellerAddress, seller_uuid)

            elif choice == '6':
                break
            
            else:
                print("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    main()
