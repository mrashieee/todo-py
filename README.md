# ToDo Manager
#### Video Demo: <https://youtu.be/QZYQyy1bALU?si=_F5MraZoFHuvhkEV>
#### Description:

This is my final project for CS50P. It's a gamified to-do and habit tracker that lives right in your terminal. You earn XP for getting things done, and the more XP you pile up, the higher your level goes. The formula is simple: `level = xp // 100 + 1`. So 0 XP puts you at level 1, and once you cross 100, you're level 2 — like a video game, but for real life.

## How It All Works

When you fire up `python project.py`, the first thing it does is load your saved data from a JSON file. If the file doesn't exist or is corrupted, it creates a fresh slate with some sensible defaults. Then it checks if any daily, weekly, or monthly resets are due — so recurring tasks reappear and habit counters zero out when they should. After that, if you haven't set up your profile yet, it asks for your name and age. Once that's done, you land on the main menu with four options: Tasks, Habits, Profile, and Exit.

## Tasks

The task system is the heart of the app. You can add tasks with a name, a category (like Work or Health), and a recurrence pattern — none, daily, weekly, or monthly. Each category has a base XP value, and the recurrence type gives it a multiplier. A one-off task gives standard XP, but a monthly task gives way more because it's a bigger commitment.

Once a task is created, it sits in your Active list. Mark it done and the XP gets added to your profile. If you accidentally mark the wrong thing, toggling it back subtracts the XP — so your score is always honest. You can also remove tasks one by one or wipe out a whole list at once.

## Habits

Habits are for the small stuff you want to do every day. You add one the same way as a task — pick a name and a category — and then log it each time you do it. Every log earns you XP and bumps the counter. If you fall off the wagon, there's a reset option that zeros everything out and adjusts your XP accordingly. No shame.

## Profile & Categories

Your profile shows your name, age, current level, and XP. You can change your name or age anytime, and the level always updates automatically.

Categories are what give each task and habit its XP value. The defaults are Work (30), Health (20), Learning (25), Productivity (15), and Personal (10). But you can add your own with any XP value between 1 and 100. You can also remove or reset categories anytime.

## Persistence

Everything saves automatically to a JSON file after every change. The load function handles missing or corrupted files gracefully — it just starts over with defaults. The recovery system on startup also checks if recurring tasks need to be reset based on how much time has passed.

## Testing

The project includes three tests using pytest. One checks that the default data structure has all the right keys and starting values. Another verifies that tasks are split correctly into active and completed lists. The third tests the level calculation formula with a handful of values. All three pass.

## Design Decisions

I used `title()` for category names to avoid duplicates from case differences. I capped custom category XP at 100 so users can't break the game balance. Level is calculated on the fly instead of stored, so it's always accurate. XP is subtracted when tasks are uncompleted or habits are reset — no cheating the system. And the recurrence multipliers reward longer-term commitments with higher XP.

The only dependency is pytest. Everything else is Python's standard library.
