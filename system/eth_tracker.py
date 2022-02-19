import datetime
import cryptocompare

def get_eth_price():
    coin_dict = cryptocompare.get_price('ETH', currency="USD")
    return f"以太幣: {coin_dict['ETH']['USD']} 美元"