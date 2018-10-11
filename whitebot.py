import discord
import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from discord.ext import commands
import json
pending = []

# https://discordapp.com/oauth2/authorize?client_id=498889371030781952&scope=bot&permissions=268512342
# https://discordapp.com/oauth2/authorize?client_id=498964999918583820&scope=bot&permissions=268512306
now = datetime.datetime.now()
with open("stats.json") as f:
    stats = json.load(f)
with open("config.json") as f:
    config = json.load(f)

with open("config.json") as f:
    config = json.load(f)
    TOKEN = config['LOGIN'][0]['TOKEN']
    PREFIX = config['LOGIN'][0]['PREFIX']
    print(PREFIX)


client = commands.Bot(command_prefix=PREFIX)


def save_stats_backup(stats):
    with open("stats_backup.json", "w") as f:
        f.write(json.dumps(stats))


def save_stats(stats):
    with open("stats.json", "w") as f:
        f.write(json.dumps(stats))


@client.event
async def on_ready():
    print("Bot is Ready")


@client.event
async def on_message(message):
    await client.process_commands(message)


@client.event
async def on_member_remove(member):
    if member.mention in pending:
        pending.remove(member.mention)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name="pending")
    await client.add_roles(member, role)
    pending.append(member.mention)


@client.event
async def on_member_kick(member):
    role = discord.utils.get(member.server.roles,
                             name="pending")
    if member.mention in pending:
        time = now.strftime("%Y-%m-%d %H:%M")
        if role in member.roles:
            y = str(now.year)
            m = str(now.month)
            d = str(now.day)
            await client.kick(ctx.message.mentions[0])
            stats['Statistics'][0]['Applicants'] += 1
            stats['Statistics'][0]['Users Denied'] += 1
            stats['Applied'][0][str(member)] = time
            stats['Denied'][0][str(member)] = time
            stats['Data Applied'][0][y][0][m][0][d] += 1
            stats['Data Denied'][0][y][0][m][0][d] += 1
            save_stats(stats)
            await client.say("User " + member + " denied")
            pending.remove(member)


@client.event
async def on_member_ban(member):
    role = discord.utils.get(member.server.roles,
                             name="pending")
    if member.mention in pending:
        time = now.strftime("%Y-%m-%d %H:%M")
        if role in member.roles:
            y = str(now.year)
            m = str(now.month)
            d = str(now.day)
            await client.kick(ctx.message.mentions[0])
            stats['Statistics'][0]['Applicants'] += 1
            stats['Statistics'][0]['Users Denied'] += 1
            stats['Applied'][0][str(member)] = time
            stats['Denied'][0][str(member)] = time
            stats['Data Applied'][0][y][0][m][0][d] += 1
            stats['Data Denied'][0][y][0][m][0][d] += 1
            save_stats(stats)
            await client.say("User " + member + " denied")
            pending.remove(member)


@client.event
async def on_member_update(before, member):
    role = discord.utils.get(ctx.message.server.roles,
                             name="pending")
    if role in before.roles and role not in member.roles:

        if member.mention in pending:
            time = now.strftime("%Y-%m-%d %H:%M")
            y = str(now.year)
            m = str(now.month)
            d = str(now.day)
            await client.remove_roles(member, role)
            stats['Statistics'][0]['Applicants'] += 1
            stats['Statistics'][0]['Users Accepted'] += 1
            stats['Applied'][0][str(member)] = time
            stats['Accepted'][0][str(member)] = time
            stats['Data Applied'][0][y][0][m][0][d] += 1
            stats['Data Accepted'][0][y][0][m][0][d] += 1
            save_stats(stats)
            await client.say("User " + member + " accepted")
            pending.remove(member.mention)


@client.command(pass_context=True)
async def accept(ctx):
    if ctx.message.author.server_permissions.administrator:
        try:
            if ctx.message.mentions[0] in ctx.message.server.members:
                print("valid")
                channel = discord.utils.get(ctx.message.server.channels,
                                            id="498971465144860672")
                if ctx.message.channel == channel:
                    role = discord.utils.get(ctx.message.server.roles,
                                             name="pending")
                    member = ctx.message.mentions[0]
                    time = now.strftime("%Y-%m-%d %H:%M")
                    if role in member.roles:
                        y = str(now.year)
                        m = str(now.month)
                        d = str(now.day)
                        pending.remove(member)
                        await client.remove_roles(member, role)
                        stats['Statistics'][0]['Applicants'] += 1
                        stats['Statistics'][0]['Users Accepted'] += 1
                        stats['Applied'][0][str(member)] = time
                        stats['Accepted'][0][str(member)] = time
                        stats['Data Applied'][0][y][0][m][0][d] += 1
                        stats['Data Accepted'][0][y][0][m][0][d] += 1
                        save_stats(stats)
                        await client.say("User " + member + " accepted")
                    else:
                        await client.say("User Not pending...")
        except IndexError:
            await client.say("You must mention someone...")

    else:
        await client.say("You can't use this... Not admin...")
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def deny(ctx):
    if ctx.message.author.server_permissions.administrator:
        try:
            if ctx.message.mentions[0] in ctx.message.server.members:
                print("valid")
                save_stats_backup(stats)
                role = discord.utils.get(ctx.message.server.roles,
                                         name="pending")
                channel = discord.utils.get(ctx.message.server.channels,
                                            id="498971465144860672")
                if ctx.message.channel == channel:
                    member = ctx.message.mentions[0]
                    time = now.strftime("%Y-%m-%d %H:%M")
                    if role in member.roles:
                        y = str(now.year)
                        m = str(now.month)
                        d = str(now.day)
                        pending.remove(member)
                        await client.kick(ctx.message.mentions[0])
                        stats['Statistics'][0]['Applicants'] += 1
                        stats['Statistics'][0]['Users Denied'] += 1
                        stats['Applied'][0][str(member)] = time
                        stats['Denied'][0][str(member)] = time
                        stats['Data Applied'][0][y][0][m][0][d] += 1
                        stats['Data Denied'][0][y][0][m][0][d] += 1
                        save_stats(stats)
                        await client.say("User " + member + " denied")
                    else:
                        await client.say("User already denied him")
        except IndexError:
            await client.say("You must mention someone...")

    else:
        await client.say("You can't use this... Not admin...")
    await client.delete_message(ctx.message)


# @client.command(pass_context=True)
# async def ping(ctx):
#     now = datetime.datetime.utcnow()
#     diff = str(ctx.message.timestamp - now)
#     final = []
#     for i in diff:
#         if i == ":" or i == "0":
#             continue
#         else:
#             final.append(i)
#     final = ''.join(str(x) for x in final)
#     embed = discord.Embed(title="Ping: " '{:.2f}ms'.format(float(final)*100))
#     await client.say(embed=embed)


@client.command(pass_context=True)
async def showstats(ctx):
    if ctx.message.author.server_permissions.administrator:
        accepted = int(stats['Statistics'][0]['Users Accepted'])
        denied = int(stats['Statistics'][0]['Users Denied'])
        applied = int(stats['Statistics'][0]['Applicants'])
        try:
            acceptedP = (accepted/applied) * 100
            deniedP = (denied/applied) * 100
        except ZeroDivisionError:
            acceptedP = 0
            deniedP = 0
        embed = discord.Embed(title="Statistics",
                              colour=discord.Colour(0xf0d434))

        embed.add_field(name="Users Applied (total)",
                        value=applied)
        embed.add_field(name="Users Accepted (total/percentage)",
                        value="{} / {:.2f}%".format(accepted, acceptedP))
        embed.add_field(name="Users Denied (total/percentage)",
                        value="{} / {:.2f}%".format(denied, deniedP))

        await client.say(embed=embed)

    else:
        await client.say("You can't use this... Not admin...")
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def showaccepted(ctx):
    embed = discord.Embed(title="Statistics",
                          colour=discord.Colour(0xf0d434))
    embed.set_author(name="Users Accepted",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    for i in stats['Accepted'][0]:
        embed.add_field(name=i, value=stats['Accepted'][0][i])

    await client.say(embed=embed)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def showdenied(ctx):
    embed = discord.Embed(title="Users Denied",
                          colour=discord.Colour(0xf0d434))
    embed.set_author(name="Users Denied",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    for i in stats['Denied'][0]:
        embed.add_field(name=i, value=stats['Denied'][0][i])

    await client.say(embed=embed)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def showapplied(ctx):
    embed = discord.Embed(title="Users Applied",
                          colour=discord.Colour(0xf0d434))
    embed.set_author(name="Users Applied",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    for i in stats['Applied'][0]:
        embed.add_field(name=i, value=stats['Applied'][0][i])

    await client.say(embed=embed)
    await client.delete_message(ctx.message)


@client.command(pass_context=True)
async def showgraph(ctx, *args):
    """
    This command has 4 possible arguments:

    There are 3 types of graphs:
        Plot graphs
        Pie  graphs
        Bar  graph

    To make a plot graph:
            .showgraph [year] [month1] [month2] <plot>
        All of these arguments are optional but give different outputs.
        Example:
            .showgraph 2018         (Shows a plot graph of the whole year)
            .showgraph 2018 1 2     (Shows a plot graph of Jan and Feb)
            .showgraph 2018 1       (Shows a plot graph for Jan)
            .showgraph 2018 1 plot  (Same as before)
            .showgraph now          (Shows a plot graph for the current month)
    To make a Pie graph:
            .showgraph pie
        Pie graphs calculate using all the statistics, so there are no other options.

    To make a Bar graph:
            .showgraph [year] [month1] [month2] <bar>
        Bar graphs only work with more than one month, so you have to always specify the months
        unless you want to get a chart for the whole year.
        Example:
            .showgraph 2018 1 5 bar (Shows a bar graph for the months Jan through May)
            .showgraph 2018 bar     (Shows a bar graph for the whole year)

    Any questions or improvements? Talk to Kitty ^^ xoxo

    """
    m = 0
    m2 = 0
    try:
        arg1 = args[0]
        yr = arg1
        arg2 = args[1]
        m = arg2
        arg3 = args[2]
        m2 = arg3
        arg4 = args[3]
    except:
        pass
    if len(args) > 4:
        return await client.say("Too many arguments...")
    elif len(args) == 4:
        try:
            if int(arg1) > 2020 or int(arg1) < 2018 or int(arg2) > 12 or int(arg2) < 1 or int(arg3) > 12 or int(arg3) < 1:
                return await client.say("Expected year between 2018 and 2020. Read up on instructions.")
            else:
                if str(arg4).lower() == 'plot':
                    graphtype = 'plot'
                elif str(arg4).lower() == 'bar':
                    graphtype = 'bar'
                elif str(arg4).lower() == 'pie':
                    graphtype = 'pie'
        except TypeError:
            print(arg1, arg2, arg3, arg4)
            print(type(arg1), type(arg2), type(arg3), type(arg4))
            return await client.say("Expected a number. Read up on instructions")
    elif len(args) == 3:
        try:
            if int(arg1) > 2020 or int(arg1) < 2018 or int(arg2) > 12 or int(arg2) < 1:
                return await client.say("Expected year between 2018 and 2020 and a month between 1 and 12\n. Read up on instructions.")
            if str(arg3).lower() == 'plot':
                graphtype = 'plot'
                m2 = 0
            elif str(arg3).lower() == 'bar':
                graphtype = 'bar'
                m2 = 0
            elif str(arg3).lower() == 'pie':
                graphtype = 'pie'
                m2 = 0
            else:
                if int(arg3) > 12 or int(arg3) < 1:
                    return await client.say("Expected a month between 1 and 12 Read up on instructions.")
                graphtype = 'plot'
                m2 = 0
        except TypeError:
            return await client.say("Expected a month or a graph type. Read up on instructions")
        except UnboundLocalError:
            graphtype = 'plot'
            m2 = 0
    elif len(args) == 2:
        try:
            if int(arg1) > 2020 or int(arg1) < 2018:
                return await client.say("Expected year between 2018 and 2020\n. Read up on instructions.")

            if str(arg2).lower() == 'plot':
                graphtype = 'plot'
            elif str(arg2).lower() == 'bar':
                graphtype = 'bar'
            elif str(arg2).lower() == 'pie':
                graphtype = 'pie'
            else:
                if arg3:
                    if int(arg3) > 12 or int(arg3) < 1:
                        return await client.say("Expected a year between 2018 and 2020. Read up on instructions.")
                    else:
                        graphtype = 'plot'

        except TypeError:
            return await client.say("Expected a year between 2018 and 2020 or a graph type. Read up on instructions")
        except UnboundLocalError:
            graphtype = 'plot'
        except ValueError:
            if str(arg2).lower() == 'plot':
                graphtype = 'plot'
            elif str(arg2).lower() == 'bar':
                graphtype = 'bar'
            elif str(arg2).lower() == 'pie':
                graphtype = 'pie'
            else:
                graphtype = 'plot'
    elif len(args) == 1:
        try:
            if int(arg1) > 2020 or int(arg1) < 2018:
                return await client.say("Expected a year between 2018 and 2020. Read instructions")
            graphtype = 'plot'
            m = 1
            m2 = 12
            realmonth = 'January'
            realmonth2 = 'December'
        except TypeError:
            if str(arg1).lower() == 'plot':
                graphtype = plot
            elif str(arg1).lower() == 'bar':
                graphtype = 'bar'
            elif str(arg1).lower() == 'pie':
                graphtype = 'pie'
            elif str(arg1).lower() == 'now':
                yr = now.year
                m = now.month
                realmonth = now.strftime("%B")
                m2 = 0
            else:
                return await client.say("Expected a year between 2018 and 2020 or a graph type. Read up on instructions.")
        except ValueError:
            if str(arg1).lower() == 'plot':
                graphtype = 'plot'
            elif str(arg1).lower() == 'bar':
                graphtype = 'bar'
            elif str(arg1).lower() == 'pie':
                graphtype = 'pie'
            else:
                graphtype = 'plot'
    else:
        return await client.say("Type '{}help showgraph' if you are in doubt...".format(PREFIX))

    if m == "1":
        realmonth = "January"
    if m2 == "1":
        realmonth = "January"
    if m == "2":
        realmonth = "February"
    if m2 == "2":
        realmonth2 = "February"
    if m == "3":
        realmonth = "March"
    if m2 == "3":
        realmonth2 = "March"
    if m == "4":
        realmonth = "April"
    if m2 == "4":
        realmonth2 = "April"
    if m == "5":
        realmonth = "May"
    if m2 == "5":
        realmonth2 = "May"
    if m == "6":
        realmonth = "June"
    if m2 == "6":
        realmonth2 = "June"
    if m == "7":
        realmonth = "July"
    if m2 == "7":
        realmonth2 = "July"
    if m == "8":
        realmonth = "August"
    if m2 == "8":
        realmonth2 = "August"
    if m == "9":
        realmonth = "September"
    if m2 == "9":
        realmonth2 = "September"
    if m == "10":
        realmonth = "October"
    if m2 == "10":
        realmonth2 = "October"
    if m == "11":
        realmonth = "November"
    if m2 == "11":
        realmonth2 = "November"
    if m == "12":
        realmonth = "December"
    if m2 == "12":
        realmonth2 = "December"
    channel = ctx.message.channel
    bg_color = '#36393E'
    fg_color = 'white'
    if graphtype == "plot":
        if m2 == 0:
            x = []
            y = []
            print("m: ", m)
            print(m2)
            for i in stats['Data Applied'][0][str(yr)][0][str(m)][0]:
                x.append(int(i))
                y.append(stats['Data Applied'][0][str(yr)][0][str(m)][0][i])

            ax = plt.figure().gca()
            ax.plot(x, y)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.spines['bottom'].set_color('#36393E')
            ax.spines['top'].set_color('#36393E')
            ax.spines['right'].set_color('#36393E')
            ax.spines['left'].set_color('#36393E')
            ax.set_facecolor('#36393E')
            plt.xlabel('Days of the Month', color='white')
            plt.ylabel('Number of Applicants', color='white')
            plt.title('Applicant Data for {}, {}'.format(realmonth, yr), color='whitesmoke')
            plt.plot(x, y, color='whitesmoke')
            plt.savefig("plot.png", bbox_inches='tight', facecolor='#36393E')
            with open("plot.png", "rb") as f:
                await client.send_file(channel, f)
            plt.clf()
            plt.cla()
        else:
            if int(m) > int(m2):
                return await client.say("Wrong order of months")
            else:
                x = []
                y = []
                for j in range(int(m), int(m2)+1):
                    for i in stats['Data Applied'][0][str(yr)][0][str(j)][0]:
                        y.append(stats['Data Applied'][0][str(yr)][0][str(j)][0][i])
                        x.append(int(j))

                ax = plt.figure().gca()
                ax.plot(x, y)
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                ax.spines['bottom'].set_color('white')
                ax.spines['top'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.yaxis.label.set_color('white')
                ax.xaxis.label.set_color('white')
                ax.title.set_color('white')
                ax.set_facecolor('#36393E')
                plt.xlabel('Months', color='whitesmoke')
                plt.ylabel('Number of Applicants', color='white')
                plt.title('Applicant Data for {}, between {} and {}'.format(
                    yr, realmonth, realmonth2), color='white')
                plt.plot(x, y, color='whitesmoke')
                plt.savefig("plot.png", bbox_inches='tight', facecolor='#36393E')
                with open("plot.png", "rb") as f:
                    await client.send_file(channel, f)
                plt.clf()
                plt.cla()
    if graphtype == "pie":
        x = [stats['Statistics'][0]['Users Accepted']]
        y = [stats['Statistics'][0]['Users Denied']]
        slices = [x, y]
        activities = ["Accepted", "Denied"]
        cols = ['c', 'm']
        plt.title('Total Applicant Data')
        plt.pie(slices, labels=activities, colors=cols,
                startangle=90,
                shadow=True,
                explode=(0, 0),
                autopct='%1.1f%%')
        plt.savefig("pie.png", bbox_inches='tight', facecolor='#36393E')
        with open("pie.png", "rb") as f:
            await client.send_file(channel, f)
        plt.clf()
        plt.cla()
    if graphtype == "bar":
        print("M2: ", m2)
        if m2 != 0:
            accepted = []
            denied = []
            dates = []
            applied = []
            for j in range(int(m), int(m2)+1):
                for i in stats['Data Accepted'][0][str(yr)][0][str(j)][0]:
                    accepted.append(stats['Data Accepted'][0][str(yr)][0][str(j)][0][i])
                    dates.append(int(j))
            for j in range(int(m), int(m2)+1):
                for i in stats['Data Denied'][0][str(yr)][0][str(j)][0]:
                    denied.append(stats['Data Denied'][0][str(yr)][0][str(j)][0][i])
            for j in range(int(m), int(m2)+1):
                for i in stats['Data Applied'][0][str(yr)][0][str(j)][0]:
                    applied.append(stats['Data Applied'][0][str(yr)][0][str(j)][0][i])
            width = 0.35
            print(dates)
            ax = plt.figure().gca()
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.xticks(dates, dates)
            p1 = plt.bar(dates, accepted, width)
            p2 = plt.bar(dates, denied, width, bottom=denied)
            ax.set_facecolor('#36393E')
            plt.ylabel('Users', color='whitesmoke')
            plt.title('Users Accepted/Denied\nPer months: {} - {}'.format(realmonth,
                                                                          realmonth2), color='white')

            plt.legend((p1[0], p2[0]), ('Accepted', 'Denied '))
            plt.savefig("bar.png", bbox_inches='tight', facecolor='#36393E')
            with open("bar.png", "rb") as f:
                await client.send_file(channel, f)
            plt.clf()
            plt.cla()
        else:
            await client.say("For bar graph, you must specify 2 or more months")


@client.command(pass_context=True)
async def clear(ctx, number, age=None):
    number = int(number)
    counter = 0
    if number > 100 and age is None:
        secondcounter = number
        while secondcounter > 100:
            mgs = []
            number = int(number)
            async for x in client.logs_from(ctx.message.channel, limit=number):
                mgs.append(x)
            await client.delete_messages(mgs)
        if secondcounter > 0:
            mgs = []
            number = int(number)
            async for x in client.logs_from(ctx.message.channel, limit=number):
                mgs.append(x)
            await client.delete_messages(mgs)
        else:
            print("done cleaning of {} messages".format(number))

    elif number < 100 and age is None:
        mgs = []
        number = int(number)
        async for x in client.logs_from(ctx.message.channel, limit=number):
            mgs.append(x)
        await client.delete_messages(mgs)
    else:
        async for x in client.logs_from(ctx.message.channel, limit=number):
            if counter < number:
                await client.delete_message(x)
                counter += 1


@client.command(pass_context=True)
async def resetstats(ctx):
    save_stats_backup(stats)
    for k in range(2018, 2021):
        for j in range(1, 8, 2):
            for i in range(1, 32):
                stats['Data Applied'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Accepted'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Denied'][0][str(k)][0][str(j)][0][str(i)] = 0
    for k in range(2018, 2021):
        for j in range(4, 7, 2):
            for i in range(1, 31):
                stats['Data Applied'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Accepted'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Denied'][0][str(k)][0][str(j)][0][str(i)] = 0
    for k in range(2018, 2021):
        for j in range(8, 13, 2):
            for i in range(1, 32):
                stats['Data Applied'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Accepted'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Denied'][0][str(k)][0][str(j)][0][str(i)] = 0
    for k in range(2018, 2021):
        for j in range(9, 12, 2):
            for i in range(1, 32):
                stats['Data Applied'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Accepted'][0][str(k)][0][str(j)][0][str(i)] = 0
                stats['Data Denied'][0][str(k)][0][str(j)][0][str(i)] = 0
    for k in range(2018, 2021):
        for i in range(1, 32):
            stats['Data Applied'][0][str(k)][0]["2"][0][str(i)] = 0
            stats['Data Accepted'][0][str(k)][0]["2"][0][str(i)] = 0
            stats['Data Denied'][0][str(k)][0]["2"][0][str(i)] = 0

    for element in list(stats['Applied'][0]):
        del stats['Applied'][0][element]
    for element in list(stats['Denied'][0]):
        del stats['Denied'][0][element]
    for element in list(stats['Accepted'][0]):
        del stats['Accepted'][0][element]
    stats['Statistics'][0]['Applicants'] = 0
    stats['Statistics'][0]['Users Accepted'] = 0
    stats['Statistics'][0]['Users Denied'] = 0
    save_stats(stats)
client.run(TOKEN)
