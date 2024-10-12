from ml_lib import QaqcTestModel

qaqc_obj = QaqcTestModel()

qaqc_obj.run(file_name="swe_qaqc_lib_test", is_first=True)

df = qaqc_obj.get_data()

print(df)
