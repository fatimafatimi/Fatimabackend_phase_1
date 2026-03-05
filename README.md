# FastAPI Parameters & Request Handling Examples

This project contains several example Python files demonstrating how to handle different types of data in **FastAPI**. Each file focuses on a specific concept such as **path parameters, query parameters, request bodies, headers, cookies, and forms**.

These examples help understand how FastAPI processes incoming requests and validates data using **Pydantic models and type hints**.

---

# Project Files

## 1. `path_parameter.py`

This file demonstrates how **path parameters** work in FastAPI.

### Concepts Covered

* Path parameters with types
* Automatic data conversion
* Data validation
* Parameter ordering
* Numeric validation
* Predefined values using `Enum`
* Handling paths inside parameters
* OpenAPI documentation generation

### Key Points

* Path parameters are values included directly in the URL.
* FastAPI automatically converts and validates their types.
* Using `Enum` allows restricting values to predefined options.
* `Path()` can be used for additional validation like minimum or maximum values.

Example URL:

/items/10

---

## 2. `query_parameter.py`

This file demonstrates **query parameters**, which are values passed after the `?` in a URL.

### Concepts Covered

* Default query parameters
* Optional query parameters
* Required query parameters
* Query parameter type conversion
* Combining path and query parameters

### Key Points

* Query parameters are optional by default.
* FastAPI automatically converts them to the declared data type.
* Validation and descriptions can be added using `Query()`.

Example URL:

/items/?skip=5&limit=10

---

## 3. `request_body.py`

This file explains how to send and process **request bodies** using **Pydantic models**.

### Concepts Covered

* Importing and using `BaseModel`
* Creating request body schemas
* Request body validation
* Combining request body with path parameters
* Combining request body with path and query parameters
* Request body without Pydantic

### Key Points

* Pydantic models define the structure of request data.
* FastAPI automatically validates incoming JSON.
* Request bodies are commonly used in **POST**, **PUT**, and **PATCH** requests.

Example JSON Request Body:

{
"name": "Laptop",
"description": "Gaming laptop",
"price": 1500
}

---

## 4. `form.py`

This file demonstrates how to handle **HTML form data**.

### Concepts Covered

* Importing and using `Form`
* Declaring form fields
* Optional form parameters
* Pydantic validation for form data
* Forbidding extra form fields

### Key Points

* Form data is sent using `application/x-www-form-urlencoded`.
* FastAPI uses `Form()` to extract form fields.
* Form fields are commonly used for **login forms and user registration**.

Example Form Data:

username=admin
password=12345

---

## 5. `cookie.py`

This file shows how to read **cookies** sent by the client.

### Concepts Covered

* Importing and using `Cookie`
* Declaring cookie parameters
* Optional cookies
* Using Pydantic models with cookies
* Forbidding extra cookies

### Key Points

* Cookies are small pieces of data stored on the client browser.
* They are often used for **sessions, authentication, and tracking**.
* FastAPI automatically extracts cookies using `Cookie()`.

Example Cookie:

session_id=abc123

---

## 6. `header.py`

This file demonstrates how to work with **HTTP headers** in FastAPI.

### Concepts Covered

* Importing `Header`
* Declaring header parameters
* Automatic type conversion
* Duplicate headers
* Header validation using Pydantic models
* Forbidding extra headers
* Disabling underscore conversion

### Key Points

* Headers provide metadata about the request.
* FastAPI converts underscores to hyphens automatically (e.g., `user_agent` → `User-Agent`).
* Multiple headers with the same name can be captured as lists.

Example Header:

User-Agent: Mozilla/5.0

---

# Running the Project

Run any file using **Uvicorn**:

```bash
uvicorn filename:app --reload
```

Example:

```bash
uvicorn path_parameter:app --reload
```

---

# API Documentation

FastAPI automatically generates interactive documentation.

### Swagger UI

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### ReDoc

[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These interfaces allow you to test endpoints directly from the browser.

---

# Technologies Used

* **Python**
* **FastAPI**
* **Pydantic**
* **Uvicorn**

---


