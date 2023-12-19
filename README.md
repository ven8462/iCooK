```markdown
# iCook - Recipe App

## Introduction

Welcome to iCook, your culinary companion in the digital world! This project, developed as part of my ALX End of Foundations Portfolio, is a recipe app that invites users to explore, save, and enjoy a variety of delightful recipes. Crafted with Python Flask, JavaScript, Jinja2, and fueled by the Edamam API, iCook seamlessly blends backend logic, frontend interactivity, and database management to create a flavorful user experience.

**Deployed Site:** [iCook App](#) *(www.icookapp.tech)*

**Final Project Blog Article:** [iCook Project Blog](#) *(replace with your blog article link)*

**Author(s) LinkedIn:**
- [Your Name](#) *(replace with author's LinkedIn profile link)*

## Technology Stack

### Frontend:
- HTML
- CSS
- JavaScript

### Backend:
- Flask (Microframework for Python)

### DevOps:
- Digital Ocean server for hosting
- .tech domain for online presence
- Nginx web server for handling HTTP requests
- Gunicorn application server for serving Flask application
- Certbot for SSL encryption
- UFW firewall for security

### Database:
- SQLITE for local development
- MYSQL for the server

## Architecture

The architecture of iCook follows a well-thought-out structure to enhance code organization. Here's an overview of the key components:

- **Application Logic (app folder):**
  - `static` and `templates`: Flask uses the 'static' folder to serve static assets (CSS, JS, and images) and the 'templates' folder for HTML templates.
  - **Python Modules:**
    - `errors.py`: Manages error logic and custom error pages.
    - `forms.py`: Flask forms to handle user input.
    - `__init__.py`: Marks the 'app' directory as a Python package.
    - `models.py`: Defines database models.
    - `routes.py`: Defines Flask routes and views.
  - **Configuration and Main Application File:**
    - `config.py`: Holds configuration settings for the Flask application.
    - `icook.py`: Main application module for the Flask application. Sets up Flask and provides utility for Flask shell.
  - **Auxiliary Directories:**
    - `migrations`: Contains database migration scripts.

- **Testing:**
  - `tests.py`: Test cases for the Flask application.

- **Documentation:**
  - `README.md`: Comprehensive information about the project.

## Getting Started

To set up and run the iCook project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ven8462/iCooK.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd iCook
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv myenv
   ```

4. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     myenv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source myenv/bin/activate
     ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Set up the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

7. **Run the Flask application:**
   ```bash
   python3 run.py
   ```

8. **Open your browser and savor the flavor at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).**

## Usage

1. **Search recipes on the homepage.**
2. **Click on a recipe card to view detailed information about the recipe.**
3. **Use the "Add to Favorites" feature to save recipes to your favorites.**
4. **Use the "Add to Shopping List" feature to add ingredients to your shopping list.**

## Deployment and Hosting

Ready to take iCook to the world? Follow these steps:

1. **Set up a Digital Ocean Droplet:**
   - Sign up for the GitHub Student Developer Pack (https://education.github.com/pack)
   - Create a new droplet.
   - Choose a distribution (e.g., Ubuntu).
   - Set up SSH access and log in to your Droplet from your local terminal.
   - Create a less privileged user and give them sudo privileges.
   - Set up SSH for the user by adding your public key into `.ssh`.
   - Exit and SSH into the droplet as the less privileged user.
   - Secure your server with UFW.

2. **Clone the repository:**
   ```bash
   git clone https://github.com/ven8462/iCooK.git
   ```

3. **Navigate to the project directory:**
   ```bash
   cd iCook
   ```

4. **Create a virtual environment:**
   ```bash
   python -m venv myenv
   ```

5. **Activate the virtual environment:**
   - **Windows:**
     ```bash
     myenv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source myenv/bin/activate
     ```

6. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

7. **Configure the application:**
   - Modify `config.py` to match the server configuration.

8. **Install, set up MYSQL, and upgrade the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

9. **Install and configure Nginx:**
   ```bash
   sudo apt-get install nginx
   ```

10. **Install and configure Gunicorn:**
    ```bash
    pip install gunicorn
    ```

11. **Set up SSL with Certbot:**
    - Follow Certbot instructions for your server. (https://gbeminiyi.hashnode.dev/installing-certbot-in-your-haproxy-load-balancer-server)

12. **Visit your domain:**
    [Your Domain](#)

## Acknowledgments

A special thank you to the following resources and individuals who played a pivotal role in the development of iCook:

### Resources:
- [The Flask Mega Tutorial](#)
- [Digital Ocean Gunicorn Installation](#)
- [Digital Ocean Nginx Installation](#)
- [Digital Ocean Server Setup](#)
- [Flask Documentation](#)
- [chatGPT](#)

### Individuals:
- **Friend - [Wanjang'i Gituku]:** Appreciation for constructive feedback and collaborative efforts that significantly enhanced the project's quality.
- **Friend - [Victor ]:** A personal thank you for always showing up to help me debug my code and find solutions.
- I also want to acknowledge [ALX](https://www.alxafrica.com/) for giving me this opportunity to learn a show case my skills by building this project. The community is so supportive and inspiring.

iCook is truly a labor of love, and none of it would have been possible without the incredible support from these amazing resources and individuals. A heartfelt thank you for your guidance, encouragement, and patience that contributed to  every byte of iCook's development! 🌟💻🍲