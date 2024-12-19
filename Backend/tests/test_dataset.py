from fastapi.testclient import TestClient
from src.main import app
from unittest.mock import ANY
    
client = TestClient(app)

def test_run_ml_status(mock_mongo_connection):
    """
    This test just makes sure normal routes work
    """
    response = client.get("/V1/dataset/files")
    assert response.status_code == 200
    assert response.json() == {
        "dataList": []
    }
    
    response = client.get("/V1/dataset")
    assert response.status_code == 200
    assert response.json() == {
        "dataList": []
    }
    
    response = client.post("/V1/dataset/?filename=swe_qaqc_lib_test", files={"uploaded_file": ("swe_qaqc_lib_test.csv", open("Backend/tests/test-files/swe_qaqc_lib_test.csv", "rb")), 
                                                                                     "uploaded_info_file": ("qaqc_info.json", open("Backend/tests/test-files/qaqc_info.json", "rb"))})
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "details": "File 'swe_qaqc_lib_test' uploaded"
    }
    
    response = client.get("/V1/dataset/files")
    assert response.status_code == 200
    assert response.json() == {
        "dataList": [
            {
                "dataset": "swe_qaqc_lib_test",
                "id": "123"
            }
        ]
    }
    
    response = client.delete("/V1/dataset/?dataset=swe_qaqc_lib_test")
    assert response.status_code == 204
    
    response = client.get("/V1/dataset/files")
    assert response.status_code == 200
    assert response.json() == {
        "dataList": []
    }