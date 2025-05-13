import pytest
import pymongo

from unittest.mock import patch
from src.util.dao import DAO


class TestDaoCreate:
    """
    Test suite for DAO create
    """

    @pytest.fixture
    def sut_user(self):
        """
        Fixture for creating user DAO
        """
        dao = DAO(collection_name="testUser", test_database=True)
        try:
            yield dao
        finally:
            dao.drop()

    @pytest.fixture
    def sut_video(self):
        """
        Fixture for creating video DAO
        """
        dao = DAO(collection_name="testVideo", test_database=True)
        try:
            yield dao
        finally:
            dao.drop()

    def test_dao_create_invalid(self, sut_user):
        """
        Invalid format, required property lastName missing
        """
        with pytest.raises(pymongo.errors.WriteError):
            sut_user.create({"firstName": "Test", "email": "test@test.se"})

    def test_dao_create_valid_unique(self, sut_user):
        """
        Valid format and unique email address should return object
        """
        object = sut_user.create(
            {"firstName": "Test", "lastName": "Testson", "email": "test@test.se"}
        )
        obj = sut_user.create(
            {"firstName": "Test", "lastName": "Testson", "email": "unique@test.se"}
        )

        assert isinstance(obj, dict)

    def test_dao_create_valid_not_unique(self, sut_user):
        """
        Valid format but not unique email address should raise WriteError
        """
        object = sut_user.create(
            {"firstName": "Test", "lastName": "Testson", "email": "test@test.se"}
        )
        with pytest.raises(pymongo.errors.WriteError):
            sut_user.create(
                {"firstName": "Test", "lastName": "Testson", "email": "test@test.se"}
            )

    def test_dao_create_video_valid_not_unique(self, sut_video):
        """
        Valid format and not unique url should return object
        """
        object = sut_video.create({"url": "https://url.com"})
        obj = sut_video.create({"url": "https://url.com"})

        assert isinstance(obj, dict)

    def test_dao_create_video_invalid_type(self, sut_video):
        """
        Invalid type raises WriteError
        """
        with pytest.raises(pymongo.errors.WriteError):
            obj = sut_video.create({"url": 42})
