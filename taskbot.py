# Codeniacs FLL Taskbot
import discord
import asyncio
from db import dp

class Cl:
	
	def __init__(self):
		client = discord.Client()

		db = dp.db()
		db.connect('Taskbot.sqlite3')
		db.cursor()
		db.createtasktable()

		help_message = '''Taskbot Help Message\n
		Description:
		This is a bot that helps you with task management. You can add Tasks, view them and later delete.\n
		Commands:
		#:task <taskname> = Add a task to your account
		#:mytasks = Get all your tasks
		#:deltask <taskname> = Delete the task with this name
		#:? of #:help = Help command
		'''


		@client.event
		async def on_ready():
			print('Logged in as')
			print(client.user.name)
			print(client.user.id)
			print('------')
			await client.change_presence(game=discord.Game(name="Prefix: '#:'"))

		@client.event
		async def on_message(message):
			if message.content.startswith('#:task'):
				tmp = await client.send_message(message.channel, 'Adding Task ...')
				task = message.content[7:]
				db.addtask(task, message.author)
				await client.edit_message(tmp, 'Added task {} for user {}.'.format(task, message.author))

			elif message.content.startswith('#:mytasks'):
				tmp = await client.send_message(message.channel, 'Getting Tasks ...')
				tasksraw = db.gettasks(message.author)
				tcount = 0
				tasks = ""
				for task in tasksraw:
					count = tcount + 1
					tcount += 1
					tasks += "{}: {}\n".format(count, task[1])
					
				if len(tasks) != 0:
					await client.edit_message(tmp, 'Tasks for {}\n{} '.format(message.author,tasks))
				else:
					await client.edit_message(tmp, 'You have no tasks')
					
			elif message.content.startswith('#:deltask'):
				tmp = await client.send_message(message.channel, 'Deleting Task ...')
				task = message.content[10:]
				author = message.author
				if db.deletetask(task, author):
					await client.edit_message(tmp, 'Deleted task {} from {}\'s tasks '.format(task, author))
				else:
					await client.edit_message(tmp, 'Error: Can\'t delete task {}'.format(task))
					
			elif message.content.startswith('#:help') or message.content.startswith('#:?'):
				await client.send_message(message.author, help_message)
				
			
			elif message.content.startswith('!'):
				db.disconnect()
				raise SystemExit("Exited with !exit command")

		client.run('Mzk5MjI4NjM4NTY3ODU4MTc3.DTOZ6Q.Svv0IT8cbq3Cw4nDyyWJfznCEJw')
	
if __name__ == "__main__":
	c = Cl()
