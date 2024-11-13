# Esports Scheduler

This repository contains three Python scripts designed to generate schedules for an Esports Hockey League. Each script serves a different purpose: generating a pre and reg season schedule for NHL Seasons, and a Round Robin schedule for Fifa.

## Usage

1. Ensure Python3 is installed on your computer.
2. Open CMD Terminal or Powershell.
3. Type `pip install pandas` and press enter.
4. Navigate to the folder containing the schedule file.
5. Right-click on explorer, and select "Open in Terminal".
6. Type `python (schedule_name).py` and press enter.
7. Check the folder for the generated schedule in CSV format.

## Files

### 1. `fifa_scheduler.py`

This script generates a round-robin style schedule for a FIFA league. Each team plays every other team a specified number of times, with two timeslots per day.

#### Notes

- Each team plays every other team exactly `TIMES_TO_PLAY` times.
- Each team plays twice per day.
- No conferences or divisions are considered.
- Output format is CSV.

### 2. `reg_season_scheduler.py`

This script generates a regular season schedule for the AXHL (Esports Hockey League). The schedule is based on a priority system to ensure even home and away matches, duplicate prevention, and distribution of matches.

#### Notes

- The scheduler uses a number of factors to generate the schedule based on a priority system.
- The schedule includes conferences and divisions.
- Output format is CSV.

### 3. `pre_season_scheduler.py`

This script generates a pre-season schedule for the AXHL. The schedule is designed for a single week of games with the highest priority being to prevent duplicate matches.

#### Notes

- The scheduler is designed to generate a schedule for a single week of games.
- Home and away matches are not considered.
- Output format is CSV.

## Customizable Variables

Each script contains a section for customizable variables where you can adjust team names, the number of times each team plays, game days, match times, and other relevant settings.

## Author

Created by Dakota Gagne. Asking before using this program is appreciated.
