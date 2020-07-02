import sqlite3
import contextlib
import tempfile
import math

from tabulate import tabulate

PUBLISH_TO_SERVER = False

if PUBLISH_TO_SERVER:
	import paramiko

def add(id, win, opp_name, opp_league, opp_rank, my_league, my_rank, loser_score):
	with contextlib.closing(sqlite3.connect('games.db')) as conn:
		c = conn.cursor()
		# make sure the table exists
		c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='games';")
		if not c.fetchone()[0]:
			c.execute("""
				CREATE TABLE games
				(
					id INTEGER PRIMARY KEY,
					win INTEGER,
					opp_name TEXT,
					opp_league INTEGER,
					opp_rank INTEGER,
					my_league INTEGER,
					my_rank INTEGER,
					loser_score INTEGER,
					timestamp TEXT DEFAULT CURRENT_TIMESTAMP
				);
			""")
		
		c.execute('SELECT COUNT(*) FROM games WHERE id=?;', (id,))
		if not c.fetchone()[0]:
			c.execute("""
				INSERT INTO games
				(id, win, opp_name, opp_league, opp_rank, my_league, my_rank, loser_score)
				VALUES (?, ?, ?, ?, ?, ?, ?, ?);""",
				(id, win, opp_name, opp_league, opp_rank, my_league, my_rank, loser_score)
			)
			
			conn.commit()

def oldest_game():
	with contextlib.closing(sqlite3.connect('games.db')) as conn:
		c = conn.cursor()
		c.execute("""
			SELECT timestamp
			FROM games
			ORDER BY timestamp ASC
			LIMIT 1;
		""")
		return c.fetchone()[0].split(' ')[0]

def get_win_loss():
	with contextlib.closing(sqlite3.connect('games.db')) as conn:
		c = conn.cursor()
		c.execute('SELECT COUNT(*) FROM games WHERE win=1;')
		wins = c.fetchone()[0]
		c.execute('SELECT COUNT(*) FROM games WHERE win=0;')
		losses = c.fetchone()[0]
		gcd = math.gcd(wins, losses)
		return f'{wins//gcd}:{losses//gcd}'

def format_row(row):
	def get_rank(league, rank):
		if league == 4:
			return f'Master {rank}'
		
		return f"""{(
				'Bronze',
				'Silver',
				'Gold',
				'Diamond',
			)[league]} {(
				'E',
				'D',
				'C',
				'B',
				'A',
			)[rank]}"""
	win, opp_name, opp_league, opp_rank, my_league, my_rank, loser_score, timestamp = row
	
	return (
		timestamp[:-3],
		opp_name,
		('Loss', 'Win')[win],
		(f'{loser_score}-3', f'3-{loser_score}')[win],
		get_rank(opp_league, opp_rank),
		get_rank(my_league, my_rank),
	)

def fetch_rows():
	with contextlib.closing(sqlite3.connect('games.db')) as conn:
		c = conn.cursor()
		c.execute("""
			SELECT
				win,
				opp_name,
				opp_league,
				opp_rank,
				my_league,
				my_rank,
				loser_score,
				timestamp
			FROM games
			ORDER BY timestamp DESC;""")
		
		for row in c:
			yield format_row(row)

def create_table(rows):
	return tabulate(rows, headers=[
		'Timestamp',
		'Opponent',
		'Result',
		'Score',
		'Opponent Rank',
		'My Rank',
	])

def publish():
	with tempfile.TemporaryFile(mode='r+') as f:
		table = create_table(fetch_rows())
		table_width = len(table.split('\n')[1]) # the hyphens separating headers from data
		                                        # guaranteed to be the longest line		
		
		print('FANTASY STRIKE RANKED RESULTS'.center(table_width), file=f)
		print('-----------------------------'.center(table_width), file=f)
		print('Updated automatically after each match'.center(table_width), file=f)
		print(file=f)
		print(f'Win:loss ratio since {oldest_game()} is {get_win_loss()}', file=f)
		print(file=f)
		print(create_table(fetch_rows()), file=f)
		print(file=f)
		print('Generated with https://github.com/undergroundmonorail/fs_stats', file=f)
		f.seek(0)
		
		if PUBLISH_TO_SERVER:
			with paramiko.SSHClient() as ssh:
				ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				ssh.connect('glaceon.social', username='mastodon', key_filename='id_rsa')
				with ssh.open_sftp() as sftp:
					sftp.putfo(f, 'hollymcfarland.com/fs-stats.txt')
		else:
			with open('output.txt', 'w') as f2:
				print(f.read(), file=f2)
