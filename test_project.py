import pytest
from project import default_data, split_tasks, calculate_level

def test_default_data():
    data = default_data()
    assert "profile" in data
    assert "categories" in data
    assert "tasks" in data
    assert "habits" in data
    assert "meta" in data
    assert data["profile"]["name"] == None
    assert data["profile"]["age"] == None
    assert data["profile"]["xp"] == 0

def test_split_tasks():
    data = default_data()
    data["tasks"] = [
        {"name": "Task 1", "done": False},
        {"name": "Task 2", "done": True},
        {"name": "Task 3", "done": False},
        ]
    active, completed = split_tasks(data)
    assert len(active) == 2
    assert len(completed) == 1
    assert active[0]["name"] == "Task 1"
    assert active[1]["name"] == "Task 3"
    assert completed[0]["name"] == "Task 2"

def test_calculate_level():
    assert calculate_level(0) == 1
    assert calculate_level(50) == 1
    assert calculate_level(100) == 2
    assert calculate_level(250) == 3
    assert calculate_level(999) == 10
