from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import ANY
    
client = TestClient(app)

def test_run_ml(mock_mongo_connection):
    """
    This test just makes sure normal routes work
    """
    
    response = client.post("/V1/run_ml/?file=swe_qaqc_lib_test&model_name=QaqcMainModel&dim_red_method=COMBO")
    assert response.status_code == 200
    assert response.json() == {
        "ml_id": "QaqcMainModel_swe_qaqc_lib_test",
        "status": "Running",
        "details": "Request received",
        "running_time": "",
        "updated": ANY
        }
