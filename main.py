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


def right_result(qtd_dices, difficult):
    hits = 0
    result_dices = []
    for i in range(qtd_dices):
        dice = random.randrange(1, 11)
        if dice >= difficult:
            hits += 1
        if dice == 1:
            hits -= 1
        result_dices.append(dice)
    hits = 0 if hits < 0 else hits
    result_dices.sort(reverse=True)
    return f'{hits}  ⟵ {result_dices} \n'


def damage_block_result(input_int, difficult):
    result_dices = []
    hits = 0
    for i in range(input_int):
        dice = random.randrange(1, 11, 1)
        if dice >= difficult:
            hits += 1
        result_dices.append(dice)
    result_dices.sort(reverse=True)
    return f'{hits}  ⟵ {result_dices} \n'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# main discord bot
@client.event
async def on_message(message):
    content = str(message.content).lower()
    # author = message.author.name
    # mention = message.author.mention
    # If just int roll 10
    result = ''
    if content.isnumeric():
        result = simple_result(int(content))
        await message.reply(str(result))
        # await message.channel.response(str(result))

    # If start with 'a', count the hits in normal tests with difficult 6 if start with 'h', count de damage and block
    elif content.startswith('a') or content.startswith('h'):
        qtd_dices = ''.join([i for i in content if i.isdigit()])
        if content[0] == 'a':
            result = right_result(int(qtd_dices), deffaut_difficult)
        elif content[0] == 'h':
            result = damage_block_result(int(qtd_dices), deffaut_difficult)
        await message.reply(result)

    # If start with sa(int)a, use int to apply a another difficult
    elif content.startswith('sa'):
        difficult = int(content[2])
        qtd_dices = int(content[4:])
        if content[3] == 'a':
            result = right_result(qtd_dices, difficult)
        if content[3] == 'b':
            result = damage_block_result(qtd_dices, difficult)
        await message.reply(result)

    # if start with #, roll more tests
    elif content.startswith('#'):
        position = 1
        qtd_rolls = ''
        while content[position].isdigit():
            qtd_rolls += content[position]
            position += 1
        qtd_rolls = range(int(qtd_rolls))
        content = content[position:]
        if content.startswith('a') or content.startswith('h'):
            qtd_dices = ''.join([i for i in content if i.isdigit()])
            result = ''
            if content[0] == 'a':
                for i in qtd_rolls:
                    result += right_result(int(qtd_dices), deffaut_difficult)
            elif content[0] == 'h':
                for i in qtd_rolls:
                    result += damage_block_result(int(qtd_dices), deffaut_difficult)
            await message.reply(result)

        elif content.startswith('sa'):
            difficult = int(content[2])
            qtd_dices = int(content[4:])
            if content[3] == 'a':
                for i in qtd_rolls:
                    result += right_result(qtd_dices, difficult)
            if content[3] == 'b':
                for i in qtd_rolls:
                    result += damage_block_result(qtd_dices, difficult)
            await message.reply(result)


# main web page
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    # app.run()
    client.run(os.getenv('TOKEN'))
