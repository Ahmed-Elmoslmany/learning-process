import unittest
from assertpy import assert_that
import controllers.candidates as candidates
import http



class TestGetAllCandidatesController(unittest.TestCase):
    def test_get_candidates(self):
        request = RequestDouble('/candidates')
        controller = candidates.GetAllCandidatesController(request)
        response, status_code = controller.get_candidates()
        assert_that(response.get('path')).is_equal_to('/candidates')
        assert_that(status_code).is_equal_to(http.HTTPStatus.OK)
        
        
class TestGetCandidateController(unittest.TestCase):
    def test_get_candidate(self):
        request = RequestDouble('/candidates/<int:id>')
        controller = candidates.GetCandidateController(request)
        response, status_code = controller.get_candidate()
        assert_that(response.get('path')).is_equal_to('/candidates/<int:id>')
        assert_that(status_code).is_equal_to(http.HTTPStatus.OK)
        
                
class TestCreateCandidateController(unittest.TestCase):
    def test_create_candidate(self):
        request = RequestDouble('/candidates')
        controller = candidates.CreateCandidateController(request)
        response, status_code = controller.create_candidate()
        assert_that(response.get('path')).is_equal_to('/candidates')
        assert_that(status_code).is_equal_to(http.HTTPStatus.CREATED)
        
        
class TestUpdateCandidateController(unittest.TestCase):
    def test_update_candidate(self):
        request = RequestDouble('/candidates/<int:id>')
        controller = candidates.UpdateCandidateController(request)
        response, status_code = controller.update_candidate()
        assert_that(response.get('path')).is_equal_to('/candidates/<int:id>')
        assert_that(status_code).is_equal_to(http.HTTPStatus.OK)        
        

class TestDeleteCandidateController(unittest.TestCase):
    def test_delete_candidate(self):
        request = RequestDouble('/candidates/<int:id>')
        controller = candidates.DeleteCandidateController(request)
        response, status_code = controller.delete_candidate()
        assert_that(response.get('path')).is_equal_to('/candidates/<int:id>')
        assert_that(status_code).is_equal_to(http.HTTPStatus.OK)        

                
class TestCandidatesCollectionSerializer(unittest.TestCase):
    def test_serialize_candidates_successfully(self):
        given_candidates = [CandidateDouble('John', 'Doe'), CandidateDouble('John2', 'Doe2')]
        result = candidates._CandidatesCollectionSerializer(given_candidates).serialize('/candidates')  
        first_candidate = result.get('data')[0]
        second_candidate = result.get('data')[1] 
        assert_that(result.get('path')).is_equal_to('/candidates')
        assert_that(first_candidate.get('firstName')).is_equal_to('John')
        assert_that(first_candidate.get('lastName')).is_equal_to('Doe')
        assert_that(second_candidate.get('firstName')).is_equal_to('John2')
        assert_that(second_candidate.get('lastName')).is_equal_to('Doe2')


class TestCandidateSingleSerializer(unittest.TestCase):
    def test_serialize_single_candidate_successfully(self):
        given_candidate = CandidateDouble('John', 'Doe')
        result = candidates._CandidateSingleSerializer(given_candidate).serialize('/candidates')
        assert_that(result.get('path')).is_equal_to('/candidates')
        candidate = result.get('data')
        assert_that(candidate.get('firstName')).is_equal_to('John')
        assert_that(candidate.get('lastName')).is_equal_to('Doe')
        

class TestCandidateSerializer(unittest.TestCase):
    def test_serialize_candidate_successfully(self):
        given_candidate = CandidateDouble('John', 'Doe')
        result = candidates._CandidateSerializer(given_candidate).serialize()
        assert_that(result.get('firstName')).is_equal_to('John')
        assert_that(result.get('lastName')).is_equal_to('Doe')
        

class TestCandidateMessageSerializer(unittest.TestCase):
    def test_serialize_message(self):        
        given_message = MessageDouble('message')
        result = candidates._CandidateMessageSerializer(given_message).serialize('/candidates/<int:id>')
        data = result.get('data')
        assert_that(result.get('path')).is_equal_to('/candidates/<int:id>')
        assert_that(data.get('message')).is_equal_to('message')
        
                
class CandidateDouble:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        

class RequestDouble:
    def __init__(self, path):
        self.path = path
        
        
class MessageDouble:
    def __init__(self, message):
        self.message = message
        

    
if __name__ == '__main__':
    unittest.main()     
