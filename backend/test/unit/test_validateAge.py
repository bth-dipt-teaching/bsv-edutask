# import pytest
# import unittest.mock
# from src.util.helpers import ValidationHelper

# @pytest.mark.unit
# def test_hasAttribute_Underage():
#     # print("hsbihsbhkablhkb")
#     # Create mock objeckt
#     mockobjekt = unittest.mock.mock.MagicMock()
#     mockobjekt.get.return_value = {"age": 5}
#     validate = ValidationHelper()
#     result = validate.validateAge(5)
#     # print(result)
#     assert result == "underaged"
    
# @pytest.mark.unit
# def test_hasAttribute_Valid():
#     # print("hsbihsbhkablhkb")
#     validate = ValidationHelper()
#     result = validate.validateAge(40)
#     # print(result)
#     assert result == "valid"
    
# @pytest.mark.unit
# def test_hasAttribute_Invalid():
#     # print("hsbihsbhkablhkb")
#     validate = ValidationHelper()
#     result = validate.validateAge(150)
#     # print(result)
#     assert result == "invalid"