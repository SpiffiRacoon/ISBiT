import pytest
import asyncio
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_run_ml_with_polling(mock_mongo_connection):
    """
    Example test with polling mechanism to check ML run status
    """
    # Step 1: Upload test dataset
    response = client.post(
        "/V1/dataset/?filename=swe_qaqc_lib_test",
        files={
            "uploaded_file": ("swe_qaqc_lib_test.csv", open("Backend/tests/test-files/swe_qaqc_lib_test.csv", "rb")),
            "uploaded_info_file": ("qaqc_info.json", open("Backend/tests/test-files/qaqc_info.json", "rb"))
        }
    )
    assert response.status_code == 200

    # Step 2: Start the ML run
    start_response = client.post('/V1/run_ml/?file=swe_qaqc_lib_test&model_name=QaqcMainModel&dim_red_method=COMBO')
    assert start_response.status_code == 200

    # Step 3: Poll for status
    max_retries = 10  # Maximum number of polls
    interval = 2  # Seconds between polls

    for attempt in range(max_retries):
        print(f"Polling attempt {attempt + 1}/{max_retries}...")
        status_response = client.get('/V1/run_ml/?model_name=QaqcMainModel&file=swe_qaqc_lib_test')
        assert status_response.status_code == 200

        status = status_response.json()
        print("Current status:", status)
        
        # Check if ML run has completed
        if status["status"] == "Not running" and status["details"] == "Success ML run completed":
            print("ML run completed successfully.")
            break

        # Wait before the next poll
        await asyncio.sleep(interval)
    else:
        pytest.fail("ML run did not complete within the expected time.")

    # Step 4: Clean up
    flush_response = client.post('/V1/run_ml/flush?model_name=QaqcMainModel&file=swe_qaqc_lib_test')
    assert flush_response.status_code == 201
