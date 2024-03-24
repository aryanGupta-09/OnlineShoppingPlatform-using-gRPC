import grpc
from concurrent import futures
import market_pb2
import market_pb2_grpc

class MarketServicer(market_pb2_grpc.MarketServicer):
    
    def __init__(self):
        self.sellers = {}
        self.items = {}
        self.raters = {}
        self.wishlists = {}
    
    def NotifyBuyers(self, itemId, action):
        for buyerAddress in self.wishlists.keys():
            if itemId in self.wishlists[buyerAddress]:
                with grpc.insecure_channel(buyerAddress) as channel:
                    
                    stub = market_pb2_grpc.MarketStub(channel)
                    request = market_pb2.NotifyBuyerRequest(
                        item = {
                            "itemId": itemId,
                            "quantity": self.items[itemId]["quantity"],
                            "price": self.items[itemId]["price"]
                        }, action=action)
                    response = stub.NotifyBuyer(request)
                    
                    print(f"Notify buyer status: {response.status}")
    
    def NotifySellers(self, itemId, buyerAddress, action):
        with grpc.insecure_channel(self.items[itemId]["sellerAddress"]) as channel:
            
            stub = market_pb2_grpc.MarketStub(channel)
            request = market_pb2.NotifySellerRequest(
                item = {
                    "itemId": itemId,
                    "quantity": self.items[itemId]["quantity"],
                    "price": self.items[itemId]["price"]
                }, action=action, buyerAddress=buyerAddress)
            response = stub.NotifySeller(request)
            
            print(f"Notify buyer status: {response.status}")

    def RegisterSeller(self, request, context):
        
        sellerAddress = request.sellerAddress
        uuid = request.uuid

        if sellerAddress not in self.sellers:
            self.sellers[uuid] = sellerAddress
            print(f"Seller join request from {sellerAddress}, uuid = {uuid}")
            return market_pb2.RegisterSellerResponse(status="SUCCESS")
        
        else:
            print("Failed: Seller with the same address already registered")
            return market_pb2.RegisterSellerResponse(status="FAIL")

    def SellItem(self, request, context):

        itemId = len(self.items) + 1
        itemName = request.itemName
        category = request.category
        quantity = request.quantity
        description = request.description
        sellerAddress = request.sellerAddress
        price = request.price
        uuid = request.uuid

        # authenticate seller
        if uuid in self.sellers.keys() and self.sellers[uuid] == sellerAddress:
            self.items[itemId] = {
                "itemName": itemName,
                "category": category,
                "quantity": quantity,
                "description": description,
                "sellerAddress": sellerAddress,
                "price":price,
                "uuid": uuid,
                "rating": 0.0
            }

            print(f"Sell Item request from {sellerAddress}")
            return market_pb2.SellItemResponse(status="SUCCESS", itemId=itemId)
        
        else:
            print("Failed: Seller authentication failed")
            return market_pb2.SellItemResponse(status="FAIL")

    def UpdateItem(self, request, context):
        itemId = request.itemId
        newPrice = request.newPrice
        newQuantity = request.newQuantity
        sellerAddress = request.sellerAddress
        uuid = request.uuid

        # check if the item exists and the seller is authenticated
        if itemId in self.items.keys() and self.items[itemId]["uuid"] == uuid and self.items[itemId]["sellerAddress"] == sellerAddress:
            self.items[itemId]["price"] = newPrice
            self.items[itemId]["quantity"] = newQuantity

            print(f"Update Item {itemId} request from {sellerAddress}")
            action = "update"
            self.NotifyBuyers(itemId,action)
            return market_pb2.UpdateItemResponse(status="SUCCESS")
        
        else:
            print("Failed: Item update failed, authentication or item not found")
            return market_pb2.UpdateItemResponse(status="FAIL")

    def DeleteItem(self, request, context):
        itemId = request.itemId
        sellerAddress = request.sellerAddress
        uuid = request.uuid

        # check if the item exists and the seller is authenticated
        if itemId in self.items.keys() and self.items[itemId]["uuid"] == uuid and self.items[itemId]["sellerAddress"] == sellerAddress:
            self.items.pop(itemId)

            print(f"Delete Item {itemId} request from {sellerAddress}")
            return market_pb2.DeleteItemResponse(status="SUCCESS")
        
        else:
            print("Failed: Item deletion failed, authentication or item not found")
            return market_pb2.DeleteItemResponse(status="FAIL")

    def DisplaySellerItems(self, request, context):
        sellerAddress = request.sellerAddress
        uuid = request.uuid

        # authenticate seller
        if uuid in self.sellers.keys() and self.sellers[uuid] == sellerAddress:
            sellerItems = []

            for itemId, item in self.items.items():
                
                #check if the item belongs to the authenticated seller
                if item["uuid"] == uuid and item["sellerAddress"] == sellerAddress:
                    
                    #create item details
                    itemDetails = market_pb2.DisplaySellerItemsResponse.ItemDetails(
                        itemId = itemId,
                        itemName=item["itemName"],
                        category=item["category"],
                        quantity=item["quantity"],
                        description=item["description"],
                        sellerAddress=item["sellerAddress"],
                        price=item["price"],
                        uuid=item["uuid"],
                        rating=item["rating"]
                    )
                    sellerItems.append(itemDetails)

            print(f"Display Items request from {sellerAddress}")
            return market_pb2.DisplaySellerItemsResponse(sellerItems=sellerItems)
        
        else:
            print("Failed: Display items failed, authentication failed")
            return market_pb2.DisplaySellerItemsResponse()
    

    def SearchItem(self, request, context):
        itemName = request.itemName
        category = request.category
        matchedItems = []

        for itemId, item in self.items.items():
            
            #check if the item name and category matches the search criteria
            if (not itemName or itemName.lower() in item["itemName"].lower()) and (not category or category == "ANY" or category == item["category"]):
                itemDetails = market_pb2.SearchItemResponse.ItemDetails(
                    itemId=itemId,
                    price=item["price"],
                    itemName=item["itemName"],
                    category=item["category"],
                    description=item["description"],
                    quantity=item["quantity"],
                    rating=item["rating"],
                    sellerAddress=item["sellerAddress"]
                )
                matchedItems.append(itemDetails)

        print(f"Search request for Item name: {itemName}, Category: {category}")
        return market_pb2.SearchItemResponse(searchResults=matchedItems)

    def BuyItem(self, request, context):
        itemId = request.itemId
        quantity = request.quantity
        buyerAddress = request.buyerAddress

        if itemId in self.items:
            item = self.items[itemId]

            if quantity <= item["quantity"]:
                item["quantity"] -= quantity
                print(f"Buy request {quantity} of item {itemId} from {buyerAddress}")
                action = "buy"
                self.NotifySellers(itemId, buyerAddress, action)
                return market_pb2.BuyItemResponse(status="SUCCESS")
            
            else:
                print(f"Failed: Not enough stock available for item {itemId}")
                return market_pb2.BuyItemResponse(status="FAIL")
            
        else:
            print(f"Failed: Item with ID {itemId} not found")
            return market_pb2.BuyItemResponse(status="FAIL")

    def AddToWishList(self, request, context):
        itemId = request.itemId
        buyerAddress = request.buyerAddress

        if itemId in self.items:
            print(f"Wishlist request of item {itemId} from {buyerAddress}")
            if buyerAddress in self.wishlists:
                self.wishlists[buyerAddress].append(itemId)
            else:
                self.wishlists[buyerAddress] = [itemId]

            return market_pb2.AddToWishListResponse(status="SUCCESS")
        
        else:
            print(f"Failed: Item with ID {itemId} not found")
            return market_pb2.AddToWishListResponse(status="FAIL")
    
    def ShowWishList(self, request, context):
        buyerAddress = request.buyerAddress
        print(f"Show wishlist request from {buyerAddress}")
        wishList = []

        if buyerAddress in self.wishlists:
            for itemId in self.wishlists[buyerAddress]:
                item = self.items[itemId]
                itemDetails = market_pb2.ShowWishListResponse.ItemDetails(
                    itemId=itemId,
                    price=item["price"],
                    itemName=item["itemName"],
                    category=item["category"],
                    description=item["description"],
                    quantity=item["quantity"],
                    rating=item["rating"],
                    sellerAddress=item["sellerAddress"]
                )
                wishList.append(itemDetails)

        return market_pb2.ShowWishListResponse(wishList=wishList)

    def RateItem(self, request, context):
        itemId = request.itemId
        buyerAddress = request.buyerAddress
        rating = request.rating

        if itemId in self.items:
            item = self.items[itemId]

            if 1 <= rating <= 5:
                if itemId not in self.raters:
                    self.raters[itemId]=1
                else:
                    self.raters[itemId]+=1

                item["rating"] = (item["rating"] + rating) / self.raters[itemId]
                print(f"{buyerAddress} rated item {itemId} with {rating} stars")

                return market_pb2.RateItemResponse(status="SUCCESS")
            
            else:
                print("Failed: Rating must be between 1 and 5")
                return market_pb2.RateItemResponse(status="FAIL")
            
        else:
            print(f"Failed: Item with ID {itemId} not found")
            return market_pb2.RateItemResponse(status="FAIL")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    market_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port("[::]:50051") # replace with address of current machine
    server.start()
    print("Market server is running...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
