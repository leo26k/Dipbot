import discord
# from discord import app_commands
from discord.ext import commands, tasks
import os
# from keep_alive import keep_alive
from datetime import datetime, timedelta
import gc
# import json
import pytz
import asyncio
from copy import deepcopy
from functions import check_roles, trigger_, check_defend, check_move, check_support, check_convoy, check_build, check_disband, check_retreat, di, check_disband_retreat, check_hold

client = commands.Bot(intents=discord.Intents.all(),
	command_prefix='.',
	help_command=None)


print(db["da"]["turn"]["deadline"])
nations_discord={'italy': (1122279175819120832, 1123708225615839302), 'france': (1122279070005215363, 1123708106472439959), 'germany': (1122279150628130836, 1123708170729177139), 'austria': (1122279223269273620, 1123708412245594123), 'russia': (1122279202096427009, 1123708253591834634), 'turkey': (1122279246212120697, 1123708368285089894), 'england': (1122279123398705292, 1123708322579759256)}

@client.event
async def on_ready():
	print('online')
	# check_deadline.start()

@tasks.loop(minutes=5)
async def check_deadline():
	# print('here')
	# pass
	chn=client.get_channel(1122279536697016320)
	now=datetime.now(pytz.UTC)
	d=now.strftime('%d.%m.%Y %H')
	if db['da']['turn']['deadline'][0]==d:
		await trigger_func('real')
		await asyncio.sleep(10)
	elif db['da']['turn']['deadline'][3]==d:
		da=db['da']
		season=da['turn']['season']
		for idd in da['nations']:
			missing=0
			if season in ['spring', 'autumn']:
				for ter in da['nations'][idd]['units']:
					if ter not in da['nations'][idd]['orders']:
						missing=1
			elif season in ['winter', 'summer']:
				for ter in da['turn']['retreats']:
					missing=1
				if len(missing)==0:
					missing=1
			else:
				scs=len(da['nations'][idd]['sc_lands'])
				uns=len(da['nations'][idd]['units'])
				if scs<uns:
					missing=1
				elif scs>uns:
					missing=1
			if missing==1:
					chn=client.get_channel(nations_discord[idd][0])
					await chn.send(f"<@&{nations_discord[idd][1]}> 1h reminder")
		db['da']['turn']['deadline'][3]=0
		
		# old_deadline=db['da']['turn']['deadline'][1]
		# old_time=datetime.strptime(old_deadline, '%d.%m.%Y %H')
		# new_time=old_time+timedelta(hours=24)
		# n=new_time.replace(tzinfo=pytz.UTC)
		# ts=datetime.timestamp(n)
		# ti=str(ts).split('.')[0]
		# new_deadline=new_time.strftime('%d.%m.%Y %H')
		# db['da']['turn']['deadline'][0]=new_deadline
		# db['da']['turn']['deadline'][1]=new_deadline
		# db['da']['turn']['deadline'][2]=0    
		# await chn.send(f'<t:{int(ti)}:f>')
	else:
		await chn.send('checked')
		# await asyncio.sleep(10)
		# return
	



async def trigger_func(mode):
	da=deepcopy(db['da'])
	first_season=da['turn']['season']
	first_year=da['turn']['year']
	# for i in da['nations']:
	# 	print(i, da['nations'][i]['orders'])
	
	da_new, msg_t, second_season, second_year=trigger_(da)
	if mode=='real':
		chn_id=1122279631781896263	
		log_chn=client.get_channel(chn_id)
		for m in msg_t:
			await log_chn.send(m)
		
		chn=client.get_channel(1122279611972202546)
		await chn.send(f"**{first_year} {first_season} orders**", file=discord.File(f'turns/{first_year}_{first_season}_orders.png'))
		await chn.send(f"**{second_year} {second_season}**", file=discord.File(f'turns/{second_year}_{second_season}_state.png'))
		for n in nations_discord:
			if len(da_new['nations'][n]['sc_lands'])>0:
				chn=client.get_channel(nations_discord[n][0])
				await chn.send(f"<@&{nations_discord[n][1]}> new turn, **{second_year} {second_season}**")

		old_deadline=da_new['turn']['deadline'][1]
		old_time=datetime.strptime(old_deadline, '%d.%m.%Y %H')
		new_time=old_time+timedelta(hours=24)    
		new_time2=old_time+timedelta(hours=23)  
		n=new_time.replace(tzinfo=pytz.UTC)
		ts=datetime.timestamp(n)
		ti=str(ts).split('.')[0]
		new_deadline=new_time.strftime('%d.%m.%Y %H')
		new_deadline2=new_time2.strftime('%d.%m.%Y %H')
		da_new['turn']['deadline'][0]=new_deadline
		da_new['turn']['deadline'][1]=new_deadline		
		da_new['turn']['deadline'][3]=new_deadline2	
		da_new['turn']['deadline'][2]=0
		chn=client.get_channel(1125889045147418645)
		await chn.send(f"**{second_year} {second_season}** deadline:\n<t:{int(ti)}:f>")
		db['da']=deepcopy(da_new)

	del da
	gc.collect()
	return
# @check_deadline.before_loop
# async def before_trigger():
# 	print('here')
# # 	now=datetime.now(pytz.UTC)
# 	d=now.strftime('%d.%m.%Y %H:%M')
# 	if db['da']['turn']['deadline']==d:
# 		await fake_trigger()
# 		db['da']['turn']['deadline']='17.07.2023 15:00'
# 		return
# 	chn=client.get_channel(1122279536697016320)
# 	await chn.send('checked')
# 	await asyncio.sleep(10)
# 	print('passed')
	# return
		# chn=client.get_channel(1122279536697016320)
		# await chn.send(f'time {d}')
# @client.command()
# async def print_da(ctx):
#   roles=check_roles(ctx)
#   if not roles[0]:
#     return
#   da=dict(db['da'])
#   with open(r'print_da.yaml', 'w') as file:
#     documents = yaml.dump(da, file)
#     file.close()
	# with open("print_da.json", "w") as outfile:
	#     outfile.write(json_object)
	#     outfile.close()
	# print('done')

@client.command()
async def request(ctx, t):
	roles=check_roles(ctx)
	if not roles[1]:
		return 
	idd=roles[2]
	t=int(t)      
	da=db['da']
	if t+da['turn']['deadline'][2]<=6 and t>0:
		old_deadline=db['da']['turn']['deadline'][0]
		old_time=datetime.strptime(old_deadline, '%d.%m.%Y %H')
		new_time=old_time+timedelta(hours=t)    
		n=new_time.replace(tzinfo=pytz.UTC)
		ts=datetime.timestamp(n)
		ti=str(ts).split('.')[0]
		new_deadline=new_time.strftime('%d.%m.%Y %H')
		new_time2=old_time+timedelta(hours=t-1)
		new_deadline2=new_time2.strftime('%d.%m.%Y %H')
		db['da']['turn']['deadline'][0]=new_deadline
		db['da']['turn']['deadline'][3]=new_deadline2
		db['da']['turn']['deadline'][2]+=t
		await ctx.message.add_reaction('👍')
		chn=client.get_channel(1125889045147418645)
		await chn.send(f"<@&{1123708064692981811}>, {idd} has extended the turn by {t}h\n<t:{int(ti)}:f>")
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send('can request max 6h extenison per turn')

@client.command()
async def start(ctx):
	check_deadline.start()

@client.command()
async def trigger(ctx, mode='fake'):
	roles=check_roles(ctx)
	if not roles[0]:
		return
		
	await trigger_func(mode)
	await ctx.reply('done')



# @client.command()
# async def fake_trigger(ctx):
#   roles=check_roles(ctx)
#   if not roles[0]:
#     return
#   fake_trigger_()


@client.command(aliases=['m'])
async def move(ctx, *, t):
	# .attack mos with sev
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	e=t.split(' ')
	target=e[-1].lower()
	ter=e[0].lower()
	msg_text, convoy, paths=check_move(idd, ter, target, da)
	
	if msg_text==None:
		db['da']['nations'][idd]['orders'][ter]={'target': target, 'mode': 'm', 'convoy': convoy, 'paths': paths}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()


@client.command(aliases=['s'])
async def support(ctx, *, t):
		# .suport mos to sev with war
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	e=t.split(' ')
	helped=e[0].lower()
	target=e[2].lower()
	ter=e[-1].lower()
	msg_text=check_support(idd, ter, helped, target, da)
	if msg_text==None:
		db['da']['nations'][idd]['orders'][ter]={'target': target, 'helped': helped, 'mode': 's'}
		
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()
	

@client.command(aliases=['d'])
async def defend(ctx, *, t):
#    .defend mos with ukr
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	e=t.split(' ')
	helped=e[0].lower()
	ter=e[-1].lower()
	msg_text=check_defend(idd, ter, helped, da)
	if msg_text==None:
		db['da']['nations'][idd]['orders'][ter]={'helped': helped, 'mode': 'd'}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()

@client.command(aliases=['c'])
async def convoy(ctx, *, t):
#    .convoy lon to bel with nth
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	e=t.split(' ')
	target=e[2].lower()
	helped=e[0].lower()
	ter=e[-1].lower()
	msg_text, paths=check_convoy(idd, ter, helped, target, da)
	if msg_text==None: 
		db['da']['nations'][idd]['orders'][ter]={'target': target, 'helped': helped, 'mode': 'c', 'paths': paths}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()
		

@client.command(aliases=['b'])
async def build(ctx, *, t):
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	e=t.split(' ')
	unit=e[0].lower()
	ter=e[-1].lower()
	msg_text=check_build(idd, ter, unit, da)
	if msg_text==None: 
		db['da']['nations'][idd]['orders'][ter]={'mode': 'b', 'unit': unit}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()


@client.command(aliases=['di', 'dd'])
async def disband(ctx, *, t):
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	e=t.split(' ')
	ter=e[0].lower()
	if da['turn']['season']=='build phase':
		msg_text=check_disband(idd, ter, da)
	else:
		msg_text=check_disband_retreat(idd, ter, da)	
	if msg_text==None:
		if da['turn']['season'] in ['winter', 'summer']:
			db['da']['nations'][idd]['orders'][ter]={'mode': 'di', 'unit': da['turn']['retreats'][ter]['unit']}
		else:
			db['da']['nations'][idd]['orders'][ter]={'mode': 'di', 'unit': da['nations'][idd]['units'][ter]}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()


@client.command(aliases=["vibes", "vibe", "chill", "chil", "rest"])
async def hold(ctx, ter):
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	ter=ter.lower()
	msg_text=check_hold(ter, idd, da)	
	if msg_text==None: 
		db['da']['nations'][idd]['orders'][ter]={'mode': 'h'}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()

@client.command(aliases=['r'])
async def retreat(ctx, *, t):
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	e=t.split(' ')
	ter=e[0].lower()
	target=e[-1].lower()
	msg_text=check_retreat(idd, ter, target, da)
	if msg_text==None: 
		db['da']['nations'][idd]['orders'][ter]={'mode': 'r', 'target': target, 'unit': da['turn']['retreats'][ter]['unit']}
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()


@client.command(aliases=['st', 'ss'])
async def stats(ctx):
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	msg_text=f"**{idd[0].upper()+idd[1:]}**  {di['discord'][idd]['text']}\n**{da['turn']['year']} {da['turn']['season']}**\n\n**Missing orders**:"
	season=da['turn']['season']
	if season in ['spring', 'autumn']:
		missing=[]
		for ter in da['nations'][idd]['units']:
			if ter not in da['nations'][idd]['orders']:
				missing.append(ter)
		if len(missing)==0:
			msg_text+=' no orders missing\n\n**Orders:**\n'
		else:
			msg_text+=f" {', '.join(missing)}\n\n**Orders**:\n"
	elif season in ['winter', 'summer']:
		missing=[]
		for ter in da['turn']['retreats']:
			if da['turn']['retreats'][ter]['idd']==idd:
				missing.append(ter)
		if len(missing)==0:
			msg_text+=' no orders missing\n\n**Orders:**\n'
		else:
			msg_text+=f" {', '.join(missing)}\n\n**Orders**:\n"
	else:
		scs=len(da['nations'][idd]['sc_lands'])
		ords=len(da['nations'][idd]['orders'])
		uns=len(da['nations'][idd]['units'])
		if scs<uns:
			dif=uns-scs-ords
			msg_text+=f" **disband {dif}** units\n\n**Orders:**\n"
		elif scs>uns:
			dif=scs-ords-uns
			msg_text+=f" **build {dif}** units\n\n**Orders:**\n"
		else:
			msg_text+=f" no orders missing\n\n**Orders:**\n"
	n=1
	for ter in da['nations'][idd]['orders']:
		order=da['nations'][idd]['orders'][ter]
		mode=order['mode']
		if mode=='m':
			msg_text+=f"{n}. move {ter} to {order['target']}\n"
		elif mode=='s':
			msg_text+=f"{n}. {ter} support {order['helped']} to {order['target']}\n"
		elif mode=='c':
			msg_text+=f"{n}. {ter} convoy {order['helped']} to {order['target']}\n"
		elif mode=='d':
			msg_text+=f"{n}. {ter} defend {order['helped']}\n"
		elif mode=='r':
			msg_text+=f"{n}. retreat {ter} to {order['target']}\n"
		elif mode=='di':
			msg_text+=f"{n}. disband {ter}\n"
		elif mode=='b':
			msg_text+=f"{n}. build {order['unit']} in {ter}\n"
		elif mode=='h':
			msg_text+=f"{n}. {ter} hold\n"
	await ctx.channel.send(msg_text)
	del da
	gc.collect()


@client.command(aliases=['re', 'rr'])
async def remove(ctx, ind):
	roles=check_roles(ctx)
	if not roles[1]:
		return
	idd=roles[2]
	da=db['da']
	# da=functions.da_
	ind=int(ind)
	msg_text=''
	if ind>len(da['nations'][idd]['orders']) or ind<1:
		msg_text+=f"index out of range, should be 1-{len(da['nations'][idd]['orders'])}"
	if msg_text=='': 
		del db['da']['nations'][idd]['orders'][(list(da['nations'][idd]['orders'].keys())[ind-1])]
		await ctx.message.add_reaction('👍')
	else:
		await ctx.message.add_reaction('❌')
		await ctx.channel.send(msg_text)
	del da
	gc.collect()




# toc = os.environ['toc']
# toc=
my_secret=str(os.environ['toc'])
# keep_alive()
client.run(my_secret)