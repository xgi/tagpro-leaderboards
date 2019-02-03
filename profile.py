import helpers


class Profile:
    def __init__(self, name, id, points):
        self.name = name
        self.id = id
        self.points = points
        self.data = {}

    def parse_data(self, d):
        self.data = {
            'Time Played': {
                'day': helpers.time_str(d['timePlayed']['today']),
                'week': helpers.time_str(d['timePlayed']['week']),
                'month': helpers.time_str(d['timePlayed']['month'])
            },
            'Games': {
                'day': d['games']['today'],
                'week': d['games']['week'],
                'month': d['games']['month']
            },
            'Wins': {
                'day': int(d['won']['today']),
                'week': int(d['won']['week']),
                'month': int(d['won']['month'])
            },
            'Losses': {
                'day': int(d['lost']['today']),
                'week': int(d['lost']['week']),
                'month': int(d['lost']['month'])
            },
            'Power-up %': {
                'day': 0 if int(d['stats']['today']['potentialPowerups']) == 0 else
                str(int(int(d['stats']['today']['powerups']) /
                        int(d['stats']['today']['potentialPowerups']) * 100)) + "%",
                'week': 0 if int(d['stats']['week']['potentialPowerups']) == 0 else
                str(int(int(d['stats']['week']['powerups']) /
                        int(d['stats']['week']['potentialPowerups']) * 100)) + "%",
                'month': 0 if int(d['stats']['month']['potentialPowerups']) == 0 else
                str(int(int(d['stats']['month']['powerups']) /
                        int(d['stats']['month']['potentialPowerups']) * 100)) + "%"
            },
            'Save %': {
                'day': 0 if int(d['stats']['today']['saveAttempts']) == 0 else
                str(int(int(d['stats']['today']['saved']) /
                        int(d['stats']['today']['saveAttempts']) * 100)) + "%",
                'week': 0 if int(d['stats']['week']['saveAttempts']) == 0 else
                str(int(int(d['stats']['week']['saved']) /
                        int(d['stats']['week']['saveAttempts']) * 100)) + "%",
                'month': 0 if int(d['stats']['month']['saveAttempts']) == 0 else
                str(int(int(d['stats']['month']['saved']) /
                        int(d['stats']['month']['saveAttempts']) * 100)) + "%",
            },
            'Tags': {
                'day': d['stats']['today']['tags'],
                'week': d['stats']['week']['tags'],
                'month': d['stats']['month']['tags']
            },
            'Popped': {
                'day': d['stats']['today']['pops'],
                'week': d['stats']['week']['pops'],
                'month': d['stats']['month']['pops']
            },
            'Grabs': {
                'day': d['stats']['today']['grabs'],
                'week': d['stats']['week']['grabs'],
                'month': d['stats']['month']['grabs']
            },
            'Captures': {
                'day': d['stats']['today']['captures'],
                'week': d['stats']['week']['captures'],
                'month': d['stats']['month']['captures']
            },
            'Hold': {
                'day': helpers.time_str(d['stats']['today']['hold']),
                'week': helpers.time_str(d['stats']['week']['hold']),
                'month': helpers.time_str(d['stats']['month']['hold'])
            },
            'Prevent': {
                'day': helpers.time_str(d['stats']['today']['prevent']),
                'week': helpers.time_str(d['stats']['week']['prevent']),
                'month': helpers.time_str(d['stats']['month']['prevent'])
            },
            'Returns': {
                'day': d['stats']['today']['returns'],
                'week': d['stats']['week']['returns'],
                'month': d['stats']['month']['returns']
            },
            'Support': {
                'day': d['stats']['today']['support'],
                'week': d['stats']['week']['support'],
                'month': d['stats']['month']['support']
            },
            'Disconnects': {
                'day': int(d['disconnected']['today']),
                'week': int(d['disconnected']['week']),
                'month': int(d['disconnected']['month'])
            }
        }

        self.data['Win %'] = {
            'day': 0 if self.data['Wins']['day'] == 0 else
            str(int(self.data['Wins']['day'] /
                    (self.data['Wins']['day'] + self.data['Losses']['day']
                     + self.data['Disconnects']['day']) * 100)) + "%",
            'week': 0 if self.data['Wins']['week'] == 0 else
            str(int(self.data['Wins']['week'] /
                    (self.data['Wins']['week'] + self.data['Losses']['week']
                     + self.data['Disconnects']['week']) * 100)) + "%",
            'month': 0 if self.data['Wins']['month'] == 0 else
            str(int(self.data['Wins']['month'] /
                    (self.data['Wins']['month'] + self.data['Losses']['month']
                     + self.data['Disconnects']['month']) * 100)) + "%"
        }
