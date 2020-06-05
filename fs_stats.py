import asyncio
from enum import Enum, auto
import re
import os

import watchgod

import database

OUTPUT_LOG = os.environ['USERPROFILE'] + r'\AppData\LocalLow\Sirlin Games\Fantasy Strike\output_log.txt'

class State(Enum):
	GAME_CLOSED = auto()
	NO_MATCH = auto()
	MATCH = auto()

class StateMachine():
	def __init__(self, state=None):
		if state is None:
			state = State.GAME_CLOSED
		
		self.state = state
		
		self.gameplay_random_seed = None
		self.opp_name = None
		self.opp_rank = None
		self.my_rank = None
		self.player_number = None
		self.win = None
		self.loser_score = None

	def __call__(self, line):
		if self.state == State.GAME_CLOSED:
			self.game_closed(line)
		elif self.state == State.NO_MATCH:
			self.no_match(line)
		elif self.state == State.MATCH:
			self.match(line)
	
	def game_closed(self, line):
		# If the game is closed but we're getting updates,
		# it must be open again
		self.state = State.NO_MATCH
	
	def no_match(self, line):
		if 'Steam shutdown' in line:
			self.on_shutdown()
	
		if '[|joinranked:' in line:
			data = line[:-1].split('|joinranked:')[1]
			my_dict = dict([value.split(':') for value in data.split(',')])
			if 'oppName' in my_dict:
				self.gameplay_random_seed = int(my_dict['gameplayRandomSeed'])
				self.player_number = int(my_dict['pnum'])
				self.opp_name = my_dict['oppName']
				self.opp_rank = int(my_dict['oppLeague']), int(my_dict['oppRank'])
				self.my_rank = int(my_dict['playerLeague']), int(my_dict['playerRank'])
				
				self.state = State.MATCH
	
	def match(self, line):
		if 'Steam shutdown' in line:
			self.on_shutdown()
		
		if 'END PrepareTeamBattleScreen' in line:
			if (match := re.search(r'winnerChars P1 (\[.*?\]) P2 (\[.*?\])', line)):		
				if len(match.group(1).split(',')) == 3:
					# player 1 wins
					self.loser_score = len(match.group(2).split(','))
					self.win = self.player_number == 1
				elif len(match.group(2).split(',')) == 3:
					# player 2 wins
					self.loser_score = len(match.group(1).split(','))
					self.win = self.player_number == 2
				else:
					return
				
				database.add(
					self.gameplay_random_seed,
					self.win,
					self.opp_name,
					self.opp_rank[0],
					self.opp_rank[1],
					self.my_rank[0],
					self.my_rank[1],
					self.loser_score
				)
				
				self.gameplay_random_seed = self.opp_name = self.opp_rank = self.my_rank = self.player_number = self.win = self.loser_score = None
				self.state = State.NO_MATCH
	
	def on_shutdown(self):
		self.gameplay_random_seed = self.opp_name = self.opp_rank = self.my_rank = self.player_number = self.win = self.loser_score = None
		self.state = State.GAME_CLOSED

		database.publish()

def main(state_machine):
	with open(OUTPUT_LOG) as f:
		for _ in watchgod.watch(OUTPUT_LOG):
			for line in f.readlines():
				line = line.strip()
				if line:
					state_machine(line)


if __name__ == '__main__':
	main(StateMachine())