import os
import discord
from discord.ext import commands
from connect_to_sheets import Sheets

my_secret = os.environ['DISCORD_TOKEN']
TOKEN = my_secret

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!ts ')

sheets = Sheets()
sheets.save_df_locally()

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.errors.CheckFailure):
#        await ctx.send('You do not have the correct role for this command.')


@bot.command(name='list', help='Displays all items.')
async def list(context, focus='item', sort='asc'):
  df = sheets.get_df_data()

  asc_value = True
  if (sort == 'desc' and sort != 'asc' and sort != ''):
    asc_value = False
  elif (sort == 'asc'):
    asc_value = True
  else:
    await context.send('Hmmm, the sorting value feels a little off: (' + sort +
                       ')')
    return

  if (focus == 'item'):
    focus = 'Item'
  elif (focus == 'price'):
    focus = 'CityPrice'
  else:
    await context.send('Hmmm, the focus value feels a little off: (' + focus +
                       ')')
    return

  df = df.sort_values(by=focus, ascending=asc_value)

  embed = discord.Embed(title="List of items",
                        description="Here is all of the available items.")

  for index, row in df.iterrows():
    embed.add_field(name=row['Item'],
                    value='City price: ' + str(row['CityPrice']),
                    inline=True)

    if (len(embed.fields) > 23):
      await context.send(embed=embed)

      embed = discord.Embed(title="List of items",
                            description="Here is all of the available items.")

  await context.send(embed=embed)


@bot.command(name='update', help='Updates the list.')
@commands.has_role('admin')
async def update(context):
  response = 'Oh, this will take just a moment'
  await context.send(response)
  sheets.save_df_locally()
  await context.send('...and done!')


@bot.command(name='craft', help='Shows how to craft items.')
async def craft(context, item, count=1):
  item = item.capitalize()
  df = sheets.get_df_data()

  embed = discord.Embed(title=str(count) + ' ' + item)

  for i in range(1, 4):
    req = str(df['Req' + str(i)].loc[df['Item'] == item].iloc[0])
    req_count = str(
      df['Req' + str(i) + ' Units'].loc[df['Item'] == item].iloc[0] * count)

    if (req != 'nan'):
      sub_req1 = str(df['Req1'].loc[df['Item'] == req].iloc[0])
      sub_req1_count = str(df['Req1 Units'].loc[df['Item'] == req].iloc[0] *
                           count)

      sub_req2 = str(df['Req2'].loc[df['Item'] == req].iloc[0])
      sub_req2_count = str(df['Req2 Units'].loc[df['Item'] == req].iloc[0] *
                           count)

      sub_req3 = str(df['Req3'].loc[df['Item'] == req].iloc[0])
      sub_req3_count = str(df['Req3 Units'].loc[df['Item'] == req].iloc[0] *
                           count)

    embed.add_field(name=req + ': ' + req_count,
                    value=sub_req1 + ': ' + sub_req1_count + '/' + sub_req2 +
                    ': ' + sub_req2_count + '/' + sub_req3 + ': ' +
                    sub_req3_count,
                    inline=False)

  await context.send(embed=embed)


bot.run(TOKEN)
