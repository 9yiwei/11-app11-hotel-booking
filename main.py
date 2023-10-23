import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_card = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book the hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id]["available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class ReservationTicket:
    def __init__(self, costumer_name, hotel_object):
        self.costumer_name = costumer_name
        self.hotel = hotel_object

    def generation(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.costumer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class SpaTicket:
    def __init__(self, costumer_name, hotel_object):
        self.costumer_name = costumer_name
        self.hotel = hotel_object

    def generation(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are you SOA booking data:
        Name: {self.costumer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, numbers):
        self.numbers = numbers

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.numbers, "expiration": expiration, "cvc": cvc, "holder": holder}
        if card_data in df_card:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.numbers, "password"].squeeze()
        print(given_password)
        print(password)
        if password == given_password:
            return True
        else:
            return False


print(df)

hotel_ID = input("Enter the id of hotel: ")
hotel = SpaHotel(hotel_ID)
if hotel.available():
    credit_card = SecureCreditCard(numbers="1234")
    if credit_card.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(name, hotel)
            print(reservation_ticket.generation())
            spa = input("Do you want to book a spa package?: ")
            if spa == "yes":
                hotel.book_spa_package()
                spa_ticket = SpaTicket(name, hotel)
                print(spa_ticket.generation())
            else:
                pass
        else:
            print("CreditCard authentication failed.")
    else:
        print("There was a problem with your payment.")
else:
    print("Hotel is not free")