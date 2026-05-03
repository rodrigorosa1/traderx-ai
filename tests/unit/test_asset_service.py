import unittest
from unittest.mock import Mock
from uuid import uuid4

from app.schemas.asset_schema import AssetOut
from app.services.asset_service import AssetService


class TestAssetService(unittest.TestCase):
    def test_find_all_success(self):
        assets = [
            AssetOut(id=uuid4(), name="Bitcoin", symbol="BTC-USD", code="BTC"),
            AssetOut(id=uuid4(), name="Ethereum", symbol="ETH-USD", code="ETH"),
        ]

        mock_repo = Mock()
        mock_repo.find_all.return_value = assets

        service = AssetService(mock_repo)
        result = service.find_all()

        self.assertEqual(result, assets)
        mock_repo.find_all.assert_called_once()
