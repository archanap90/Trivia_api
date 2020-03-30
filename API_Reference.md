## API Reference

### Getting Started
* Base URL:  At this point app can be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/` and `http://localhost:3000/` for the frontend.

### Error Handling

Errors are returned as JSON objects in the following format:
```
    {
        "success": False,
        "error": 422,
        "message": "Unprocessable entity"
    }
```

The API will return two error types when requests fail:
* 404: Resource Not Found
* 422: Not processable 

### Endpoint Library

#### GET /categories
* General: Returns a list of categories and success value.
* Sample:
```
curl http://127.0.0.1:5000/categories

{
    "categories": [
        null,
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "success": true
}
```
#### GET /questions
* General: Returns a list of categories, list of questions, total number of questions and success value. Results are paginated in group of 10 questions. Include a request argument to choose page number, starting from 1.

* Sample:
```
curl http://127.0.0.1:5000/questions?page=2

{
    "categories": [],
    "currentCategory": "",
    "questions": [],
    "success": true,
    "total_questions": 10
}
```

#### GET /questions/<int:question_id>
* General: Returns the question and success value.
* Sample:
```
curl http://127.0.0.1:5000/questions/12

{
    "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
    },
    "success": true
}
```
#### DELTE /questions/<int:question_id>
* General: Deletes the question with id passed in the request parameter. And, 
returns success value and a message
* Sample:
```
curl --request DELETE 'http://localhost:3000/questions/12' \
        --header 'Content-Type: application/json' \
        --data-raw '{
	                    "searchTerm": "movie"
                    }'

{
    "success": true,
    deleted_question": 12,
    "message": "Successfully Deleted!"
}
```
#### POST /questions/add
* General: Adds a new question in the database. And, returns a success value and message
* Sample:
```
curl --request POST 'http://localhost:3000/questions/add' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "answer": "George Washington Carver",
        "category": 4,
        "difficulty": 2,
        "question": "Who invented Peanut Butter?"
    }'

{
  "message": "New question was added successfully!",
  "success": true
}
```
#### POST /questions/search
* General: Searches for all the questions containing the search term passed in request and returns a list of questions and total number.

* Sample:
```
curl --request POST 'http://localhost:3000/questions/search' \
    --header 'Content-Type: application/json' \
    --data-raw '{
	    "searchTerm": "movie"
        }'

{
  "currentCategory": "",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "totalQuestions": 1
}
```

#### GET /categories/<int:category_id>/questions
* General: Returns the list questions under the category passed as parameter in the request, success value and total number of questions.
* Sample:
```
curl http://127.0.0.1:5000/categories/2/questions

{
    "currentCategory": "",
    "questions": [
    {},
    {},
    {},
    {}
    ],
    "success": true,
    "totalQuestions": 4
}
```
#### POST  /quizzes
* General: Returns a random question that's not in the previousQuestions list passed as POST request data.
* Sample:
```
curl --request POST 'http://127.0.0.1:5000/quizzes' \
    --header 'Content-Type: application/json' \
    --data-raw '
            {
                "previous_questions":[],
                "quiz_category":
                    {
                        "type":"Science",
                        "id":"1"
                    }
            }'

{
  "question": {
    "answer": "Acoustics",
    "category": 1,
    "difficulty": 2,
    "id": 24,
    "question": "The behavior of sound in rooms and concert halls is a separate science what is its name?"
  },
  "success": true
}
```


