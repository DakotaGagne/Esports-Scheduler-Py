'''

# Reg Season Scheduler (AXHL, Round Robin Style)
# Created by Dakota Gagne
# Asking before using this program is appreciated

This program is designed to generate a pre season schedule for E Sports Hockey League

Needs to be run in a Python environment
Ensure Python3 is installed on your computer (https://realpython.com/installing-python/)
Open CMD Terminal or Powershell.
Type "pip install pandas" and press enter
Now in file explorer, navigate to the folder containing this file
Right click on explorer, and select "Open in Terminal"
Type "python AXHL_Round_Robin_Reg_Season_Scheduler.py" and press enter
Done! Check the folder for the generated schedule (CSV format)
'''

# Imports
import random
import sys
import pandas as pd
import datetime
import time




'''
START OF CUSTOMIZABLE VARIABLES

'''

defSeed = 8253577151864899339 # Default Seed to use if want repeatable results
autoseed = False # Set to True if want random results

TTL_MATCHES = 82 # Total number of matches to be played in a season

gameDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"] # List of weekdays on which games will be held. Can change to desired weekly sched
matchTimes = ["9:55PM EST", "10:35PM EST"] # Time slots for matches. Can change to desired time slots (must be 2 values)
startDay = [2025, 2, 23] # The starting day of the regular season schedule - Can be changed to desired start date
pausePointDates = [[[2025, 4, 18], [2025, 4, 21]]] # Dates where no games will be held - Can be changed to desired dates

team_names = [
    # Can be any Number of teams, so long as it is even
    "Albany Devils",
    "Bloomington Bison",
    "Brampton Beast",
    "Calgary Flames",
    "Carolina Hurricanes",
    "Chicago Blackhawks",
    "Cincinnati Cyclones",
    "Cincinnati Mighty Ducks",
    "Columbus Cottonmouths",
    "Dallas Stars",
    "Detroit Red Wings",
    "Edmonton Oilers",
    "Edmonton Road Runners",
    "Florida Panthers",
    "Grand Rapids Griffins",
    "Greenville Swamp Rabbits",
    "Hershey Bears",
    "Iowa Heartlanders",
    "Jacksonville Icemen",
    "Lehigh Valley Phantoms",
    "Los Angeles Kings",
    "Manitoba Moose",
    "Minnesota Wild",
    "Montreal Canadiens",
    "New Haven Eagles",
    "New Jersey Devils",
    "New York Rangers",
    "Ontario Reign",
    "Pittsburgh Penguins",
    "Saint John Sea Dogs",
    "San Jose Sharks",
    "Springfield Thunderbirds",
    "Syracuse Crunch",
    "Tampa Bay Lightning",
    "Toeldo Walleye",
    "Toronto Maple Leafs",
    "Utah HC",
    "Vancouver Canucks",
    "Vegas Golden Knights",
    "Washington Capitals"
]


def addDay (date, d = 1): # Increments datetime var by 1 day, or more if specified
    return date + datetime.timedelta(days=d)



def round_robin_generator(teams, cycles = 1):
    tm_cnt = len(teams)
    if tm_cnt % 2 != 0:
        raise ValueError("Number of teams must be even.")
    # Initialize the matches
    matches = []
    
    # Generate the matches
    tm_cnt = len(teams)
    dir = 0
    for _ in range(cycles):
        for ts in range(tm_cnt - 1):
            timeslot = []
            for i in range(tm_cnt // 2):
                team1 = teams[(ts + i) % (tm_cnt - 1)]
                team2 = teams[tm_cnt - 1] if i == 0 else teams[(ts + tm_cnt - 1 - i) % (tm_cnt - 1)]

                # Add the match to the schedule
                if dir == 0:
                    timeslot.append([team1, team2])
                else:
                    timeslot.append([team2, team1])
            matches.append(timeslot)
        dir = [1, 0][dir]
    print("Round Robin Matches Generated")
    return matches



def format_schedule(match_list, day, seed):
    # Takes the list of matches generated and converts into a string
    # match_list contains the raw values of the matches
    # day contains the datetime value starting at the start date
    match_time = 0 # 0 or 1 depending on which time slot will be used (used to pull time from global matchTimes var)
    sched = []
    sched.append("="*20 + " AXHL REGULAR SEASON SCHEDULE - Created by Dakota " + "="*20)
    sched.append("Seed: " + str(seed))
    sched.append(" ")    
    
    for time_slot in match_list:
        # Skip dates that are excluded
        # Skips days that wont have games
        while day.strftime("%A") not in gameDays:
            day = addDay(day)
        # Skips any date specified
        for pausePoint in pausePointDates:
            if len(pausePoint) == 3:
                # Single Date
                pauseDate = datetime.date(pausePoint[0], pausePoint[1], pausePoint[2])
                if day == pauseDate:
                    day = addDay(day)
            else:
                # Date Range
                pauseStart = datetime.date(pausePoint[0][0], pausePoint[0][1], pausePoint[0][2])
                pauseEnd = datetime.date(pausePoint[1][0], pausePoint[1][1], pausePoint[1][2])
                if day >= pauseStart and day <= pauseEnd:
                    while day <= pauseEnd:
                        day = addDay(day)
        # Skips days that wont have games
        while day.strftime("%A") not in gameDays:
            day = addDay(day)
            
        for match in time_slot:
            # written like this for readability
            matchStr = ""
            # add first match conf, div, name, respectively
            matchStr += "(HOME) " + str(match[0])
            # add vs separator
            matchStr += " VS "
            # add second match conf, div, name, respectively
            matchStr += "(AWAY) " + str(match[1])
            # add time and date
            matchStr += " -> " + str(day) + ", " + str(matchTimes[match_time])
            # Add match to schedule
            sched.append(matchStr)
        # Add spacer after time slot
        sched.append(" ")
        match_time = [1, 0][match_time] # swap time slot time
        if(match_time == 0): # time slot for given day completed
            # iterate day
            day = addDay(day)
            # add readability divider
            sched.append("="*100)
            # add spacer
            sched.append(" ")
    print("Formatted Schedule")
    return sched
    


def main():
    # Shuffle the teams
    if autoseed:
        seed = random.randint(0, sys.maxsize)
    else:
        seed = defSeed
    random.seed(seed)
    # random.shuffle(team_names)
    
    # Calculate # of round robin schedules needed for each tier
    i = 0
    while i * len(team_names)-1 < TTL_MATCHES: i += 1
    cycles = i
    print("Total Cycles: " + str(cycles))
    
    # Generate Round Robin Schedule for each Tier
    matches = round_robin_generator(team_names, cycles)
    
    # Strip excess matches from the schedules
    matches = matches[:TTL_MATCHES]
    print("Matches Trimmed")
    
    # Match Checking
    team_cnt = [0] * len(team_names)
    for ts in matches:
        for m in ts:
            team_cnt[team_names.index(m[0])] += 1
            team_cnt[team_names.index(m[1])] += 1
    if len(set(team_cnt)) != 1:
        raise ValueError("Teams do not have the same number of matches.")
    print("All teams have the same number of matches: " + str(team_cnt[0]))
    
    # Using datetime module for built in calendar handling (can check day of week this way)
    day = datetime.date(startDay[0], startDay[1], startDay[2])
    
    # Format the schedule with dates, home, and away
    schedule = format_schedule(matches, day, seed)
    
    # Output the schedules as csv file
    scheduleDF = pd.DataFrame(schedule)
    scheduleDF.to_csv("AXHL_REGULAR_SEASON_SCHEDULE.csv", index=False, header=0) # Update the name to include season number
    print("Schedules have been generated and saved to CSV files.")
    print("Seed Used: " + str(seed))
    
    print("Total Timeslots / Matches: " + str(len(matches)))
    ttlMatchCnt = str(sum([len(ts) for ts in matches]))
    print("Total Games in Season (Should be " + str(len(matches)*len(team_names)//2) + "): " + ttlMatchCnt)
 
    
    
if __name__ == "__main__":
    main()