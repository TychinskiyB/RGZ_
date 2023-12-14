from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import users, medicines
from flask_login import login_user, login_required, current_user, logout_user


app = Flask(__name__)
