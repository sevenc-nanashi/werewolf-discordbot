from dataclasses import dataclass

from lib.player import Players

class Game():

    def __init__(self):
        self.players = Players()
        self.channels = Channels
        self.roles = Roles
        self.days = 1
        self.tasks = 0
        self.times = 0
        self.vote_target = None
        self.raid_target = None
        self.escort_target = None

    @property
    def role_list(self) -> str:
        msg = ''
        for p in self.players:
            msg += f'\n{p.role_name} {p.mention}'
        return msg

    async def increase_task(self):
        self.tasks += 1

    async def decrease_task(self):
        self.tasks -= 1

    def is_village_win(self) -> bool:
        for p in self.players.alives:
            if p.role == "狼":
                return False
        return True

    def is_werewolf_win(self) -> bool:
        village_count = 0
        werewolf_count = 0
        for p in self.players.alives:
            if p.role == "狼":
                werewolf_count += 1
            else:
                village_count += 1
        return village_count <= werewolf_count

@dataclass
class Channels:
    alive: None
    dead: None
    audience: None
    wolfs: None
        
@dataclass
class Roles:
    alive: None
    dead: None