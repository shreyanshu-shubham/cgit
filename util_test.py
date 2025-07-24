import pytest
import os
import shutil
import util

# TODO : raise proper errors in code and write test for it

@pytest.fixture(scope="function")
def empty_folder():
    temp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"test-repo")
    os.makedirs(temp_folder,exist_ok=False)
    yield temp_folder
    shutil.rmtree(temp_folder)

class TestUtils:

    def test_cgit_get_root_no_init(self,empty_folder):
        assert util.get_cgit_root(empty_folder) == None

    def test_cgit_get_root(self,empty_folder):
        util.init_repo(empty_folder)

        dir1 = os.path.join(empty_folder,"dir1")
        os.makedirs(dir1)

        assert util.get_cgit_root(empty_folder) == empty_folder
        assert util.get_cgit_root(dir1) == empty_folder

    def test_cgit_not_init(self, empty_folder):
        assert util.is_in_cgit_repo(empty_folder) == False

    def test_cgit_init(self, empty_folder):
        util.init_repo(empty_folder)
        assert util.is_in_cgit_repo(empty_folder) == True
    
