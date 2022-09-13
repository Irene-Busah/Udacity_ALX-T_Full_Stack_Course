import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}:{}@{}:{}/{}'.format('postgres', 'abc', 'localhost', '5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
			'question': 'What is total people in CS',
			'answer': '97',
			'difficulty': 2,
            'category': "History"
		}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_paginated_Questions(self):
        """tests the paginated questions function"""
        query_res = self.client().get('/questions')
        query_data = json.loads(query_res.data)

        self.assertEqual(query_res.status_code, 200)
        self.assertEqual(query_data['success'], True)
        self.assertTrue(query_data['questions'])
        self.assertTrue(query_data['categories'])
        self.assertTrue((query_data['total_questions']))
    
    def test_delete_question(self):
        """tests the delete endpoint"""
        query_res = self.client().delete('/questions/14')
        query_data = json.loads(query_res.data)

        self.assertEqual(query_res.status_code, 200)
        self.assertEqual(query_data['success'], True)
        self.assertEqual(query_data['Deleted_ID'], 14)
        # self.assertTrue(query_data['Current_Questions'])

    def test_422_if_question_does_not_exist(self):
        """tests the delete endpoint if the question does not exit"""
        query_res = self.client().delete('/questions/1000')
        query_data = json.loads(query_res.data)

        self.assertEqual(query_res.status_code, 404)
        self.assertEqual(query_data['success'], False)
        self.assertEqual(query_data['Message'], 'Not Found')
    
    def test_add_question(self):
        """tests the add endpoint"""
        

        res = self.client().post('/questions', json=self.new_question)
        query_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(query_data['Success'], True)
        # self.assertTrue(query_data['New_question_ID'])
        # self.assertTrue(query_data['Total_Number_Questions'])
    
    def test_404_if_questions_creation_not_allowed(self):
        """test the add question to the wrong endpoint"""
        self.new_question = {
			'question': 'What is total people in CS',
			'answer': '97',
			'difficulty': 2,
            'category': "History"
		}
        res = self.client().patch('/questions', json=self.new_question)
        query_data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(query_data['success'], False)
        self.assertEqual(query_data['message'], 'Method Not Allowed')
    
    def test_search_endpoint(self):
        """tests the search endpoint"""
        res = self.client().post('/searchedQuestions', json={'searchTerm': 'What is'})
        query_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(query_data['Success'], True)
        self.assertTrue(len(query_data['Questions']))
    
    def test_404_search_not_found(self):
        """tests the search endpoint if the search word is not found"""
        query_res = self.client().post('/searchedQuestions', json={'searchTerm': 'kdjggdjfygdygdfqy', })
        query_data = json.loads(query_res.data)
        self.assertEqual(query_res.status_code, 404)
        self.assertEqual(query_data['success'], False)
        self.assertEqual(query_data['Message'], 'Not Found')

    def test_quiz(self):
        """tests """
        query_res = self.client().post('/quizzes', json={'previous_questions': [14], 'quiz_category': {'type':'History', 'id': '4'}})
        query_data = json.loads(query_res.data)
        self.assertEqual(query_res.status_code, 200)
        self.assertEqual(query_data['success'], True)
        # self.assertEqual(query_data['question']['category'], '4')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()