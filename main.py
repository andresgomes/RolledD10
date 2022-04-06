from flask import Flask, render_template, request, redirect, session, flash, url_for
import discord
import asyncio
import os
import random

app = Flask(__name__)

client = discord.Client()
deffaut_difficult = 6

def simple_result(input_int):
    result_dice = []
    for i in range(input_int):
        result_dice.append(random.randrange(1, 11))
    result_dice.sort(reverse=True)
    return result_dice

def right_result(input_int, difficult):
    hits = 0
    result_dices = []
    for i in range(input_int):
        dice = random.randrange(1, 11)
        if dice >= difficult:
            hits += 1
        if dice == 1:
            hits -= 1
        result_dices.append(dice)
    result_dices.sort(reverse=True)
    return f'{hits} <- {result_dices}'

def damage_block_result(input_int):
    result_dices = []
    hits = 0
    for i in range(input_int):
        dice = random.randrange(1, 11, 1)
        if dice >= 6:
            hits += 1
        result_dices.append(dice)
    result_dices.sort(reverse=True)
    return f'{hits} <- {result_dices}'

#main web page
@app.route('/')
def index():
    return render_template("index.html")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#main discord bot
@client.event
async def on_message(message):
    content = str(message.content).lower()
    author = message.author.name
    mention = message.author.mention
    #If just int roll 10
    if content.isnumeric():
        result = simple_result(int(content))
        await message.reply(str(result))
        #await message.channel.response(str(result))

    #If start with 'a', count the hits in normal tests with difficult 6 if start with 'ha', count de damage and block
    elif content.startswith('a') or content.startswith('ha'):
        qtd_dices = ''.join([i for i in content if i.isdigit()])
        result = ''
        if content[1].isdigit():
            result = right_result(int(qtd_dices), deffaut_difficult)
        elif content[2].isdigit():
            result = damage_block_result(int(qtd_dices))
        await message.reply(result)

    #If start with hd(int)a, use int to apply a another difficult
    elif content.startswith('hd'):
        difficult = int(content[2])
        new_input_client = content[4: ]
        qtd_dices = int(new_input_client)
        result = right_result(qtd_dices, difficult)
        await message.reply(result)

#main web page
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    client.run(os.getenv('TOKEN'))

