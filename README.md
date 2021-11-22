# Project-Contributors
## How to run
In order to run the application, you should only have a docker installation in your environment.
Follow the next steps
- Go inside project-contributors directory ()
```sh
cd project-contributors
```
- Run the command
```sh
sudo docker-compose up --build
```
And that's it! Project-Contributors is now up to test it, with an Sqlite3 database.

## How to use
You can try it with Postman request tool:
### Below are some examples of the basic endpoints:
##### POST: localhost:8000/api/add_user/
#
```sh
    {
        "username": "user1",
        "password": "1111",
        "email": "user1@gmail.com",
        "age": 30,
        "first_name": "Dimosthenis",
        "last_name": "Dimos",
        "country": "Greece",
        "residence": "Achaia"
    }
```
##### POST: localhost:8000/api/login/
#
```sh
    {
        "username": "user1",
        "password": "1111",
    }
```
##### POST: localhost:8000/api/add_skills/
#
```sh
    {
        "added_skills": ["Go", "Python"]
    }
```
##### POST: localhost:8000/api/remove_skills/
#
```sh
    {
        "deleted_skills": ["Python"]
    }
```
##### POST: localhost:8000/api/create_project/
#
```sh
{
    "project_name": "Project Contributors",
    "description": "Django Project",
    "maximum_collaborators": 8,
    "collaborators": 4
}
```
##### POST: localhost:8000/api/remove_project/
#
```sh
{
    "project_name": "Project Contributors"
}
```
##### GET: localhost:8000/api/open_projects/
##### RESPONSE:
#
```sh
[
    {
        "id": 2,
        "project_name": "Project Contributors",
        "description": "Django Project",
        "maximum_collaborators": 8,
        "collaborators": 4,
        "created_user_id": 3,
        "project_status": "In progress",
        "open_seats": 4
    }
]
```
##### POST: localhost:8000/api/complete_project/
#
```sh
{
    "project_name": "Project Contributors",
    "status": "Completed"
}
```
##### POST: localhost:8000/api/collaboration_offer/
#
```sh
{
    "project_name": "Project Contributors"
}
```
##### POST: localhost:8000/api/handle_collaboration_offer/
#
```
{
    "contributor_name": "user3",
    "action": "accept"
}
```
##### POST: localhost:8000/api/logout/
#
#
# Thanks for reading!
