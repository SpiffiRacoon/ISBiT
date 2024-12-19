from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import ANY
    
client = TestClient(app)

def test_run_ml(mock_mongo_connection):
    """
    This test just makes sure normal routes work
    """
    
    test_get_ml_dim = client.get('/V1/ml/dim')
    assert test_get_ml_dim.status_code == 200
    assert test_get_ml_dim.json() == [
        "COMBO",
        "PCA",
        "TSNE",
        "UMAP"
    ]
    test_get_models = client.get('/V1/ml/models')
    assert test_get_models.status_code == 200
    assert test_get_models.json() == [
        "QaqcMainModel"
    ]