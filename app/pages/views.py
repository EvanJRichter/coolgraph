from app.app_and_db import app, db
from app.pages.models import Trade
from datetime import datetime
from flask import jsonify, render_template, redirect, request, url_for

import requests

base_url = "https://api.twitter.com/1.1/{0}"

@app.route('/')
def index():
  return render_template('pages/home_page.html')

@app.route('/api/<string:year>/<string:from_team>/<string:to_team>/')
def team_details(year, from_team, to_team):
  trades = Trade.query.filter(Trade.year == year).filter(Trade.from_team == from_team).filter(Trade.to_team == to_team).all()
  json_trades = []
  for trade in trades:
    json_trades.append(trade.serialize())
  return jsonify(trades=json_trades)

@app.route('/api/<string:year>/<string:team>/')
def complete_team_details(year, team):
  from_trades = Trade.query.filter(Trade.year == year).filter(Trade.from_team == team).all()
  to_trades = Trade.query.filter(Trade.year == year).filter(Trade.to_team == team).all()
  json_to_trades = []
  json_from_trades = []
  for trade in to_trades:
    json_to_trades.append(trade.serialize())
  for trade in from_trades:
    json_from_trades.append(trade.serialize())
  return jsonify(from_trades=json_from_trades, to_trades=json_to_trades)

@app.route('/api/transaction/<string:transaction_id>/')
def get_transaction_details(transaction_id):
  trades = Trade.query.filter(Trade.transaction_id == transaction_id).all()
  json_trades = []
  for trade in trades:
    json_trades.append(trade.serialize())
  return jsonify(trades=json_trades)

@app.teardown_appcontext
def shutdown_session(exception=None):
  db.remove()