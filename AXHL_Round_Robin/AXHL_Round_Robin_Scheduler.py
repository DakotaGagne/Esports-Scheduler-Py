

# Imports
import random
import sys
import pandas as pd
import datetime
import time

# Declarations

defSeed = 6730504492698659822 # Default Seed to use if want repeatable results
autoseed = False # Set to True if want random results


'''

START OF CUSTOMIZABLE VARIABLES

'''
TTL_MATCHES = 82 # Total number of matches to be played in a season

gameDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"] # List of weekdays on which games will be held. Can change to desired weekly sched
matchTimes = ["9:55PM EST", "10:35PM EST"] # Time slots for matches. Can change to desired time slots (must be 2 values)
startDayRegseason = [2025, 2, 23] # The starting day of the regular season schedule - Can be changed to desired start date
pausePointDates = [[[2025, 4, 18], [2025, 4, 21]]]

team_names = [
    # Can be any Number of teams, so long as it is even
    "Team 1",
    "Team 2",
    "Team 3",
    "Team 4",
    "Team 5",
    "Team 6",
    "Team 7",
    "Team 8",
    "Team 9",
    "Team 10",
    "Team 11",
    "Team 12",
    "Team 13",
    "Team 14",
    "Team 15",
    "Team 16",
    "Team 17",
    "Team 18",
    "Team 19",
    "Team 20",
    "Team 21",
    "Team 22",
    "Team 23",
    "Team 24",
    "Team 25",
    "Team 26",
    "Team 27",
    "Team 28",
    "Team 29",
    "Team 30",
    "Team 31",
    "Team 32",
    "Team 33",
    "Team 34",
    "Team 35",
    "Team 36",
    "Team 37",
    "Team 38",
    "Team 39",
    "Team 40"
]



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
        
    
    
    
    
    print("Generated Round Robin Schedule")


def format_schedule(matches):
    return matches
    
    print("Formatted Schedule")


        
def main():
    '''
    HOW DOES PRE SEASON WORK?
    WHAT IS UP WITH THE RESCHEDULED GAMES?
    ARE THERE CONF AND DIV GAMES?
    CHANGE LIST
    Need 1 Schedule for 40 teams (should handle any even number)
    Need to add dates
    ttl matches should be 82
    Set it to make full schedules until exceeding ttl matches

    Order of operations:
    Calculate number of round robin schedules needed
    Generate one and duplicate
    Alternate Home and Away for them all
    Strip excess to hit 82 matches
    Add dates to each match
    '''
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
    
    # # Format the schedule with dates, home, and away
    # upperTierSchedule = format_schedule(upperTierSchedule)
    
    # Output the schedules as csv file
    # upperTierDF = pd.DataFrame(upperTierSchedule)
    # upperTierDF.to_csv("UpperTierSchedule.csv")
    # print("Schedules have been generated and saved to CSV files.")
    # print("Seed Used: " + str(seed))
    
    



if __name__ == "__main__":
    main()