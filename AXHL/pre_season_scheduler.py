'''

# Pre Season Scheduler (AXHL)
# Created by Dakota Gagne
# Asking before using this program is appreciated

This program is designed to generate a pre season schedule for E Sports Hockey League

Needs to be run in a Python environment
Ensure Python3 is installed on your computer (https://realpython.com/installing-python/)
Open CMD Terminal or Powershell.
Type "pip install pandas" and press enter
Now in file explorer, navigate to the folder containing this file
Right click on explorer, and select "Open in Terminal"
Type "python pre_season_scheduler.py" and press enter
Done! Check the folder for the generated schedule (CSV format)


*Notes* 
The variables that can be adjusted are listed below
This scheduler is designed to generate a schedule for a single week of games
Biggest priority is to prevent all duplicate matches
Home and Away matches not considered in this schedule
    

'''



# Imports
import random
import sys
import pandas as pd
import datetime
import time

# Declarations

defSeed = 2550841796367335994 # Default Seed to use if want repeatable results
autoseed = True # Set to True if want random results

'''

START OF CUSTOMIZABLE VARIABLES

'''

team_names = [
    # Can Change these values
    # Ensure that all divisions and conferences have the same number of teams
["W-Conf", "P-Div", "Alaska Aces"],
["W-Conf", "P-Div", "Anaheim Ducks"],
["W-Conf", "P-Div", "Calgary Flames"],
["W-Conf", "P-Div", "Coachella Valley Firebirds"],
["W-Conf", "P-Div", "Edmonton Oilers"],
["W-Conf", "P-Div", "Los Angeles Kings"],
["W-Conf", "P-Div", "Tahoe Knight Monsters"],
["W-Conf", "P-Div", "Utah Grizzlies"],
["W-Conf", "P-Div", "Vancouver Canucks"],
["W-Conf", "P-Div", "Vegas Golden Knights"],

["W-Conf", "C-Div", "Allen Americans"],
["W-Conf", "C-Div", "Chicago Blackhawks"],
["W-Conf", "C-Div", "Colorado Avalanche"],
["W-Conf", "C-Div", "Dallas Stars"],
["W-Conf", "C-Div", "Kansas City Mavericks"],
["W-Conf", "C-Div", "Phoenix Coyotes"],
["W-Conf", "C-Div", "Quad City Mallards"],
["W-Conf", "C-Div", "St. Louis Blues"],
["W-Conf", "C-Div", "Toledo Walleye"],
["W-Conf", "C-Div", "Winnipeg Jets"],

["E-Conf", "M-Div", "Buffalo Sabres"],
["E-Conf", "M-Div", "Carolina Hurricanes"],
["E-Conf", "M-Div", "Charlotte Checkers"],
["E-Conf", "M-Div", "Detroit Red Wings"],
["E-Conf", "M-Div", "Orlando Solar Bears"],
["E-Conf", "M-Div", "Pittsburgh Penguins"],
["E-Conf", "M-Div", "Richmond Renegades"],
["E-Conf", "M-Div", "Savannah Ghost Pirates"],
["E-Conf", "M-Div", "Toronto Maple Leafs"],
["E-Conf", "M-Div", "Washington Capitals"],

["E-Conf", "A-Div", "Boston Bruins"],
["E-Conf", "A-Div", "Hartford Whalers"],
["E-Conf", "A-Div", "Hershey Bears"],
["E-Conf", "A-Div", "Lehigh Valley Phantoms"],
["E-Conf", "A-Div", "Maine Mariners"],
["E-Conf", "A-Div", "New Jersey Devils"],
["E-Conf", "A-Div", "New York Rangers"],
["E-Conf", "A-Div", "Ottawa Senators"],
["E-Conf", "A-Div", "Philadelphia Flyers"],
["E-Conf", "A-Div", "Worcester Railers "]
]


gameDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"] # List of weekdays on which games will be held. Can change to desired weekly sched
matchTimes = ["9:55PM EST", "10:35PM EST"] # Time slots for matches. Can change to desired time slots (must be 2 values)
startDayPreseason = [2024, 10, 13] # The starting day of the pre season schedule - Can be changed to desired start date

'''

END OF CUSTOMIZABLE VARIABLES

'''



def addDay (date, d = 1): # Increments datetime var by 1 day, or more if specified
    return date + datetime.timedelta(days=d)




def fetch_random_team(): # Returns a random team from the list (specifically a list including conf, div, and name)
    randInd = random.randint(0, len(team_names)-1)
    return team_names[randInd]




def time_slot_generator(match_list):
    # Generates a list of matches for a single time slot
    # Will only work if the list of teams is an even number
    # Also prevents any duplicates in the schedule
        # Note: Since the scheduler is random, sometimes a schedule is made that
        #       forces duplicates, so there are only a certain number of attempts
        #       allowed when picking a new match, to prevent infinite looping.
        #       If a match fails to be found within the allowable limit,
        #       the whole schedule gets reattempted until it succeeds (within another limit)
    
    matches = []
    matchCnt = int(len(team_names)/2)

    for _ in range(matchCnt):
        # Adds a single match to list
        # Ensures that the teams chosen has not been added to the list already
        duplicate = True
        
        attempts = 0 # Used for tracking attempts made to find new match
        max_attempts = 150 # Total allowed attempts to find a match (can be adjusted as needed)
        while duplicate:
            # Initializes the team variables for the conf, div, and name (done in seperate vars for readability)
            tm1C = tm1D = tm2N = ""
            tm2C = tm2D = tm2N = ""
            occurs = True
            # Generate team1Name
            while occurs:
                occurs = False
                tm1C, tm1D, tm1N = fetch_random_team()
                if len(matches) > 0: # Makes sure at least one match has already been created
                    for m in matches:
                        if tm1N == m[0][2] or tm1N == m[1][2]:
                            # Team is already added to list so try again
                            occurs = True

            # Generate team2Name
            # Note: most of this part is a copy of the above, except an additional check
            # to make sure that the second team is not the same as the first
            # I could shorten this code but left it like this for readability
            occurs = True
            while occurs:
                occurs = False
                tm2C, tm2D, tm2N = fetch_random_team()
                if(tm2N == tm1N):
                    # Same team chosen for both sides of the match, so try again
                    occurs = True
                elif len(matches) > 0:
                    for m in matches:
                        if tm2N == m[0][2] or tm2N == m[1][2]:
                            # Team is already added to list so try again
                            occurs = True
            
            # Match duplication check
            duplicate = False
            for time_slot in match_list:
                for match in time_slot:
                    #if (match[0][2] == tm1N or match[1][2] == tm1N) and (match[0][2] == tm2N or match[1][2] == tm2N):
                    if tm1N == match[0][2] or tm1N == match[1][2]:
                        if tm2N == match[0][2] or tm2N == match[1][2]:
                            # Both team names for new match exist in another scheduled match
                            # So reattempt
                            duplicate = True
                            attempts += 1 
                            if attempts > max_attempts:
                                # Attempts exceed max allowed, so raise exception to be caught in try statement
                                # Will force a new schedule to be attempted
                                raise Exception()
        # Match fits into timeslot and is not a duplicate, so add it
        matches.append([[tm1C, tm1D, tm1N], [tm2C, tm2D, tm2N]])
        
    return matches




def list_to_string(match_list, day, seed):
    # Takes the list of matches generated and converts into a string
    # match_list contains the raw values of the matches
    # day contains the datetime value starting at the start date
    match_time = 0 # 0 or 1 depending on which time slot will be used (used to pull time from global matchTimes var)
    sched = []
    sched.append("="*20 + " AXHL PRE SEASON SCHEDULE - Created by Dakota " + "="*20)
    sched.append("Seed: " + str(seed))
    sched.append(" ")
    
    for time_slot in match_list:
        # Skips days that wont have games
        while day.strftime("%A") not in gameDays:
            day = addDay(day)
            
        for match in time_slot:
            # written like this for readability
            matchStr = ""
            # add first match conf, div, name, respectively
            matchStr += str(match[0][0]) + ", " + str(match[0][1]) + ", " + str(match[0][2])
            # add vs separator
            matchStr += " VS "
            # add second match conf, div, name, respectively
            matchStr += str(match[1][0]) + ", " + str(match[1][1]) + ", " + str(match[1][2])
            # add time and date
            matchStr += " -> " + str(day) + ", " + str(matchTimes[match_time])
            # Add match to schedule
            sched.append(matchStr)
        # Add spacer after time slot
        sched.append(" ")
        match_time = [1, 0][match_time] # swap time slot time
        if(match_time == 0): # time slot sfor given day completed
            # iterate day
            day = addDay(day)
            # add readability divider
            sched.append("="*100)
            # add spacer
            sched.append(" ")
    return sched
        

        

def schedule_generator(weeks, startingDay, seed):
    # Generates the list of matches for date and time for the total number of weeks
    # Starts at the startingDay value (list in yr, month, day format) 
    # Since its random, the scheduler may not always succeed first try making a duplicate free schedule
    # So this function uses a try except block to prevent infinite looping and know when to retry
    schedule = []
    match_list = []
    
    # Using datetime module for built in calendar handling (can check day of week this way)
    day = datetime.date(startingDay[0], startingDay[1], startingDay[2])
    
    failed = True
    attempts = 0 # keeps track of number of times the scheduler has retried
    max_attempts = 100
    while failed:
        try:
            failed = False
            for _ in range(weeks * len(gameDays)):
                # Code below is for a single day of matches
                # For loop makes sure it runs for the total amount of days that need to be scheduled
                timeSlot1 = time_slot_generator(match_list)
                match_list.append(list(timeSlot1))
                timeSlot2 = time_slot_generator(match_list)
                match_list.append(list(timeSlot2))
        except:
            # scheduler could not find match that was not a duplicate
            failed = True
            # clear match_list twice to prevent any leakage
            while len(match_list) > 0:
                del match_list[-1]
            match_list = list()
            attempts += 1
            if attempts > max_attempts:
                # Tried to make schedule the max allowable times
                # Raises error to prevent looping
                # Should never get here but exists for worst case
                raise Exception("Scheduler failed to generate without duplicates. Try running program again")


    # TTL Matches check
    ttlMatches = len(team_names) * weeks * len(gameDays)
    matchCnt = 0
    for ts in match_list:
        matchCnt += len(ts)
    if ttlMatches != matchCnt:
        raise Exception("Number of matches generated is not what it should be. Req: " + str(ttlMatches) + ", Act: " + str(matchCnt))
    
    
    # Error Check for timeslots
    # Makes sure that the schedule didn't generate more than 1 match for a given team in each time slot
    for tm in team_names:
        for ts in match_list:
            cnt = 0
            for m in ts:
                # Should always find one match that satisfies the below condition, but not two
                if tm[2] == m[0][2] or tm[2] == m[1][2]:
                    cnt += 1
                    # Raise exception if found more than one
                    if cnt > 1:
                        raise Exception("Something went wrong. Duplicate team in time slot")
    
    print("")
    print("Pre Season Schedule Generated!")
    print("")
    
    # Dupe Tracking
    # Used to determine the ttl number of duplicate matches and the max number of times a team will play another
    # For Preseason it should always be 0             
    duped_match = []
    for ts1 in match_list:
        for match1 in ts1:
            already_done = False
            if len(duped_match) > 0:
                for duped in duped_match:
                    # Makes sure not to count the same match twice
                    if match1[0][2] == duped[0][0][2] and match1[1][2] == duped[0][1][2] or match1[0][2] == duped[0][1][2] and match1[1][2] == duped[0][0][2]:
                        already_done = True
            if not already_done:
                cnt = 0
                # loops through matches in match list a second time to compare the two and find all duplicates
                # will always find one (itself)
                for ts2 in match_list:
                    for match2 in ts2:
                        if match1[0][2] == match2[0][2] and match1[1][2] == match2[1][2] or match1[0][2] == match2[1][2] and match1[1][2] == match2[0][2]:
                            cnt += 1
                if cnt > 1:
                    # Adds match to list and the # of times a dupe was found
                    duped_match.append([match1, cnt])
    
    # printout
    print("Total Duplicate Matches: " + str(len(duped_match)))
    print("")
    schedule = list_to_string(match_list, day, seed)
    return schedule, match_list # Returns completed schedule as list
        



def main(testing = False):
    start_time = time.time()
    # PRE SEASON
    # Seeding for Schedule
    if autoseed:
        seed = random.randrange(sys.maxsize)
    else:
        seed = defSeed
    random.seed(seed)
    
    start_time = time.time()
    print("")
    print("Generating Pre Season Schedule. Please Wait...")
    print("Seed Used: " + str(seed))
    weeks = 1
    # Generate Schedule
    preSeasonSchedule, match_list = schedule_generator(weeks, startDayPreseason, seed)
    
    # Convert schedule to CSV
    print("Creating PreSeason CSV...")
    print("")
    df = pd.DataFrame(preSeasonSchedule)
    df.to_csv('Pre_Season_Schedule.csv', index=False, header=0)
    # Print time it takes to execute
    print("Execution took %s Seconds" % (time.time() - start_time))
    if testing:
        return match_list
        



if __name__ == "__main__":
    main()