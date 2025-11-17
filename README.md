# 📌 Employee Task Management System

*A Full-Stack Application with FastAPI, JWT Auth & Modern Frontend UI*

---

## 📖 Overview

This project is a complete **Employee–Task Management System** built with a **FastAPI backend** and a **modern, animated frontend**.
Users can **sign up, log in, manage employees, assign tasks, and update task statuses**, all protected through **JWT authentication**.

---

# 🛠️ Tech Stack Used

### **Backend**

* **FastAPI** (primary framework)
* **SQLAlchemy** (ORM)
* **Pydantic** (data validation)
* **JWT (JSON Web Tokens)** for authentication
* **SQLite / MySQL** (database support)
* **Uvicorn** (server)

### **Frontend**

* **HTML5**
* **CSS3** (Dark theme, animated flip-card UI)
* **Vanilla JavaScript (Fetch API)**
* **Responsive layout**

### **Tools**

* Git & GitHub
* VS Code
* Python 3.10+

---

# ⚙️ Setup Instructions

## 🖥️ 1. Clone the Repository

```bash
git clone https://github.com/SowndaryaS0201/employee_task_api_modified.git
cd employee_task_api_modified
```

---

# 🛠️ Backend Setup (FastAPI)

## 🔹 2. Create & Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

## 🔹 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🔹 4. Run Backend Server

```bash
uvicorn backend.main:app --reload
```

Backend available at:

```
http://127.0.0.1:8000
```

Swagger docs:

```
http://127.0.0.1:8000/docs
```

---

# 🌐 Frontend Setup

No installation needed.
Open:

```
frontend/index.html
```

The frontend communicates with the backend through:

```js
const API_BASE = "http://127.0.0.1:8000";
```

Update the URL if you deploy backend online.

---

# 🔐 Authentication Flow

| Step | Description                                               |
| ---- | --------------------------------------------------------- |
| 1    | User signs up                                             |
| 2    | User logs in                                              |
| 3    | Backend returns a JWT token                               |
| 4    | Token stored in `localStorage`                            |
| 5    | All protected calls send: `Authorization: Bearer <token>` |

---

# 📋 Core Features

### 👤 **User Authentication**

* Signup + Login
* JWT-secured endpoints

### 👥 **Employee Management**

* Add Employee
* View All Employees
* Update Employee
* Delete Employee

### 🗒️ **Task Management**

* Assign tasks to employees
* Edit & update task status
* Delete tasks

### 🎨 **Frontend**

* Animated flip-card login/signup
* Dark-themed UI
* Responsive layout
* Clean user-friendly design

---

# 🖼️ Screenshots


### **Login / Signup**

<img width="2218" height="1280" alt="image" src="https://github.com/user-attachments/assets/fb7a184d-531a-4601-a6e4-2eec743fe6f1" />

<img width="2204" height="1222" alt="image" src="https://github.com/user-attachments/assets/aa243982-6373-429c-97d9-fb2fc926ca69" />



### **Home Dashboard**

<img width="2209" height="1255" alt="image" src="https://github.com/user-attachments/assets/88e668c6-eb21-49a2-9ec1-1580db15e9f0" />


### **Employee List**

<img width="2192" height="1246" alt="image" src="https://github.com/user-attachments/assets/74669cb3-df44-4377-95a1-9fa62660de3b" />

<img width="2190" height="1264" alt="image" src="https://github.com/user-attachments/assets/be57cac1-aa8b-436f-84a5-36213b9accfe" />

### **End Points**

<img width="2177" height="1257" alt="image" src="https://github.com/user-attachments/assets/99b13d18-e8b8-498c-b38d-43786bc006ba" />


---

# 📌 Assumptions

* Each employee may have multiple tasks.
* A user must be logged in to access employee and task endpoints.
* Backend returns structured JSON for easy frontend parsing.
* Database is SQLite for local testing (can be swapped with MySQL/Postgres).

---

# ⭐ Features Implemented

* Modern **flip-card animation** for auth UI
* Clean **dark theme** designed manually
* Token stored in `localStorage` with redirect to `home.html`
* Organized backend structure following best practices (`routers/`, `schemas/`, `models/`)
* CORS-ready backend (easy deployment)

---



# 👩‍💻 Author

**S. Sowndarya**
4th Year IT | Full-Stack Developer | FastAPI Enthusiast
GitHub: **[https://github.com/SowndaryaS0201](https://github.com/SowndaryaS0201)**

