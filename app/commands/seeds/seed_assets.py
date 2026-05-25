from app.core.database import SessionLocal
from app.models.asset import Asset

ASSETS = [
    {
        "name": "Bitcoin",
        "symbol": "BTC",
        "code": "BTC-USD",
    },
    {
        "name": "Ethereum",
        "symbol": "ETH",
        "code": "ETH-USD",
    },
    {
        "name": "Tether",
        "symbol": "USDT",
        "code": "USDT-USD",
    },
    {
        "name": "BNB",
        "symbol": "BNB",
        "code": "BNB-USD",
    },
    {
        "name": "XRP",
        "symbol": "XRP",
        "code": "XRP-USD",
    },
    {
        "name": "USD Coin",
        "symbol": "USDC",
        "code": "USDC-USD",
    },
    {
        "name": "Solana",
        "symbol": "SOL",
        "code": "SOL-USD",
    },
    {
        "name": "TRON",
        "symbol": "TRX",
        "code": "TRX-USD",
    },
    {
        "name": "Dogecoin",
        "symbol": "DOGE",
        "code": "DOGE-USD",
    },
    {
        "name": "Cardano",
        "symbol": "ADA",
        "code": "ADA-USD",
    },
]


def run():
    db = SessionLocal()

    try:
        created = 0

        for asset_data in ASSETS:
            exists = db.query(Asset).filter(Asset.code == asset_data["code"]).first()

            if exists:
                print(f"[SKIP] {asset_data['code']} already exists")
                continue

            asset = Asset(
                name=asset_data["name"],
                symbol=asset_data["symbol"],
                code=asset_data["code"],
            )

            db.add(asset)
            created += 1

            print(f"[CREATED] {asset_data['code']}")

        db.commit()

        print("")
        print(f"Seeder finished. Created: {created}")

    except Exception as exc:
        db.rollback()

        print(f"[ERROR] {str(exc)}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run()
