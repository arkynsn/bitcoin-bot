import pyupbit

access = "HxzMreaqvtoc197sqiqluljcgIB4NNK79UKSB7WP"
secret = "I2ZDtT1EZqxswZFuDQg6u3qwXnII6GRSZNgi9U9Q"

upbit = pyupbit.Upbit(access, secret)

balances = upbit.get_balances()

print(balances)