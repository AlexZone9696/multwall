from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from tronpy.keys import PrivateKey as TronPrivateKey
from eth_account import Account
from flask import Flask, jsonify, render_template
import webbrowser

# Создаем Flask-приложение
app = Flask(__name__)

# Функция генерации кошельков с общей мнемоникой
def generate_wallets():
    # Генерируем 12-словную мнемоническую фразу
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    
    # Ethereum (BIP44, m/44'/60'/0'/0/0)
    bip44_eth_ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    eth_private_key = bip44_eth_ctx.PrivateKey().Raw().ToHex()
    eth_address = bip44_eth_ctx.PublicKey().ToAddress()
    eth_wallet = {
        "address": eth_address,
        "private_key": eth_private_key
    }

    # Binance Smart Chain (тот же путь, что и Ethereum, так как BNB BEP20 совместим с адресами ETH)
    bnb_wallet = {
        "address": eth_address,  # Адрес совпадает с ETH
        "private_key": eth_private_key
    }
    
    # TRON (тот же путь, что и Ethereum, так как адреса совместимы)
    tron_private_key = TronPrivateKey.fromhex(eth_private_key)
    tron_address = tron_private_key.public_key.to_base58check_address()
    tron_wallet = {
        "address": tron_address,
        "private_key": eth_private_key
    }
    
    return {
        "mnemonic": str(mnemonic),  # Преобразуем мнемонику в строку
        "wallets": {
            "ethereum": eth_wallet,
            "bnb": bnb_wallet,
            "tron": tron_wallet
        }
    }

# Маршрут для главной страницы
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для генерации кошельков
@app.route('/generate_wallets', methods=['GET'])
def generate_wallets_route():
    wallet_data = generate_wallets()
    return jsonify(wallet_data)

if __name__ == '__main__':
    # Открываем браузер автоматически после запуска сервера
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
