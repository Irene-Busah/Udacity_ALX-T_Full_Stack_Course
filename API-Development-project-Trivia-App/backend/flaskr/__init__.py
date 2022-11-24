from crypt import methods
import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginatedQuestions(request, questions_selection):
    """organises the questions into pages"""
    pages = request.args.get('page', 1, type=int)
    start = (pages - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    data = []
    for question in questions_selection:
        display = question.format()
        data.append(display)
    questions = data[start:end]
    return questions


# ===================================================
# CREATE_APP FUNCTION
# ===================================================

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app=app, resources={"/": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def afterRequest(response):
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response


    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    # ======================== READ ENDPOINTS ========================

    @app.route('/categories', methods=['GET'])
    def getAllCategories():
        """retrieves all the categories inthe server/database"""
        categories = Category.query.order_by(Category.id).all()
        category = {}
        # returning 404 if there is no category in the database
        if len(categories) is None:
            abort(404)
        else:
            category = {}
            # looping through the queried data and update the category object
            for cateSelect in categories:
                category.update({cateSelect.id: cateSelect.type})
            return jsonify({
                'success': True,
                'categories': category
            })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    def getAllQuestion():
        """retrieves all the questions in the server/database"""
            
        questions = Question.query.all()
        questionSelection = paginatedQuestions(request, questions)

        # get all categories
        categories = Category.query.all()
        category = {}
        for cate in categories:
            category.update({cate.id: cate.type})
            

        # abort 404 if no questions
        if (len(questionSelection) == 0):
            abort(404)

        # returning the data to view on the frontend
        return jsonify({
            'success': True,
            'questions': questionSelection,
            'total_questions': len(questions),
            'categories': category
        })

    
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:categoryID>/questions', methods=['GET'])
    def retrieve_category_questions(categoryID):
        """retrieves all the questions related to a category"""
        category = Category.query.get(categoryID)
        if not category:
            abort(404)

        else:
            questions = Question.query.order_by(Question.id).filter(Question.category == str(categoryID)).all()
            current_questions = paginatedQuestions(request=request, questions_selection=questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'current_category': category.type,
                'total_questions': len(questions)
            })
        


    # ======================== DELETE ENDPOINT ======================

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:questionID>', methods=['DELETE'])
    def delete_specific_question(questionID):
        """remove a specific question from the frontend & server"""
        query_question = Question.query.get(questionID)

        if query_question is None:
            abort(404)

        try:
            query_question.delete()
            question_selection = Question.query.order_by(Question.id).all()
            current_questions = paginatedQuestions(request, questions_selection=question_selection)
            return jsonify({
                'success': True,
                'Deleted_ID': questionID,
                'Current_Questions': current_questions
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """


    # ==================== CREATE ENDPOINT =========================

    @app.route('/questions', methods=['POST'])
    def add_question():
        """inserts a new question into the database"""
        request_body = request.get_json()
        newQuestion = request_body.get('question', None)
        new_answer = request_body.get('answer', None)
        new_category = request_body.get('category', None)
        difficulty_level = request_body.get('difficulty', None)
        try:
            question = Question(question=newQuestion, answer=new_answer, category=new_category, difficulty=difficulty_level)
            question.insert()

            question_selection = Question.query.order_by(Question.id).all()
            current_questions = paginatedQuestions(request=request, questions_selection=question_selection)
            # flash('Question created successfully')
            return jsonify({
                'Success': True,
                'New_question_ID': Question.id,
                'Current_questions': current_questions,
                'Total_Number_Questions': len(question_selection)
            })
        except:
            abort(422)



    # ======================== SEARCH ENDPOINT ======================

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/searchedQuestions', methods=['POST'])
    def find_question():
        """searches for questions in the server given a specific searching term"""
        

        request_body = request.get_json()
        search_key = request_body.get('searchTerm')
        search_word  = Question.query.filter(
            Question.question.ilike(f'%{search_key}%')).all()

        if len(search_word) == 0:
            abort(404)
        available_questions = paginatedQuestions(request=request, questions_selection=search_word)
        return jsonify({
            'Success': True,
            'Total_questions': len(search_word),
            'Questions': available_questions
        })




    

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        
        request_body = request.get_json()
        question = request_body['previous_questions']
        category = request_body['quiz_category']
        

        if category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == category['id']).all()
        question = None
        if questions:
            question = random.choice(questions).format()

        return jsonify({
            'success': True,
            'question': question
        })

        


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(422)
    def unprocessable_error_422(error):
        return jsonify({
            'success': False,
            'Error': 422,
            'Message': 'Unprocessable'
        }), 422
    
    @app.errorhandler(404)
    def not_found_error_404(error):
        return jsonify({
            'success': False,
            'Error': 404,
            'Message': 'Not Found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    return app

