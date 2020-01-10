# API Documentation

#### Backend delpoyed at [Heroku](https://lambda-beastmode.herokuapp.com) <br>


To get the server running locally:

- Clone this repo
- **pipenv install** to install required dependencies
- From CLI /manage.py runserver

### Backend framework made with Django

🚫 Why did you choose this framework?

-    Flexibility
-    Reliability
-    Scalability
-    Simplicity
-    Batteries Included
-    ORM
-    Middleware support

##  Endpoints

       |

#### User Routes

| Method | Endpoint                | Access Control      | Description                                        |
| ------ | ----------------------- | ------------------- | -------------------------------------------------- |
| GET    | `/api/init/`        | all users           | Initializes the map and player object from User token.               |
| POST    | `/api/move/`    | all users | Moves player from room to room.             |
| POST    | `/api/say/`        | all users | Displays text message to all Users in Room.                    |


# login/ register

| POST   | `/users/register/owner` | none                | Creates a new user as owner of a new organization. |
| PUT    | `/users/:userId`        | owners, supervisors |                                                    |
| DELETE | `/users/:userId`        | owners, supervisors |                                                    |

# Data Model

####  Room

---

```
{
  id: INTEGER 
  title: STRING
  description: STRING
  x: INTEGER
  y: INTEGER
  n_to: INTEGER
  e_to: INTEGER
  s_to: INTEGER
  w_to: INTEGER
}
```

#### Player

---

```
{
  user: username
  currentRoom : INTEGER
  uuid: UUID
}
```


##  Environment Variables

In order for the app to function correctly, the user must set up their own environment variables.

create a .env file that includes the following:

    * SECRET_KEY - authorization token
    * DATABASE_URL - location of database production/local
    * DEBUG - TRUE/FALSE
    * PUSHER_APP_ID - ID
    * PUSHER_KEY - KEY
    * PUSHER_SECRET - Token
    * PUSHER_CLUSTER - AWS cluster server
    
## Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./code_of_conduct.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Frontend Documentation](https://github.com/CSBeastMode/front-end/tree/auth) for details on the fronend of our project.
