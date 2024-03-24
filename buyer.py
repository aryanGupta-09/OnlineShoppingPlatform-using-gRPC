import grpc
from concurrent import futures
import market_pb2
import market_pb2_grpc
import threading

def search_item(stub, itemName, category):
    request = market_pb2.SearchItemRequest(itemName=itemName, category=category)
    response = stub.SearchItem(request)
    for item in response.searchResults:
        print(f"Item ID: {item.itemId}, Price: {item.price}, Name: {item.itemName}, Category: {item.category}, Quantity: {item.quantity}, Rating: {item.rating}, Seller: {item.sellerAddress}")

def buy_item(stub, itemId, quantity, buyerAddress):
    request = market_pb2.BuyItemRequest(itemId=itemId, quantity=quantity, buyerAddress=buyerAddress)
    response = stub.BuyItem(request)
    print(f"Buy item status: {response.status}")

def add_to_wishlist(stub, itemId, buyerAddress):
    request = market_pb2.AddToWishListRequest(itemId=itemId, buyerAddress=buyerAddress)
    response = stub.AddToWishList(request)
    print(f"Add to wishlist status: {response.status}")

def show_wishlist(stub, buyerAddress):
    request = market_pb2.ShowWishListRequest(buyerAddress=buyerAddress)
    response = stub.ShowWishList(request)

    if len(response.wishList) == 0:
        print("Wishlist is empty")
    else:
        for item in response.wishList:
            print(f"Item ID: {item.itemId}, Price: {item.price}, Name: {item.itemName}, Category: {item.category}, Quantity: {item.quantity}, Rating: {item.rating}, Seller: {item.sellerAddress}")

def rate_item(stub, itemId, buyerAddress, rating):
    request = market_pb2.RateItemRequest(itemId=itemId, buyerAddress=buyerAddress, rating=rating)
    response = stub.RateItem(request)
    print(f"Rate item status: {response.status}")


class BuyerServer(market_pb2_grpc.MarketServicer):
    
    def NotifyBuyer(self, request, context):
        item = request.item
        if request.action == "update":
            print(f"\nItem {item.itemId} has been updated\nNew Price: {item.price}\nNew Quantity: {item.quantity}")
        return market_pb2.NotifyBuyerResponse(status="Notification received")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServicer_to_server(BuyerServer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

def main():
    serverThread = threading.Thread(target=serve)
    serverThread.start()
    serverAddress = "localhost:50051" # replace with market's address
    buyerAddress = "localhost:50053" # replace with address of current machine

    with grpc.insecure_channel(serverAddress) as channel:
        stub = market_pb2_grpc.MarketStub(channel)

        while True:
            print("Choose an option:")
            print("1. Search Item")
            print("2. Buy Item")
            print("3. Add to Wishlist")
            print("4. Rate Item")
            print("5. Show Wishlist")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                itemName = input("Enter item name (leave blank for all items): ")
                category = input("Enter category (ELECTRONICS, FASHION, OTHERS, ANY): ")
                search_item(stub, itemName, category)

            elif choice == '2':
                itemId = int(input("Enter item ID to buy: "))
                quantity = int(input("Enter quantity to buy: "))
                buy_item(stub, itemId, quantity, buyerAddress)

            elif choice == '3':
                itemId = int(input("Enter item ID to add to wishlist: "))
                add_to_wishlist(stub, itemId, buyerAddress)

            elif choice == '4':
                itemId = int(input("Enter item ID to rate: "))
                rating = int(input("Enter rating (1 to 5): "))
                rate_item(stub, itemId, buyerAddress, rating)

            elif choice == '5':
                show_wishlist(stub, buyerAddress)

            elif choice == '6':
                break
            
            else:
                print("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    main()
