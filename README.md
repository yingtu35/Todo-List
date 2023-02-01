git status

 A basic CRUD todo list application

## **Todo-List** app let you write down things to do.

### Description
Todo-List is a web application that builts on React and FastAPI framework.
You can create, read, update, and delete any list items in your todo list.

### Features

#### User Account system (only for v2.0)

#### Todo List


### How Todo-List is created 
Todo-List mainly consists of several parts listed below:
1. Fast API: Backend framework written in Python
	- Use SQLite for database management system
	- Provide REST APIs for the fronetend to communicate
	- Handle basic CRUD operations, user authentication
2. React: Frontend JavaScript framework
	- Create a single-page application (SPA)
	- Interact with user inputs such as text input and mouseclick
	- Fetch requests to the backend on user's events
3. Chakra UI: A modular components library to build and style React applications
4. alembic: A database migrations toolkit for Python
	
## How to Use Todo-List

### 1. Clone the repository, and navigate to the project directory (v1.0 or v2.0)
```shell
cd v1.0
```
or
```shell
cd v2.0
```

### 2. Install Required Python Modules

```shell
pip install -r requirements.txt
```
### 3. [Install Node.js](https://nodejs.org/en/)

### 4. Install All Node Modules for Todo-List
Navigate to the `frontend` folder
```shell
cd frontend
```
Then install the depedencies
```shell
npm i
```
### 5. Run the Frontend Server
```shell
npm start
```

### 6. Run the Backend Server
Navigate back to the `backend` folder
```shell
cd ../backend
```
Run `main.py` to start the backend server
```shell
python main.py
```

## Credits (to change)
Thanks [FastAPI](https://fastapi.tiangolo.com/) for the comprehensive documentation.\
Also huge thanks to [Tech With Tim](https://www.techwithtim.net/) and [Web Dev Simplified](https://www.youtube.com/channel/UCFbNIlppjAuEX4znoulh0Cw) for amazing videos about React usage.

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)