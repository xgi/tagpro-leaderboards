class Profile:
    def __init__(self, url, name):
        self.url = url
        self.name = name

    def read_table(self, table):
        # convert table into dictionary
        self.data = {}

        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = [ele.text.strip() for ele in row.find_all('td')]
            # cols format (all str's):
            # [<Heading>, <Day>, <Week>, <Month>, <All>]

            if cols[0] == "Powerups":
                # hidden row which shows exact number of pups (without All col)
                continue

            # create dictionary with row headers as keys
            self.data[cols[0]] = {
                'day': cols[1],
                'week': cols[2],
                'month': cols[3],
                'all': cols[4]
            }
