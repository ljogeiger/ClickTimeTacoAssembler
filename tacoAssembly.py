# Author: Lukas Geiger
# Date: October 5, 2019
# Description: Clicktime Application Taco Assembly App

from flask import Flask, render_template, redirect, request, flash, url_for, session, jsonify
import json
import requests
import sys
import random

app = Flask(__name__)

app.secret_key = '772f2253fd3a4c2524a93c70aefeac2e'
base_url = "https://ct-tacoapi.azurewebsites.net"

created_taco = {"shells": "", "baseLayers": "",
                "mixins": "", "condiments": "", "seasonings": ""}
tacos = []

"""
1 - Welcome: User arrives at welcome page and clicks 'Get Started' or 'Random Taco'
2 - Taco Assembly: Launch Taco Assembly Workflow (Guides the user through a series of options)
3 - Shopping Cart: Show final product in a window and allow user to delete item
    This step uses global variables to track items in user's shopping cart which creates problems when the
    cart page is refreshed. To make this more stable I would use SQLite or some other SQL database to store user's tacos.
4 - Checkout: thank the user and says goodbye
"""


@app.route('/', methods=['GET'])
def main():
    tacos.clear()
    return render_template('index.html')

# Makes call to url for specific item requested


def getItemsFromURL(item):
    return_list = []
    data = requests.get(base_url + "/" + item)  # Get shells from url
    data_json = data.json()
    for item in data_json:
        return_list.append(item['name'])
    if not return_list:
        # This will still allow the user to continue selecting a taco without a shell
        return_list = ["Sorry we are all out of " + item + "!"]
    return return_list

# Initialize the Taco Assembly workflow by prompting the user to pick a shell.


@app.route('/addShell', methods=['GET', 'POST'])
def addShell():
    if request.method == 'POST':
        created_taco['shells'] = request.form["user_choice"]
        return redirect(url_for('addBase'))
    if request.method == 'GET':
        response = getItemsFromURL("shells")
        return render_template('shell.html', response=response)


@app.route('/addBase', methods=['GET', 'POST'])
def addBase():
    if request.method == 'POST':
        created_taco['baseLayers'] = request.form.getlist("base")
        if not len(created_taco['baseLayers']) == 1:
            flash('Please select one base layer', 'danger')
            return redirect(url_for('addBase'))
        return redirect(url_for('addMixins'))
    if request.method == 'GET':
        response = getItemsFromURL("baseLayers")
        return render_template('base.html', response=response)

# Allows for 1-2 mixins
# Assumption: user is not allowed to pick 0 mixins

@app.route('/addMixins', methods=['GET', 'POST'])
def addMixins():
    if request.method == 'POST':
        created_taco['mixins'] = request.form.getlist("mixins")
        if len(created_taco['mixins']) > 2 or len(created_taco['mixins']) < 1:
            flash('Please select a maximum of two mixins and minimum of 1', 'danger')
            return redirect(url_for('addMixins'))
        return redirect(url_for('addCondiments'))
    if request.method == 'GET':
        response = getItemsFromURL("mixins")
        return render_template('mixin.html', response=response)

# Allows for more than 1-3 condiments
# Assumption: user is not allowed to pick 0 condiments

@app.route('/addCondiments', methods=['GET', 'POST'])
def addCondiments():
    if request.method == 'POST':
        created_taco['condiments'] = request.form.getlist("condiments")
        if len(created_taco['condiments']) > 3 or len(created_taco['condiments']) < 1:
            flash(
                'Please select a maximum of three condiments and a minimum of 1', 'danger')
            return redirect(url_for('addCondiments'))
        return redirect(url_for('addSeasonings'))
    if request.method == 'GET':
        response = getItemsFromURL("condiments")
        return render_template('condiments.html', response=response)


@app.route('/addSeasonings', methods=['GET', 'POST'])
def addSeasonings():
    if request.method == 'POST':
        created_taco['seasonings'] = request.form["user_choice"]
        return redirect(url_for('reviewCart', index=-2))
    if request.method == 'GET':
        response = getItemsFromURL("seasonings")
        return render_template('seasoning.html', response=response)


@app.route('/reviewCart/<index>', methods=['GET'])
def reviewCart(index):
    if int(index) >= 0:
        del tacos[int(index) - 1]
    elif int(index) == -1:
        taco = "You selected a taco with " + created_taco["shells"] + " shell with a base of " + created_taco["baseLayers"] + ". Your mixins are " + \
            created_taco["mixins"] + " with condiments of " + created_taco["condiments"] + \
            " and seasoning of " + created_taco["seasonings"] + "."
        tacos.append(taco)
    else:
        print(created_taco)
        if created_taco["shells"]:
            if len(created_taco["mixins"]) > 1 and len(created_taco["condiments"]) > 1:
                taco = "You selected a taco with " + created_taco["shells"] + " shell with a base of " + created_taco["baseLayers"][0] + ". Your mixins are " + \
                    " and ".join(created_taco["mixins"]) + " with condiments of " + " and ".join(created_taco["condiments"]) + \
                    " and seasoning of " + created_taco["seasonings"] + "."
            elif len(created_taco["mixins"]) > 1 and len(created_taco["condiments"]) == 1:
                taco = "You selected a taco with " + created_taco["shells"] + " shell with a base of " + created_taco["baseLayers"][0] + ". Your mixins are " + \
                    " and ".join(created_taco["mixins"]) + " with condiments of " + created_taco["condiments"][0] + \
                    " and seasoning of " + created_taco["seasonings"] + "."
            elif len(created_taco["mixins"]) == 1 and len(created_taco["condiments"]) > 1:
                taco = "You selected a taco with " + created_taco["shells"] + " shell with a base of " + created_taco["baseLayers"][0] + ". Your mixins are " + \
                    created_taco["mixins"][0] + " with condiments of " + " and ".join(created_taco["condiments"]) + \
                    " and seasoning of " + created_taco["seasonings"] + "."
            else:
                taco = "You selected a taco with " + created_taco["shells"] + " shell with a base of " + created_taco["baseLayers"][0] + ". Your mixins are " + \
                    created_taco["mixins"][0] + " with condiments of " + created_taco["condiments"][0] + \
                    " and seasoning of " + created_taco["seasonings"] + "."
        else:
            taco = "No shell selected"

        tacos.append(taco)
    return render_template('cart.html', response=tacos)

# Selects random taco ingredients.
# Assumption: only required to generate a random taco with one ingredient of each item


@app.route('/randomTaco', methods=['GET'])
def randomTaco():
    for key in created_taco.keys():
        items = getItemsFromURL(key)
        random_int = random.randint(0, len(items) - 1)
        created_taco[key] = items[random_int]
    return redirect(url_for('reviewCart', index=-1))


@app.route('/thankYou', methods=['GET'])
def thankYou():
    return render_template('thankYou.html')


if __name__ == '__main__':
    app.run(host='localhost', debug="true")
