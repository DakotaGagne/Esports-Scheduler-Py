
'''

# Regular Season Scheduler (AXHL)
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
The scheduler uses a number of factors to generate
Based on priority system
1st Priority: Even Home and Away matches
2nd Priority: Duplicate prevention (Duplicates are going to happen because there are fewer combinations than total matches, but this tries to space them out as much as possible)
3rd Priority: Distribution of matches (Same Div, Same Conf, Diff Conf) (See req_dist for specific distribution)

'''





# Imports
import random
import pandas as pd
import datetime
import time
import sys

# Declarations

defSeed = 8664124930412768677 # Default Seed to use if want repeatable results
autoseed = True # Set to True if want random results

'''

START OF CUSTOMIZABLE VARIABLES

'''

team_names = [
    # Can Change these values
    # Ensure that all divisions and conferences have the same number of teams

# P, C, M, A

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
["E-Conf", "A-Div", "Worcester Railers"]
]


gameDays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"] # List of weekdays on which games will be held. Can change to desired weekly sched
matchTimes = ["9:55PM EST", "10:35PM EST"] # Time slots for matches. Can change to desired time slots (must be 2 values)
startDayRegseason = [2024, 10, 20] # The starting day of the regular season schedule - Can be changed to desired start date

# Total Schedule Length
    # Default to ttlMatchPerTeam unless its 0
    
# Will base schedule off of ttlMatchPerTeam unless it is set to 0, then it will base sched off of weeks
weeks = 8 # Length of reg season
ttlMatchPerTeam = 60 # Total matches, if specified

# Inclusive start and end
# Can be a single date or a range
# EX single date: [2024, 10, 31]
# EX range: [[2024, 10, 31], [2024, 11, 28]]
# EX combined: [[2024, 10, 25], [[2024, 10, 31], [2024, 11, 08]], [2024, 11, 25]]
pausePointDates = []


# 26 Division, 24 intra conf, 32 inter conf
# 82 total
req_dist = {
    "same_div": 0.3050, # Within same conf and div
    "same_conf": 0.2950, # Diff div, same conf
    "diff_conf": 0.1000 # Diff conf (req dist her is per match combination (ttl 4))
}




'''

END OF CUSTOMIZABLE VARIABLES

'''


class TEAM:
    # Used to keep track of home and away matches for each team
    def __init__(self, conf, div, name):
        self.conf = conf
        self.div = div
        self.name = name
        self.home = 0
        self.away = 0

def addDay (date, d = 1): # Increments datetime var by 1 day, or more if specified
    return date + datetime.timedelta(days=d)




def fetch_random_team(): # Returns a random team from the list (specifically a list including conf, div, and name)
    randInd = random.randint(0, len(team_names)-1)
    return team_names[randInd]




def dist_calculator(curr_sched):
    
    # Calculates the distribution of matches for current schedule
    # Starts by adding up all matches
    
    dist = {
        "same_div": 0,
        "same_conf": 0,
        "diff_conf": {
            "A vs C": 0, # for atlantic div vs central div
            "A vs P": 0, # for atlantic div vs pacific div
            "M vs C": 0, # for metropolitan div vs central div
            "M vs P": 0 # for metropolitan div vs central div
        }
    }
    dist_ratios = {
        "same_div": 0,
        "same_conf": 0,
        "diff_conf": {
            "A vs C": 0, # for atlantic div vs central div
            "A vs P": 0, # for atlantic div vs pacific div
            "M vs C": 0, # for metropolitan div vs central div
            "M vs P": 0 # for metropolitan div vs central div
        }
    }
    ttl_matches = 0
    for time_slot in curr_sched:
        for match in time_slot:
            ttl_matches += 1
            if match[0][0] == match[1][0]: # same conf
                if match[0][1] == match[1][1]: # same div
                    dist["same_div"] += 1
                else:
                    dist["same_conf"] += 1
            else:
                if match[0][1] == "A-Div" or match[1][1] == "A-Div" and match[0][1] == "C-Div" or match[1][1] == "C-Div":
                    # Atlantic vs Central
                    dist["diff_conf"]["A vs C"] += 1
                elif match[0][1] == "A-Div" or match[1][1] == "A-Div" and match[0][1] == "P-Div" or match[1][1] == "P-Div":
                    # Atlantic vs Pacific
                    dist["diff_conf"]["A vs P"] += 1
                elif match[0][1] == "M-Div" or match[1][1] == "M-Div" and match[0][1] == "C-Div" or match[1][1] == "C-Div":
                    # Metropolitan vs Central
                    dist["diff_conf"]["M vs C"] += 1
                elif match[0][1] == "M-Div" or match[1][1] == "M-Div" and match[0][1] == "P-Div" or match[1][1] == "P-Div":
                    # Metropolitan vs Pacific
                    dist["diff_conf"]["M vs P"] += 1
                else:
                    raise Exception("Error when creating dist. Check schedule generation")
    
    # Create float value ratios
    dist_ratios["same_conf"] = float(dist["same_conf"]) / float(ttl_matches)
    dist_ratios["same_div"] = float(dist["same_div"]) / float(ttl_matches)
    dist_ratios["diff_conf"]["A vs C"] = float(dist["diff_conf"]["A vs C"]) / float(ttl_matches)
    dist_ratios["diff_conf"]["A vs P"] = float(dist["diff_conf"]["A vs P"]) / float(ttl_matches)
    dist_ratios["diff_conf"]["M vs C"] = float(dist["diff_conf"]["M vs C"]) / float(ttl_matches)
    dist_ratios["diff_conf"]["M vs P"] = float(dist["diff_conf"]["M vs P"]) / float(ttl_matches)
    return dist_ratios




def dist_difference(curr_dist):
    # Simply returns the required distribution minus the current
    # Less than 0 means more matches than needed, more than 0 means less
    diff = {}
    diff["same_div"] = req_dist["same_div"] - abs(curr_dist["same_div"])
    diff["same_conf"] = req_dist["same_conf"] - abs(curr_dist["same_conf"])
    diff["diff_conf"] = {}
    diff["diff_conf"]["A vs C"] = req_dist["diff_conf"] - abs(curr_dist["diff_conf"]["A vs C"])
    diff["diff_conf"]["A vs P"] = req_dist["diff_conf"] - abs(curr_dist["diff_conf"]["A vs P"])
    diff["diff_conf"]["M vs C"] = req_dist["diff_conf"] - abs(curr_dist["diff_conf"]["M vs C"])
    diff["diff_conf"]["M vs P"] = req_dist["diff_conf"] - abs(curr_dist["diff_conf"]["M vs P"])
    
    return diff
    
    
    
    
def rand_match_gen(teams):
    # Generates a valid random match and returns it
    # Called once for very first generated match
    dupe = True
    while dupe:
        tm1 = fetch_random_team()
        tm2 = fetch_random_team()
        if tm1[2] != tm2[2]:
            dupe = False
    for tm in teams:
        if tm.name == tm1[2]:
            tm.home += 1
        if tm.name == tm2[2]:
            tm.away += 1
    return [tm1, tm2], teams




def not_in_ts(ts, tm1, tm2):
    # Checks that a team is not in the timeslot
    # Returns True or False
    works = True
    if len(ts) != 0:
        for m in ts:
            if tm1[2] == m[0][2] or tm1[2] == m[1][2] or tm2[2] == m[0][2] or tm2[2] == m[1][2]:
                works = False
    return works
    
    


def fetch_pot_matches(curr_match_list, curr_ts_matches, priority, teams = []):
    
    # Generates a list of all matches that can be added next
    # Considers that a team cannot be chosen if in curr_ts_matches
    # Returns the list
    # Priority specifies what type of match should be chosen
    #   Defaults to a list of all types if a typed list is unable to generate
    #   (will frequently occur at match 11 and 12 of a timeslot)
    
    pot_matches = []
    # Same Conf, Same Div Match
    if priority == "home_away":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont
                    if not_in_ts(curr_ts_matches, tm1, tm2):
                        # valid match, now check home away
                        home_valid = False
                        away_valid = False
                        for tm in teams:
                            if tm.name == tm1[2]:
                                if tm.home <= tm.away:
                                    home_valid = True
                                
                            if tm.name == tm2[2]:
                                if tm.away <= tm.home:
                                    away_valid = True
                        if home_valid and away_valid:
                            pot_matches.append([tm1, tm2])
                        elif not home_valid and not away_valid:
                            pot_matches.append([tm2, tm1])
    
    
    elif priority == "same_div":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    if tm1[1] == tm2[1]:
                        # Valid match, check against curr_ts
                        if not_in_ts(curr_ts_matches, tm1, tm2):
                            pot_matches.append([tm1, tm2])
    
    # Same Conf, Diff Div Match                            
    elif priority == "same_conf":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    if tm1[0] == tm2[0] and tm1[1] != tm2[1]:
                        # Valid match, check against curr_ts
                        if not_in_ts(curr_ts_matches, tm1, tm2):
                            pot_matches.append([tm1, tm2])
    
    # Atlantic vs Central Match
    elif priority == "A vs C":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    if tm1[0] in ["A-Conf", "C-Conf"] and tm2[0] in ["A-Conf", "C-Conf"] and tm1[0] != tm2[0]:
                        # Valid match, check against curr_ts
                        if not_in_ts(curr_ts_matches, tm1, tm2):
                            pot_matches.append([tm1, tm2])
        
    elif priority == "A vs P":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    if tm1[0] in ["A-Conf", "P-Conf"] and tm2[0] in ["A-Conf", "P-Conf"] and tm1[0] != tm2[0]:
                        # Valid match, check against curr_ts
                        if not_in_ts(curr_ts_matches, tm1, tm2):
                            pot_matches.append([tm1, tm2])
        
    elif priority == "M vs C":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    if tm1[0] in ["M-Conf", "C-Conf"] and tm2[0] in ["M-Conf", "C-Conf"] and tm1[0] != tm2[0]:
                        # Valid match, check against curr_ts
                        if not_in_ts(curr_ts_matches, tm1, tm2):
                            pot_matches.append([tm1, tm2])
        
    elif priority == "M vs P":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    if tm1[0] in ["M-Conf", "P-Conf"] and tm2[0] in ["M-Conf", "P-Conf"] and tm1[0] != tm2[0]:
                        # Valid match, check against curr_ts
                        if not_in_ts(curr_ts_matches, tm1, tm2):
                            pot_matches.append([tm1, tm2])
        
    elif priority == "Rand":
        for tm1 in team_names:
            for tm2 in team_names:
                if tm1[2] != tm2[2]:
                    # not the same name so cont.
                    # rand match, so skip specific check and only check against curr_ts
                    if not_in_ts(curr_ts_matches, tm1, tm2):
                        pot_matches.append([tm1, tm2])        
    else:
        # Should never get here
        raise Exception("Priority value not recognized: " + priority)
    
    if len(pot_matches) == 0:
        # failed to find match that satisfies priority
        # finding any valid matches instead
        pot_matches = fetch_pot_matches(curr_match_list, curr_ts_matches, "Rand")
        
    if len(pot_matches) == 0:
        # Should never get here
        raise Exception("Error when generating potential matches -> Cant appear to find any match regardless of dist to fit")
           
    return pot_matches
   
   

def duplicate_prevention(match_list, pot_matches, force = True):
    # Algorithm to reduce duplicate matches
    # Starts at the most recent timeslot and works backwards
    # Only considers prev 4 timeslots total
    
    # Creates copy of pot_matches to avoid memory leaks
    
    
    pot_copy = [m for m in pot_matches]
    pot_res = []
    
    maxts = -4 # Max depth for the search (negative val just means start from the end of the schedule and work backwards)
    ts = -1 # Starter depth (latest ts)
    # Match List len check built in here for more versatile use of the function
    if len(match_list) <= 0:
        return pot_matches
    cont = True
    
    # Loop through each timeslot one at a time up to max depth (maxts)
    # Move any pot match not in the ts into a new list
    # If that list has any values at the end, over write the orig
    # Cont until reach max depth or end up with empty list
    # Force cond is used to return the best we came up with if True, and an empty list otherwise (occurs only when it fails b4 reaching max depth)
    while (len(match_list) > -1 * ts or ts >= maxts) and cont:
        if(ts < maxts-1):
            # Should not get here
            raise Exception("STOPPED INFIN LOOP")
        cont = False
        for potM in pot_copy:
            nonDupe = True
            for tsM in match_list[ts]:
                # Check names for each team in match in both directions (tm1 vs tm2 is the same as tm2 vs tm1) for all matches in timeslot
                if potM[0][2] == tsM[0][2] and potM[1][2] == tsM[1][2] or potM[0][2] == tsM[1][2] and potM[1][2] == tsM[0][2]:
                    nonDupe = False
            if nonDupe:
                # Not in time slot so add to pot_res
                pot_res.append(potM)
        if len(pot_res) >= 0:
            # Over write orig
            cont = True
            pot_copy.clear()
            pot_copy = [m for m in pot_res]
        ts -= 1
        
        if not cont:
            # Failed to reach max depth, so check if force is true
            if force:
                # Return the best we managed
                return pot_copy
            else:
                # Return empty list
                return []
        else:
            # Worked properly so can send final product with no issues
            return pot_copy




def time_slot_generator(match_list, teams):
    #LIKELY ADD TEAMS LIST AS INPUT HERE -------------------------------
    
    # Generates a list of matches for a single time slot
    # Will only work if the list of teams is an even number
    # Also reduces duplicates in the schedule
    
    # List containing all matches added to timeslot
    ts_matches = []
    
    # Used once, added for readability
    matchCnt = int(len(team_names)/2)
    # Loop through once for each match to add
    for _ in range(matchCnt):
        
        # Create a random match to add if its the first match of the schedule
        if len(match_list) == 0 and len(ts_matches) == 0:
            match, teams = rand_match_gen(teams)
            ts_matches.append(match)
        
        # Otherwise generate list of potential matches based on match priority
        # Same Div matches are top priority, then Same Conf, then Diff Conf ordered in opposite direction of the schedules usual gen
        #      When the schedule generates, A vs C and A vs P are always a higher percentage than M vs P and M vs C
        #      Flipped priority to help even it out. Still does not result in even distribution but seems like
        #       its due to all the restrictions placed on the schedule. Likely can be improved but haven't found a perfect solution yet
        else:
            # List to contain all potential matches generated
            pot_matches = []
            # First adds all time slots in match list, then adds the current timeslot matches at whatever point it is at in the gen
            comb_match_list = [ts for ts in match_list]
            # Add ts_matches if its not empty
            if len(ts_matches) > 0:
                comb_match_list.append(ts_matches)
            # Calculate current distribution of schedule, including curr time slot matches
            curr_dist = dist_calculator(comb_match_list)
            # Calculate difference of distribution (neg vals means too many, pos vals means too few)
            curr_dist_diff = dist_difference(curr_dist)
            
            # Check if too few Same Div matches first
            if curr_dist_diff["same_div"] > 0:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "same_div")
            
            # Then check if too few Same Conf matches
            elif curr_dist_diff["same_conf"] > 0:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "same_conf")
            
            # Then check if too few M vs P matches
            elif curr_dist_diff["diff_conf"]["M vs P"] > 0:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "M vs P")
            
            # Then check if too few M vs C matches    
            elif curr_dist_diff["diff_conf"]["M vs C"] > 0:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "M vs C")
            
            # Then check if too few A vs P matches   
            elif curr_dist_diff["diff_conf"]["A vs P"] > 0:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "A vs P")
            
            # Then check if too few A vs C matches 
            elif curr_dist_diff["diff_conf"]["A vs C"] > 0:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "A vs C")
            # In the case that none of the above conditions were satisfied,
            # Create a list of all possible matches (rand priority)
            else:
                pot_matches = fetch_pot_matches(match_list, ts_matches, "Rand")
            
            
            # Check if pot_matches contains matches
            if len(pot_matches) < 1:
                # Should never get here
                raise Exception("Returned potential matches has len 0. Current gen ts at failure: " + str(len(match_list)))
            else:
                # Duplicate checking
                # Should end up with fewer matches after duplicate prevention
                pot_matches = duplicate_prevention(match_list, pot_matches)
                if len(pot_matches) == 0:
                    # Dupe prevention failed with the current pot matches
                    # Try again with the random selector, and force the function to return the best it can do
                    pot_matches = fetch_pot_matches(match_list, ts_matches, "Rand")
                    pot_matches = duplicate_prevention(match_list, pot_matches, True)
                
                
                # SORT OPTIONS BY BEST FOR HOME AND AWAY
                ha_pot_matches = []
                
                for match in pot_matches:
                    home_valid = False
                    away_valid = False
                    for tm in teams:
                        # Home valid is true if a home match for this team would help equal things out
                        if tm.name == match[0][2]:
                            if tm.home <= tm.away:
                                home_valid = True
                        
                        # Away valid is true if an away match for this team would help equal things out
                        if tm.name == match[1][2]:
                            if tm.away <= tm.home:
                                away_valid = True
                    if home_valid and away_valid:
                        # If the match is beneficial for both, add to list
                        ha_pot_matches.append(match)
                    elif not home_valid and not away_valid:
                        # If the match is not beneficial for either, add to list in reverse order (if a home game would not help team 1, then an away game would, and vice versa)
                        ha_pot_matches.append([match[1], match[0]])
                
                
                
                if len(ha_pot_matches) == 0:
                    # None of the pot matches helped home and away balancing
                    # Specify pot matches based on ONLY matches that help home and away
                    ha_pot_matches = fetch_pot_matches(match_list, ts_matches, "home_away", teams)
                
                # Choose match at random from the thinned list
                ind = random.randint(0, len(ha_pot_matches)-1)
                
                m = ha_pot_matches[ind]
                
                # Iterate the values for the teams in the match
                for tm in teams:
                    if tm.name == m[0][2]:
                        tm.home += 1
                    if tm.name == m[1][2]:
                        tm.away += 1
                
                # Add to ts_matches
                ts_matches.append(m)    
    return ts_matches, teams




def list_to_string(match_list, day, seed):
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
            matchStr += "(HOME) " + str(match[0][0]) + ", " + str(match[0][1]) + ", " + str(match[0][2])
            # add vs separator
            matchStr += " VS "
            # add second match conf, div, name, respectively
            matchStr += "(AWAY) " + str(match[1][0]) + ", " + str(match[1][1]) + ", " + str(match[1][2])
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
    return sched


def schedule_generator(startingDay, seed):
    # General handler for schedule generation
    # Most of the actual generation happens in helper functions
    
    # Checks is the schedule should be based off of ttl number of weeks vs # of matches ttl
    weeks_based = (ttlMatchPerTeam == 0)
    
    schedule = []
    
    # List of all teams using a class
    # Used to keep track of home and away matches
    teams = []
    for tm in team_names:
        teams.append(TEAM(tm[0], tm[1], tm[2]))
    
    # Shuffles team list for the sake of the initial random match
    random.shuffle(team_names)
    
    match_list = []
    
    # Using datetime module for built in calendar handling (can check day of week this way)
    day = datetime.date(startingDay[0], startingDay[1], startingDay[2])
    
    seasonLength = 0 # Will equal total matches required, either weeks based or by a flat total
    if weeks_based:
        seasonLength = weeks * len(gameDays)
    else:
        seasonLength = int(ttlMatchPerTeam / 2)
    
    
    # SCHEDULE GENERATION LOOP
    for _ in range(seasonLength):
        # Code below is for a single day of matches
        # For loop makes sure it runs for the total amount of days that need to be scheduled
        
        timeSlot1, teams = time_slot_generator(match_list, teams)
        match_list.append(list(timeSlot1))
        timeSlot2, teams = time_slot_generator(match_list, teams)
        match_list.append(list(timeSlot2))        
            
    schedule = list_to_string(match_list, day, seed)
    
    return schedule, match_list, teams # Returns completed schedule in string form and list
        



'''
    TO-DO
    Try to determine why nhl schedule fails to balance matches outside of conference
'''                      

def dupeTracker(match_list, debug = False):
    # Checker that checks all duplicate matches in schedule that are 1 timeslot away from each other
    # Ideally comes up as none
    # debug var used to list all duplicate matches for debugging purposes
    cnt = 0
    for ts in range(len(match_list)-2):
        for m1 in range(len(match_list[ts])-1):
            for m2 in range(len(match_list[ts+1])-1):
                match1 = match_list[ts][m1]
                match2 = match_list[ts+1][m2]
                teams = [match1[0][2], match1[1][2]]
                if match2[0][2] not in teams:
                    teams.append(match2[0][2])
                if match2[1][2] not in teams:
                    teams.append(match2[1][2])
                if len(teams) == 2:
                    cnt += 1
                    if debug:
                        print("DUPLICATE OCCURED AT TS " + str(ts) + " and TS " + str(ts+1))
                        print("->" + str(match1) + "<- " + " ->" + str(match2) + "<-")
    if cnt == 0:
        print("No B2B Duplicates Found!!")
    else:
        print("Found " + str(cnt) + " B2B Duplicates")



def main(testing = False):
    # Seeding for Schedule
    if autoseed:
        seed = random.randrange(sys.maxsize)
    else:
        seed = defSeed
    random.seed(seed)
    
    start_time = time.time()
    print("")
    print("Generating Regular Season Schedule. Please Wait...")
    print("Seed Used: " + str(seed))
    
    # Generate Schedule
    regSeasonSchedule, match_list, teams = schedule_generator(startDayRegseason, seed)
              
    # Printout final distribution for testing purposes
    dist_ratios = dist_calculator(match_list)
    print("")
    print("")
    print("Regular Season Schedule Generated!")
    print("")
    print("Total Time Slots / Matches Per Team: " + str(len(match_list)))
    print("")
    print("Final Distribution:")
    print("")
    print(dist_ratios)
    print("")
    print("")
    # Convert schedule to CSV
    
    # TTL Matches check
    if ttlMatchPerTeam == 0:
        ttlMatches = len(team_names) * weeks * len(gameDays)
    else: 
        ttlMatches = len(team_names) * ttlMatchPerTeam / 2
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
    
    
    print("DUPLICATE MATCHES...")
    # Dupe Tracking
    # Used to determine the ttl number of duplicate matches and the max number of times a team will play another
    # Gives an idea of the effectiveness of the duplicate_prevention function
    # duped_match will contain all matches that have duplicates
    #   used to prevent recounting the same matches
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
    
    # Reduces the discovered matches to those with more than 2 occurences
    # Done because duplicates are impossible to prevent in a season of this size and the focus are those that occur a decent amount of times
    duped_thinned = []
    for dupe in duped_match:
        if dupe[1] > 2:
            duped_thinned.append(dupe)
    
    # printout
    print("Total Duplicate Matches: " + str(len(duped_thinned)))
    
    # Figure out which matches occur the most, then list them
    dupeCnt = 0
    most_duped = -1
    for m in duped_thinned:
        if m[1] > dupeCnt:
            dupeCnt = m[1]
    print("")
    print("The following matches occur the most at " + str(dupeCnt) + " times")
    for m in duped_thinned:
        if m[1] == dupeCnt:
            print(m[0])
    print("")
    
    # Check for B2B Dupes
    dupeTracker(match_list, False)
    
    # Even Home and Away check
    uneven = []
    for tm in teams:
        if tm.home != tm.away:
            uneven.append(tm)
    if len(uneven) != 0:
        print("The Following Matches Failed to Have Even Home and Away Matches:")
        for tm in uneven:
            print(tm.name + " -> Home: " + str(tm.home) + " Away: " + str(tm.away))
    else:
        print("All Matches Have Equal Home and Away Games")

    # Create CSV file for schedule
    print("Creating RegSeason CSV...")
    df = pd.DataFrame(regSeasonSchedule)
    df.to_csv('Reg_Season_Schedule.csv', index=False, header=0)    
    
    # Print time it takes to execute
    print("Execution took %s Seconds" % (time.time() - start_time))
    if testing:
        return match_list
    
    
if __name__ == "__main__":
    main()