import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_card = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")


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


class CreditCard:
    def __init__(self, numbers):
        self.numbers = numbers

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.numbers, "expiration": expiration, "cvc": cvc, "holder": holder}
        if card_data in df_card:
            return True
        else:
            return False


print(df)

hotel_ID = input("Enter the id of hotel: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    credit_card = CreditCard(numbers="1234")
    if credit_card.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        hotel.book()
        name = input("Enter your name: ")
        reservation_ticket = ReservationTicket(name, hotel)
        print(reservation_ticket.generation())
    else:
        print("There was a problem with your payment.")
else:
    print("Hotel is not free")