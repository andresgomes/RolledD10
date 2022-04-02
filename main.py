import discord
import asyncio
import os
import random

client = discord.Client()
defaut_difficult = 6

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

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    input_client = str(message.content).lower()
    #If just int roll 10
    if input_client.isnumeric():
        result = simple_result(int(input_client))
        await message.channel.send(str(result))

    #If start with 'a', count the hits in normal tests with difficult 6 if start with 'ha', count de damage and block
    elif input_client.startswith('a') or input_client.startswith('ha'):
        qtd_dices = ''.join([i for i in input_client if i.isdigit()])
        result = ''
        if input_client[1].isdigit():
            result = right_result(int(qtd_dices), defaut_difficult)
        elif input_client[2].isdigit():
            result = damage_block_result(int(qtd_dices))
        await message.channel.send(result)

    #If start with hd(int)a, use int to apply a another difficult
    elif input_client.startswith('hd'):
        difficult = int(input_client[2])
        new_input_client = input_client[4: ]
        qtd_dices = int(new_input_client)
        result = right_result(qtd_dices, difficult)
        await message.channel.send(result)

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))
