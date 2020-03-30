import os
import sys
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  #create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. 
  Delete the sample route after completing the TODOs
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  ##After a request is received run this method - CORS headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  def get_formatted_categories():
    categories = Category.query.all()
    '''print(type(categories[0].format())) => <class 'models.Category'> to <class 'dict'>'''
    formatted_categories = [None] + [category.type for category in categories]
    return formatted_categories

  '''
  @TODO:
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/')
  def index():
    return jsonify({'message': 'Welcome to Trivia!'})

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def show_questions():
    questions = Question.query.all()
    formatted_questions = paginate_questions(request,questions)

    if len(formatted_questions) <= 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": formatted_questions,
      "total_questions": len(formatted_questions),
      "currentCategory": '',
      "categories": get_formatted_categories()
    })

  @app.route('/categories')
  def show_categories():
    return jsonify({
      "success": True,
      "categories": get_formatted_categories()
    })

  @app.route('/questions/<int:question_id>')
  def get_question(question_id):
    question = Question.query.filter_by(id=question_id).first()
    return jsonify({
      "success": True,
      "question": question.format()
    })
  """
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """

  @app.route('/question/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    print("delete request received  ")
    Question.filter_by(id=question_id).delete()
    return jsonify({
      "success": True,
      "deleted_question": question_id,
      "message": "Successfully Deleted!"
    })
    #db.session.commit()


  """
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """
  @app.route('/questions/add', methods=['POST'])
  def add_question():
    error = False
    data_string = request.data
    question_data = json.loads(data_string)
    try:
      question_string = question_data['question']
      answer = question_data['answer']
      category = question_data['category']
      difficulty = question_data['difficulty']

      question = Question(question=question_string,answer=answer,category=category,difficulty=difficulty)
    
      question.insert()
    except Exception as err:
      error = True
      print(sys.exc_info())
    finally:
      if error:
        abort(422)
      else:
        return jsonify({
          "success": True,
          "message":'New question was added successfully!'
        })
    

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    data_string = request.data
    data = json.loads(data_string)
    searchTerm = "%" + data['searchTerm'] + "%"
    result = Question.query.filter(Question.question.ilike(searchTerm)).all()
    formatted_questions = [question.format() for question in result]
    return jsonify({
      "questions": formatted_questions,
      "totalQuestions":len(formatted_questions),
      "currentCategory": ""
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def get_questions(category_id):
    questions = Question.query.filter_by(category=category_id).all()
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions) <=0:
      abort(404)
    else:
      return jsonify({
        "success": True,
        "questions": formatted_questions,
        "totalQuestions": len(formatted_questions),
        "currentCategory": ''
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    data = request.get_json()
    category_id = data['quiz_category']['id']
    all_questions_in_category = Question.query.filter_by(category=category_id).all()
    
    #all_questions_in_category =[question.format() for question in all_questions_in_category]
    if len(all_questions_in_category) <= 0:
      abort(404)
    previous_questions = data['previous_questions']
    random_question = None
    if not previous_questions:
      random_question = random.choice(all_questions_in_category)
    else:
      filtered_questions = []
      for question in all_questions_in_category:
        if question.id not in previous_questions:
          filtered_questions.append(question)
      if len(filtered_questions) == 0:
        random_question = None
      else:
        random_question = random.choice(filtered_questions)
    if not random_question:
      return jsonify({
        "success":True,
        "forceEnd": True
      })
    else:
      return jsonify({
        "success": True,
        "question": random_question.format()
       })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  abort(404) - are not very clear so we can handle uniformly with the below decorator
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }),400


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource Not Found"
    }),404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable entity"
    }),422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Server Error"
    }),500

  return app
