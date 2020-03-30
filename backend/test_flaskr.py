import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10 

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}/{}".format('archanapur@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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

    def test_retrieve_categories(self):
        """ Tests GET /categories to retrieve all available categories """
        res = self.client().get('/categories')
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['categories']))

    def test_retrieve_questions(self):
        """ Tests GET /questions to retrieve all questions including pagination 
        (every 10 questions) and number of total questions """
        res = self.client().get('/questions?page=2')
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(data['success'])
        self.assertLessEqual(data['total_questions'],QUESTIONS_PER_PAGE) 
    
    def test_retrieve_questions_nonexistent_page(self):
        """ Tests GET /questions to retrieve all questions including pagination 
        (every 10 questions) and number of total questions """
        res = self.client().get('/questions?page=11')
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        """ Tests DELETE /questions/<int:question_id> to delete a specific question """
        
        res = self.client().delete('/questions/15')
        data = res.get_json()
        deleted_not_found = Question.query.get(20)
        self.assertEqual(res.status_code,200)
        self.assertEqual(deleted_not_found,None)
        self.assertTrue(data['success'])
        self.assertLessEqual(data['deleted_question'],20) 

    def test_delete_nonexistent_question(self):
        """ Tests DELETE /questions/<int:question_id> to delete a specific question """
        
        res = self.client().delete('/questions/14')
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertFalse(data['success'])

    def test_add_new_question(self):
        ''' Test for POST /questions/add - successfull addition of new question'''
        res = self.client().post('/questions/add',json = {
            "question":"Which organ removes excess water from the blood?",
            "answer": "Kidney",
            "category": 1,
            "difficulty": 3
            })
        data = res.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code,200)

    def test_bad_request_add_new_question(self):
        ''' Test for POST /questions/add failure addition'''
        res = self.client().post('/questions/add',json = {
            "Auestion":"Which is the most acidic part of the digestive system?",
            "Answer": "Stomach",
            "Category": 1
            })
        data = res.get_json()
        self.assertFalse(data['success'])
        self.assertEqual(res.status_code,422)
        self.assertEqual(data['message'],'Unprocessable entity')
    
    def test_search_for_keyword(self):
        ''' TEST POST /questions/search of successful search for specific question'''
        res = self.client().post('/questions/search',json = {
            "searchTerm":"movie"
            })
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue((data['totalQuestions']))

    def test_get_questions_in_category(self):
        ''' TEST GET /categories/<category_id>/questions to get all questions in specific category'''
        res = self.client().get('/categories/1/questions')
        data = res.get_json()
        self.assertEqual(res.status_code,200)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['success'])
    
    def test_get_questions_in_nonexistant_category(self):
        ''' TEST GET /categories/<category_id>/questions to get questions in non existant category'''
        res = self.client().get('/categories/111/questions')
        data = res.get_json()
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],"Resource Not Found")
        self.assertFalse(data['success'])

    def test_get_random_question_for_quiz(self):
        ''' TEST POST /quizzes successful get random question from specific category'''
        res = self.client().post("/quizzes",json = {
            "quiz_category": 
                {
                    "type":"Geography",
                    "id":"3"
                },
            "previous_questions": [14]
        })
        data  = res.get_json()
        self.assertTrue(data['success'])
        self.assertTrue(data['question']['id'] != 14)

    def test_no_questions_available_for_quiz(self):
        ''' TEST POST /quizzes to get random question from consumed category'''
        res = self.client().post("/quizzes",json = {
            "quiz_category": 
                {
                    "type":"Geography",
                    "id":"3"
                },
            "previous_questions": [13,14,15]
        })
        data  = res.get_json()
        #self.assertFalse(data['success'])
        self.assertTrue(data['forceEnd'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()