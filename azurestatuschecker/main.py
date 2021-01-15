import json
import os
import time

from flask import Blueprint, render_template, current_app, session, redirect, url_for
from . import db
from flask_login import login_required, current_user
from mcstatus import MinecraftServer

import requests

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.status'))
    return render_template('index.html')


@main.route('/status')
@login_required
def status():
    try:
        server = MinecraftServer.lookup(os.environ['SERVER_IP_ADDRESS'])
        status = server.status()
    except:
        status = None

    return render_template('status.html', username=current_user.username, status=status)


@main.route('/start_server_post', methods=['POST'])
@login_required
def start_server_post():
    if 'LAST_START_REQUEST_TIME' not in session:
        session['LAST_START_REQUEST_TIME'] = 0

    # If there was a request to start the server for the past 10 minutes, then don't start it, as it should be taking some time to boot
    if time.time() - session['LAST_START_REQUEST_TIME'] < 60 * 10:
        return (
            json.dumps(
                {'message': "A request has already been sent in the last 10 minutes. Please wait for the server to boot."}),
            503,
            {'ContentType': 'application/json'}
        )

    r = requests.post(os.environ['AZURE_MC_START_WEBHOOK_URL'])
    response = (
        json.dumps(
            {'message': "Sent request to Azure runbook. The status of this response is the same as the response from Azure."}),
        r.status_code,
        {'ContentType': 'application/json'}
    )

    session['LAST_START_REQUEST_TIME'] = time.time()

    return response
