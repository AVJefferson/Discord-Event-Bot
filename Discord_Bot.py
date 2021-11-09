# MODULES TO IMPORT
import discord as D
import os

# TOKEN PASSWORD FOR ACCESSING DISCORD BOT
TOKEN = ""
with open("token", 'r') as f:
    TOKEN = f.readline()

# TEXT REPLACE DATABASE
mdict = {
    'endl': '\n',
    'PREFIX': '!!',
    'PREFIX_len': 2,
    'hourglass': '⏳',
    'exclamation': '❗',
    'error': '⚠',
    'question': '❓',
    'tick': '✅',
    'confused': '😕'
}


def update_prefix(p):
    mdict['PREFIX'] = p
    mdict['PREFIX_len'] = len(p)
    return


def update_dict(m):
    global mdict
    if isinstance(m, D.message.Message):
        mdict.update(
            user=m.author.mention
        )
    return


# COMMAND DATABASE
f = open('list/cmd.list', 'r')
cmdlst = set(cmds[:-1] for cmds in f.readlines())
f.close()


def update_cmd():
    f = open('list/cmd.list', 'r')
    global cmdlst
    cmdlst = set(cmds[:-1] for cmds in f.readlines())
    f.close()
    return


def add_cmd(cmd):
    f = open('list/cmd.list', 'a')
    f.write(cmd + '\n')
    cmdlst.add(cmd)
    f.close()
    return


# PERMISSION DATABASE


# ROLE DATABASE


# DISCORD CLIENT
client = D.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    return


@client.event
async def on_message(message):
    # Disregard self message
    if message.author == client.user:
        return
    msg = message.content

    # Check if the sent message is a command
    if not msg.startswith(mdict['PREFIX']):
        return

    # Command Received
    await message.add_reaction('⏳')

    # Extract Command and Attributes
    cmd = tuple(msg[mdict['PREFIX_len']:].lower().split())
    l = len(cmd)

# COMMAND INTERPRETER

    # Error if only the PREFIX is sent
    if not cmd:
        await message.add_reaction('😕')
        return

    # COMMAND IN LIBRARY
    if cmd[0] in cmdlst:
        # Check is command is defined
        try:
            f = open('cmds/' + cmd[0], 'r')
            task = f.readlines()

            if not task:
                await message.reply(cmd[0] + " not defined")
                await message.add_reaction('❗')
                return

        except FileNotFoundError:
            await message.reply(cmd[0] + " not defined")
            await message.add_reaction('❗')
            return
        finally:
            f.close()

        # Updating Dictionary Contents
        update_dict(message)

        # TEXT ONLY COMMANDS

        if(task[0][:-1] == "text"):
            await message.reply("".join(task[1:-1]))

        elif(task[0][:-1] == "ftext"):
            await message.reply("".join(task[1:-1]).format(**mdict))

        # HELP
        elif(task[0][:-1] == "help"):

            # Common help
            if l == 1:
                await message.reply("Available Commands\n" + str(cmdlst) + "\n\n" + "".join(task[1:]).format(**mdict))

            # Specific help
            elif l == 2:
                # Check is command is defined
                try:
                    f = open('cmds/' + cmd[1], 'r')
                    task = f.readlines()

                    if not task:
                        await message.reply(cmd[1] + " not defined")
                        await message.add_reaction('❗')
                        return

                    await message.reply(task[-1].format(**mdict))
                except FileNotFoundError:
                    await message.reply(cmd[1] + " not defined")
                    await message.add_reaction('❗')
                    return
                finally:
                    f.close()

            # Extra arguments
            else:
                await message.reply("Extra Arguments")
                await message.add_reaction('⚠')
                return

        # EXECUTABLE CONTENT
        elif task[0][:-1] == "exec":

            # Status list used to return messages.
            # status[0]
            #   0 == Error
            #   1 == Reaction
            #   2 == Reply and Reaction
            status = [0]

            # Checking allowed argument range
            argmin = int(task[1][:-1])
            argmax = int(task[2][:-1])

            if l < argmin:
                await message.reply("Insufficient Arguments")
                await message.add_reaction('⚠')
                return
            elif l > argmax:
                await message.reply("Extra Arguments")
                await message.add_reaction('⚠')
                return

            # Execute Code Block
            try:
                exec("".join(task[3:-1]))
            except:
                status = [0]

            # Code execution failed
            if status[0] == 0:
                await message.reply("Error Executing")
                await message.add_reaction('❗')
                return

            # Reporting Result
            if status[0] == 1:
                await message.add_reaction(mdict[status[1]])
            elif status[0] == 2:
                await message.reply(status[1])
                await message.add_reaction(mdict[status[2]])
            return

        # COMMAND COMPLETED SUCCESSFULLY
        await message.add_reaction('✅')
        return

    # COMMAND NOT IN LIBRARY
    else:
        await message.add_reaction('❓')
        return


# DISCORD BOT START
client.run(TOKEN)
