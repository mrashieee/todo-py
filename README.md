# ToDo Manager
#### Video Demo:  <https://youtu.be/your-video-id-here>
#### Description:

this is my final project for CS50P. its a gamified terminal-based todo and habit manager that awards xp for getting things done. the more xp you earn the higher your level goes using the formula level = xp // 100 + 1.

**How the program works from start to finish:**

when you run python project.py the first thing that happens is load_data() which checks if ToDoManager_data.json exists. if it doesnt it calls default_data() to create the initial structure and saves it. if the file is corrupted it does the same. then apply_recurrence() runs and checks if its time for daily weekly or monthly resets so tasks reappear and habit counters zero out. then ensure_profile() checks if your name is set. if not it prompts you to set up your name and age. after all that the main menu loop starts showing the options for tasks habits profile and exit.

**project.py — all functions explained:**

default_data() returns a dictionary with the starting structure. it has a profile with name age and xp set to 0. it has five default categories Work (30 xp) Health (20) Learning (25) Productivity (15) and Personal (10). tasks and habits start as empty lists. meta tracks the last reset dates for daily weekly and monthly recurrence.

ensure_profile(data) checks if the profiles name is already set. if not it clears the screen shows a setup screen and asks for name and age. it defaults the name to User and only stores age if its a valid digit.

calculate_level(xp) takes your total xp and returns xp // 100 + 1. so 0 xp is level 1, 100 xp is level 2, 250 xp is level 3.

split_tasks(data) loops through all tasks and separates them into two lists active ones where done is False and completed ones where done is True. the view functions use this to show a clean display.

view_tasks(data) prints the task list split into active and completed sections. shows each task with its name category and xp value. if there are no tasks it says so.

task_menu() is the loop for the task section. it shows the current tasks then asks if you want to add remove toggle or go back to the main menu. any invalid input shows an error and loops.

add_tasks() starts by showing current tasks then asks for a task name. if you enter 0 or cancel it returns. otherwise it asks for a category from the existing ones and a recurrence type from none daily weekly or monthly. it calculates the tasks xp by multiplying the categorys base xp by the recurrence multiplier defined in RECURRENCE_XP. the task is saved with name category done status xp recurrence and creation date.

remove_tasks() asks if you want to remove from active or completed tasks then shows the list. you can remove a single task by number or all tasks with confirmation. it removes from the main data tasks list.

toggle_tasks() marks tasks as done or undone. when you mark an active task as done the tasks xp is added to your profile xp. when you mark a completed task as undone the xp is subtracted. this keeps the numbers accurate.

view_habits(data) shows the habit list with each habits name category xp and current count.

habit_menu() is the loop for the habit section with options to add remove log or go back.

add_habits() works like add_tasks but for habits. it asks for a name and category then creates a habit with xp based on the category times the daily multiplier. habits start with count 0 and track their last reset date.

remove_habits() lets you remove a single habit by number or all at once with confirmation.

log_habits() increments a habits count and adds its xp to your profile. it also has a reset option that subtracts all xp earned from all habits and sets their counts back to 0 for a fresh start.

view_profile(data) shows your name age calculated level with current xp how many categories you have and what recurrence types are available.

profile_menu() is the loop for the profile section with options to change name change age manage categories reset profile or go back.

change_name() prompts for a new name and defaults to the current one if nothing is entered.

change_age() prompts for a new age with input validation. it loops until you enter a valid integer.

manage_category() shows all categories with their xp values and gives options to add remove reset or go back.

reset_profile() asks for confirmation then resets everything to defaults by calling default_data() and ensure_profile().

add_category() asks for a category name and validates it doesnt already exist. then it asks for an xp value between 1 and 100. the name is stored in title case for consistency.

remove_category() asks for a category name and removes it from the dictionary. it also uses title case to match how categories are stored.

reset_category() with confirmation restores the five default categories and their original xp values.

save_data(data) opens the json file and writes the entire data dictionary with indentation for readability.

load_data() checks if the file exists. if not it creates it with defaults. it tries to load the json and if parsing fails it falls back to defaults. this way a corrupted file doesnt break the program.

apply_recurrence(data) is called on startup. it checks each reset type by comparing the stored last reset date with todays date. daily resets happen if at least 1 day has passed. they reset habit counts and set daily tasks back to undone. weekly resets happen after 7 days and uncomplete weekly tasks. monthly resets happen after 30 days and uncomplete monthly tasks. the first time each reset type runs it just sets the initial date without doing any resets.

clear() runs the appropriate terminal clear command for windows or linux and macos.

main() loads the data runs apply_recurrence and ensure_profile then shows the main menu loop. it dispatches to task_menu habit_menu or profile_menu based on input and exits cleanly on the exit option.

**test_project.py — how testing works:**

test_default_data() creates a default data structure and asserts that all five main keys exist and that name is None age is None and xp is 0.

test_split_tasks() creates a sample data with three tasks two active and one completed. it asserts that split_tasks returns two lists with the correct lengths and that the specific tasks end up in the right lists.

test_calculate_level() tests the level formula with multiple values to verify that 0 xp gives level 1, 50 gives level 1, 100 gives level 2, 250 gives level 3, and 999 gives level 10.

**requirements.txt** contains only pytest since the entire project uses nothing beyond Python's standard library.

**Design choices i made:**

I used title() consistently for category names to prevent duplicates caused by case differences. I capped custom category xp at 100 so users cant break the game balance by setting a category to a huge number. I calculate level on the fly instead of storing it in the json file so the display is always accurate even if xp changed outside the normal flow. I subtract xp when tasks are uncompleted or habits are reset so the xp total always reflects actual progress. The recurrence multipliers give higher xp for less frequent tasks which rewards commitment to long-term goals.
