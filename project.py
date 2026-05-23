import os
import sys
import json
from datetime import date

DATA_FILE = ".ToDoManager_data.json"

RECURRENCE_XP = {
    "none": 1.0,
    "daily": 1.5,
    "weekly": 2.0,
    "monthly": 5.0,
}

def default_data():
    return {
    "profile": {
        "name": None,
        "age": None,
        "xp": 0,
    },
    "categories": {
        "Work": 30,
        "Health": 20,
        "Learning": 25,
        "Productivity": 15,
        "Personal": 10,
    },
    "tasks": [],
    "habits": [],
    "meta": {
        "last_daily_reset": None,
        "last_weekly_reset": None,
        "last_monthly_reset": None,
    },
}

def ensure_profile(data):
    if (data["profile"]["name"] is not None):
        return
    clear()
    print("=== Setup Profile ===")
    name = input("Name: ").strip().title()
    age = input("Age: ").strip()
    data["profile"]["name"] = (name or "User")
    if age.isdigit():
        data["profile"]["age"] = int(age)
    save_data(data)

def calculate_level(xp):
    return xp // 100 + 1

def split_tasks(data):
    active = []
    completed = []
    for task in data['tasks']:
        if not task['done']:
            active.append(task)
        else:
            completed.append(task)
    return active,completed

def view_tasks(data = None):
    if data is None:
        data = load_data()
    print("=== Tasks ===")
    if not data["tasks"]:
        print("\n(no tasks available)")
    else:
        active, completed = split_tasks(data)
        print("\n--- Active Tasks ---\n")
        if not active:
            print("(no tasks available)")
        for i, task in enumerate(active, 1):
            print(f"[{i}] {task['name']}({task['category']}[{task['xp']}])")
        print("\n--- Completed Tasks ---\n")
        if not completed:
            print("(no tasks completed)")
        for task in completed:
            print(f"[x] {task['name']}({task['category']}[{task['xp']}])")

def task_menu():
    while True:
        clear()
        view_tasks()
        print("\n================\n"
              "(A)dd Tasks\n"
              "(R)emove Tasks\n"
              "(T)oggle Done\n"
              "(M)enu")
        choice = input("\nChoice: ").strip().lower()
        match choice:
            case "a" | "add":
                add_tasks()
            case "r" | "remove":
                remove_tasks()
            case "t" | "toggle":
                toggle_tasks()
            case "m" | "menu":
                clear()
                return
            case _:
                input("Invalid Input. Press Enter...")

def add_tasks():
    while True:
        clear()
        data = load_data()
        view_tasks(data)
        usr_input: str =input("\nEnter task name(0 to cancel): ").strip().lower()
        match usr_input:
            case "0" | "cancel" | "":
                clear()
                return
            case _:
                task_name = usr_input
                cats = list(data["categories"].keys())
                while True:
                    task_category = input(f"Enter Category[{', '.join(cats)}]: ").strip().title() or "Personal"
                    if task_category in cats:
                        break
                    input("Invalid Category. Press Enter...")
                    clear()
                    view_tasks(data)
                    print(f"Enter task name: {task_name}")
                rec = list(RECURRENCE_XP.keys())
                while True:
                    task_recurrence = input(f"Enter Recurrence({', '.join(rec)}): ").strip().lower() or "none"
                    if task_recurrence in rec:
                        break
                    input("Invalid Recurrence. Press Enter...")
                    clear()
                    view_tasks(data)
                    print(f"Enter task name: {task_name}")
                    print(f"Enter Category: {task_category}")
                base_xp = data["categories"][task_category]
                xp = int(base_xp * RECURRENCE_XP[task_recurrence])
                task = {
                    "name": task_name,
                    "category": task_category,
                    "done": False,
                    "xp": xp,
                    "recurrence": task_recurrence,
                    "created": date.today().isoformat(),
                }
                data["tasks"].append(task)
                save_data(data)
                return

def remove_tasks():
    data = load_data()
    active, completed = split_tasks(data)
    choice = input("\nRemove task from (a)ctive or (c)ompleted (0 to cancel): ").strip().lower()
    match choice:
        case "0" | "cancel" | "":
            return
        case "a" | "active":
            tasks = active
            label = "active"
        case "c" | "completed":
            tasks = completed
            label = "completed"
        case _:
            return
    if not tasks:
        input(f"No {label} tasks. Press Enter...")
        return
    clear()
    print(f"--- {label.title()} ---\n")
    for i, task in enumerate(tasks, 1):
        status = f"[{i}]" if not task["done"] else f"{i}. [x]"
        print(f"{status} {task['name']}({task['category']}[{task['xp']}])")
    choice = input("\nTask to remove(c to cancel): ").strip().lower()
    match choice:
        case "c" | "cancel" | "":
            return
        case "all":
            confirm = input(f"Remove all {len(tasks)} {label} tasks? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                for task in tasks:
                    data["tasks"].remove(task)
                save_data(data)
            return
        case _:
            try:
                num = int(choice)
                if 1 <= num <= len(tasks):
                    data["tasks"].remove(tasks[num - 1])
                    save_data(data)
                    return
                else:
                    input("Invalid Number. Press Enter...")
            except ValueError:
                input("Invalid input. Press Enter...")

def toggle_tasks():
    data = load_data()
    active, completed = split_tasks(data)
    choice = input("\nMark task from (a)ctive or (c)ompleted (0 to cancel): ").strip().lower()
    match choice:
        case "0" | "cancel":
            return
        case "a" | "active":
            tasks = active
            label = "active"
        case "c" | "completed":
            tasks = completed
            label = "completed"
        case _:
            return
    if not tasks:
        input(f"No {label} tasks. Press Enter...")
        return
    clear()
    print(f"--- {label.title()} ---\n")
    for i, task in enumerate(tasks, 1):
        status = f"[{i}]" if not task["done"] else f"{i}. [x]"
        print(f"{status} {task['name']}({task['category']}[{task['xp']}])")
    choice = input("\nTask to toggle(c to cancel): ")
    match choice:
        case "c" | "cancel":
            return
        case "all":
            confirm = input(f"Toggle all {len(tasks)} {label} tasks? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                for task in tasks:
                    if not task["done"]:
                        data["profile"]["xp"] += task["xp"]
                    else:
                        data["profile"]["xp"] -= task["xp"]
                    task["done"] = not task["done"]
                save_data(data)
            return
        case _:
            try:
                num = int(choice)
                if 1 <= num <= len(tasks):
                    task = tasks[num - 1]
                    if not task["done"]:
                        data["profile"]["xp"] += task["xp"]
                    else:
                        data["profile"]["xp"] -= task["xp"]
                    task["done"] = not task["done"]
                    save_data(data)
                    return
                else:
                    input("Invalid Number. Press Enter...")
            except ValueError:
                input("Invalid Input. Press Enter...")

def view_habits(data = None):
    if data is None:
        data = load_data()
    print("=== Habits ===\n")
    if not data["habits"]:
        print("(no habits available)")
    else:
        for i, habit in enumerate(data["habits"], 1):
            print(f"[{i}] {habit['name']}({habit['category']}[{habit['xp']}]): {habit['count']}")

def habit_menu():
    while True:
        clear()
        view_habits()
        print("\n================\n"
              "(A)dd Habits\n"
              "(R)emove Habits\n"
              "(L)og Entry\n"
              "(M)enu")
        choice = input("\nChoice: ").strip().lower()
        match choice:
            case "a" | "add":
                add_habits()
            case "r" | "remove":
                remove_habits()
            case "l" | "log":
                log_habits()
            case "m" | "menu":
                clear()
                return
            case _:
                input("Invalid Input. Press Enter...")

def add_habits():
    while True:
        clear()
        data = load_data()
        view_habits(data)
        usr_input = input("\nEnter habit name(0 to cancel): ").strip().lower()
        match usr_input:
            case "0" | "cancel" | "":
                clear()
                return
            case _:
                habit_name = usr_input
                cats = list(data["categories"].keys())
                while True:
                    habit_category = input(f"Enter Category({", ".join(cats)}): ").strip().title() or "Personal"
                    if habit_category in cats:
                        break
                    input("Invalid Category. Press Enter...")
                    clear()
                    view_habits(data)
                    print(f"Enter habit name: {habit_name}")
                base_xp = data["categories"][habit_category]
                xp = int(base_xp * RECURRENCE_XP["daily"])
                habit = {
                    "name": habit_name,
                    "category": habit_category,
                    "count": 0,
                    "xp": xp,
                    "last_reset": date.today().isoformat(),
                    "created": date.today().isoformat(),
                }
                data["habits"].append(habit)
                save_data(data)
                return

def remove_habits():
    clear()
    data = load_data()
    habits = data["habits"]
    view_habits(data)
    choice = input("\nHabit to remove(c to cancel): ").strip().lower()
    match choice:
        case "c" | "cancel" | "":
            return
        case "all":
            confirm = input(f"Remove all habits? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                for habit in habits:
                    data["habits"].remove(habit)
                save_data(data)
            return
        case _:
            try:
                num = int(choice)
                if 1<= num <= len(habits):
                    data["habits"].remove(habits[num-1])
                    save_data(data)
                    return
                else:
                    input("Invalid Number. Press Enter...")
            except ValueError:
                input("Invalid Input. Press Enter...")

def log_habits():
    clear()
    data = load_data()
    habits = data["habits"]
    view_habits(data)
    choice = input("\nHabit to log(c to cancel): ").strip().lower()
    match choice:
        case "c" | "cancel":
            return
        case "reset":
            confirm = input(f"Reset all habits? (y/n): ").strip().lower()
            if confirm in ("y", "yes"):
                for habit in habits:
                    data["profile"]["xp"] -= habit["xp"] * habit["count"]
                    habit["count"] = 0
                save_data(data)
            return
        case _:
            try:
                num = int(choice)
                if 1 <= num <= len(habits):
                    habit = habits[num - 1]
                    data["profile"]["xp"] += habit["xp"]
                    habit["count"] += 1
                    save_data(data)
                    return
                else:
                    input("Invalid Number. Press Enter...")
            except ValueError:
                input("Invalid Input. Press Enter...")

def view_profile(data = None):
    if data is None:
        data = load_data()
    profile = data["profile"]
    print("=== Profile ==="
          f"\nName: {profile["name"]}"
          f"\nAge: {profile["age"]}"
          f"\nLevel: {calculate_level(profile["xp"])}[{profile["xp"]}]"
          f"\nCategories: {len(data["categories"])}"
          f"\nRecursions Available: {", ".join(list(RECURRENCE_XP.keys()))}"
          )

def profile_menu():
    while True:
        clear()
        view_profile()
        print("\n================\n"
              "Change (N)ame\n"
              "Change (A)ge\n"
              "Manage (C)ategory\n"
              "(R)eset Profile\n"
              "(M)enu")
        choice = input("\nChoice: ").strip().lower()
        match choice:
            case "n" | "name":
                change_name()
            case "a" | "age":
                change_age()
            case "c" | "category":
                manage_category()
            case "r" | "reset":
                reset_profile()
            case "m" | "menu":
                clear()
                return
            case _:
                input("Invalid Input. Press Enter...")

def change_name():
    clear()
    data = load_data()
    print("=== Name Change ===\n")
    new_name = input(f"Name({data['profile']['name']}): ").title() or data["profile"]["name"]
    data["profile"]["name"] = new_name
    save_data(data)

def change_age():
    data = load_data()
    while True:
        try:
            clear()
            print("=== Age Change ===\n")
            new_age = int(input(f"Age({data['profile']['age']}): ")) or data["profile"]["age"]
            break
        except ValueError:
            input("Invalid Input. Press Enter...")
    data["profile"]["age"] = new_age
    save_data(data)

def manage_category():
    while True:
        clear()
        data=load_data()
        print("=== Categories ===\n")
        for category, xp in data["categories"].items():
            print(f"{category}: {xp}")
        print("\n================\n"
              "(A)dd Category\n"
              "(R)emove Category\n"
              "(Reset) Category\n"
              "(M)enu")
        choice = input("\nChoice: ").strip().lower()
        match choice:
            case "a" | "add":
                add_category()
            case "r" | "remove":
                remove_category()
            case "reset":
                reset_category()
            case "m" | "menu":
                clear()
                return
            case _:
                input("Invalid Input. Press Enter...")

def reset_profile():
    clear()
    data = load_data()
    print("=== Reset Profile ===")
    confirm = input(f"Confirmation:\nThis will reset your whole profile[{data["profile"]["name"]}] (y/n): ").strip().lower()
    match confirm:
        case "y" | "yes":
            data = default_data()
            ensure_profile(data)
            save_data(data)
        case _:
            return

def add_category():
    while True:
        clear()
        data = load_data()
        print("=== Categories ===\n")
        for category, xp in data["categories"].items():
            print(f"{category}: {xp}")
        category_name = input("\nEnter Category Name(0 to cancel): ").strip().title()
        match category_name:
            case "0" | "cancel" | "":
                return
            case _ if category_name in data["categories"]:
                input(f"Category {category_name} already exists. Press Enter...")
            case _:
                while True:
                    try:
                        category_xp = int(input(f"XP for '{category_name}':"))
                        if 1 <= category_xp <= 100:
                            break
                        input("XP must be between 1 and 100.")
                    except ValueError:
                        input("Invalid Number. Press Enter...")
                data["categories"][category_name] = category_xp
                save_data(data)

def remove_category():
    while True:
        clear()
        data = load_data()
        print("=== Categories ===\n")
        for category, xp in data["categories"].items():
            print(f"{category}: {xp}")
        category_name = input("\nCategory Name(0 to cancel): ").strip().title()
        match category_name:
            case "0" | "cancel" | "":
                return
            case _ if category_name in data["categories"]:
                data["categories"].pop(category_name)
                input(f"{category_name} Removed...")
                save_data(data)
            case _:
                input(f"Category {category_name} doesn't exists. Try Again...")

def reset_category():
    while True:
        data = load_data()
        confirm = input("Reset Category (y/n): ").strip().lower()
        if confirm in ("y", "yes"):
            data["categories"] = {
                "Work": 30,
                "Health": 20,
                "Learning": 25,
                "Productivity": 15,
                "Personal": 10,
            }
        save_data(data)
        return

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_data():
    if not os.path.exists(DATA_FILE):
        data = default_data()
        save_data(data)
        return data
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        data = default_data()
        save_data(data)
        return data

def apply_recurrence(data):
    today = date.today()
    meta = data["meta"]
    if meta["last_daily_reset"]:
        last = date.fromisoformat(meta["last_daily_reset"])
        if (today - last).days >= 1:
            for habit in data["habits"]:
                if habit["last_reset"] != today.isoformat():
                    habit["count"] = 0
                    habit["last_reset"] = today.isoformat()
            for task in data["tasks"]:
                if task["done"] and task["recurrence"] == "daily":
                    task["done"] = False
            meta["last_daily_reset"] = today.isoformat()
    else:
        meta["last_daily_reset"] = today.isoformat()
    if meta["last_weekly_reset"]:
        last = date.fromisoformat(meta["last_weekly_reset"])
        if (today - last).days >= 7:
            for task in data["tasks"]:
                if task["done"] and task["recurrence"] == "weekly":
                    task["done"] = False
            meta["last_weekly_reset"] = today.isoformat()
    else:
        meta["last_weekly_reset"] = today.isoformat()
    if meta["last_monthly_reset"]:
        last = date.fromisoformat(meta["last_monthly_reset"])
        if (today - last).days >= 30:
            for task in data["tasks"]:
                if task["done"] and task["recurrence"] == "monthly":
                    task["done"] = False
            meta["last_monthly_reset"] = today.isoformat()
    else:
        meta["last_monthly_reset"] = today.isoformat()
    save_data(data)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    data = load_data()
    apply_recurrence(data)
    ensure_profile(data)
    while True:
        clear()
        print(
            "=== ToDo Manager ==="
            "\n(T)asks"
            "\n(H)abits"
            "\n(V)iew Profile"
            "\n(E)xit"
            "\n====================\n"
            )
        choice = input("Choice: ").strip().lower()
        match choice:
            case "t" | "tasks":
                task_menu()
            case "h" | "habits":
                habit_menu()
            case "v" | "view" | "profile":
                profile_menu()
            case "e" | "exit":
                clear()
                sys.exit()
            case _:
                input("Invalid. Press Enter...")

if __name__ == "__main__":
    main()
