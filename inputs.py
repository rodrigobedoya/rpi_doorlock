from flask import Flask, render_template, session, request, jsonify, Response, redirect,url_for
from sqlalchemy import and_

from model import entities
from database import connector
import json
import datetime

from server import addEvent

now = datetime.datetime.utcnow()

while True:
    input_password = input()
    addEvent(input_password)
