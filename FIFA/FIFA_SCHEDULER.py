'''

# Regular Season Scheduler (FIFA)
# Created by Dakota Gagne
# Asking before using this program is appreciated

Needs to be run in a Python environment
Ensure Python3 is installed on your computer (https://realpython.com/installing-python/)
Open CMD Terminal or Powershell.
Type "pip install pandas" and press enter
Now in file explorer, navigate to the folder containing this file
Right click on explorer, and select "Open in Terminal"
Type "python reg_season_scheduler.py" and press enter
Done! Check the folder for the generated schedule (CSV format)

*Notes* 
This scheduler creates a round-robin style schedule
2 Timeslots Per Day
Each team plays each other equivalent of TIMES_TO_PLAY
Each team has an equal amount of home and away matches
Each team plays every other team exactly TIMES_TO_PLAY times
Each team plays twice per day
No Conf or Divisions for this schedule. Just Teams
Output format is CSV
Output includes the seed used to generate the schedule
Real World Dates and Times are not included in this iteration
    Still shows days in day 1, day 2, etc format
    Still shows timeslots in timeslot 1, timeslot 2 format

'''



# Imports
import random
import sys
import pandas as pd
import datetime
import time

# Declarations

defSeed = 6730504492698659822 # Default Seed to use if want repeatable results
autoseed = True # Set to True if want random results

'''

START OF CUSTOMIZABLE VARIABLES

'''

# team_names = [
#     # Can be any Number of teams, so long as it is even
# "Anaheim Ducks",
# "California Golden Seals",
# "Edmonton Oilers",
# "Minnesota Wild",
# "San Jose Sharks",
# "Seattle Kraken",
# "Utah Ice",
# "Vancouver Canucks",
# "Atlanta Gladiators",
# "Atlanta Thrashers 2",
# "Chicago Blackhawks",
# "Chicago Wolves",
# "Huntington Blizzards",
# "Iowa Heartlanders",
# "Nashville Predators",
# "Toledo Walleye",
# "Buffalo Sabres",
# "Carolina Hurricanes",
# "Cleaveland Monsters",
# "Detroit Red Wings"
# ]

team_cnt = 42
team_names = []

    

TIMES_TO_PLAY = 2 # Number of times each team plays each other
# Note: The schedule will repeat itself exactly for each time to play eachother


'''

END OF CUSTOMIZABLE VARIABLES

'''




#gameDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"] # List of weekdays on which games will be held - Not needed for this iteration
#matchTimes = ["9:55PM EST", "10:35PM EST"] # Not needed for this iteration
#startDay = [2024, 9, 1] # Not needed for this iteration
#pausePoint = [] # May or may not be needed

#def addDay (date, d = 1): # Increments datetime var by 1 day, or more if specified
#    return date + datetime.timedelta(days=d)


def schedule_generator(teams, times_to_play = 1):
    tm_cnt = len(teams)
    if tm_cnt % 2 != 0:
        raise ValueError("Number of teams must be even.")

    # Initialize the schedule
    schedule = []

    # Generate the matches
    dir = 0
    for _ in range(times_to_play):
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
            schedule.append(timeslot)
        dir = [1, 0][dir]

    return schedule

        
def format_schedule(matches, seed):
    # Using day 1, 2, 3...
    # Not using real dates or times, will need to add that in when given
    day = 0
    f_sched = []
    f_sched.append("==================== AXFIFA SCHEDULE - Created by Dakota ====================")
    f_sched.append("Seed: " + str(seed))
    tsI = 0
    for ts in matches:
        if tsI == 0:
            f_sched.append(" ")
            day += 1
            f_sched.append("================ DAY " + str(day) + " ================")
            f_sched.append(" ")
            f_sched.append("------- Timeslot 1 ------")
        else:
            f_sched.append(" ")
            f_sched.append("------- Timeslot 2 ------")
        for m in ts:
            f_sched.append("(HOME) " + str(m[0]) + " VS " + " (AWAY) " + str(m[1]))
        tsI = [1, 0][tsI]
    return f_sched
        
def main():
    
    start_time = time.time()
    # Seeding for Schedule
    if autoseed:
        seed = random.randrange(sys.maxsize)
    else:
        seed = defSeed
    random.seed(seed)
    
    start_time = time.time()
    print("")
    print("FIFA Schedule Generating...")
    print("Seed Used: " + str(seed))
    

    # Shuffle teams
    random.shuffle(team_names)
    
    print("Generating Matches...")
    schedule = schedule_generator(team_names, TIMES_TO_PLAY)
            
    # Error Check for timeslots
    
    print("Error Checking...")
    # Duplicate Check
    #   Makes sure that the schedule didn't generate more than 1 match for a given team in each time slot
    for tm in team_names:
        for ts in schedule:
            cnt = 0
            for m in ts:
                # Should always find one match that satisfies the below condition, but not two
                if tm == m[0] or tm == m[1]:
                    cnt += 1
                    # Raise exception if found more than one
                    if cnt > 1:
                        raise Exception("Something went wrong. Duplicate team in time slot")
    # Equal Home Away Check
    #   Makes sure each team has equal home and away matches
    test_teams = {}
    for tm in team_names:
        test_teams[tm] = [0, 0] # [HOMECNT, AWAYCNT]
    for ts in schedule:
        for m in ts:
            test_teams[m[0]][0] += 1
            test_teams[m[1]][1] += 1
    valid = True
    for tm in team_names:
        if test_teams[tm][0] != test_teams[tm][1]:
            valid = False
    if not valid:
        raise Exception("ERROR: At least one team has unequal home and away matches. Debug info: " + str(test_teams))
    else:
        print("Equal Home and Away Matches")

    # COUNTERS

    # TTL Matches Counter
    matchCnt = 0
    for ts in schedule:
        matchCnt += len(ts)
    print("Total Matches: " + str(matchCnt))
    
    #TTL Matches Per Team Counter
    print("Total Matches Per Team: " + str(len(schedule)))
    
    #TTL Days to play Counter
    print("Total Match Days: " + str(len(schedule)/2))
    
    
    # Schedule Formatting
    print("Formatting Schedule...")
    formatted_schedule = format_schedule(schedule, seed)
    

    # Convert schedule to CSV
    # Create CSV file for schedule

    print("Creating AXFIFA SCHEDULE CSV...")
    df = pd.DataFrame(formatted_schedule)
    df.to_csv('AXFIFA_SCHEDULE.csv', index=False, header=0)
    
    # Print time it takes to execute
    print("Execution took %s Seconds" % (time.time() - start_time))


if __name__ == "__main__":
    for i in range(team_cnt):
        team_names.append("Team " + str(i+1))
    print("Team Count: " + str(len(team_names)))
    main()