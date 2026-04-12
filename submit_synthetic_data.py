#!/usr/bin/env python3

import requests
import random
from typing import Dict, List, Any

SHOTS_URL = 'https://api.datadunkers.ca/api/collections/data_skaters_shots/records'
TRAITS_URL = 'https://api.datadunkers.ca/api/collections/data_skaters_traits/records'

# Manitoba-themed first and last names
FIRST_NAMES = [
    'Alex', 'Bailey', 'Casey', 'Dakota', 'Elliott', 'Finley', 'Grayson', 'Harper',
    'Indigo', 'Jordan', 'Kai', 'Logan', 'Morgan', 'Noelle', 'Owen', 'Parker',
    'Quinn', 'Riley', 'Sage', 'Taylor', 'Uma', 'Veda', 'Wade', 'Xander',
    'Yael', 'Zara', 'Aaron', 'Brit', 'Cole', 'Dana', 'Evan', 'Faye',
    'Gavin', 'Hailey', 'Isaac', 'Jensen', 'Keith', 'Liam', 'Marcus', 'Nate',
    'Oscar', 'Priya', 'Rory', 'Skylar', 'Tyler', 'Umar', 'Violet', 'Wyatt',
    'Xena', 'Yuri', 'Ziggy', 'Adrian', 'Blake', 'Cameron', 'Devin', 'Ezra',
]

LAST_NAMES = [
    'Anderson', 'Bergstrom', 'Chen', 'Doppler', 'Eriksen', 'Fitzpatrick',
    'Goldstein', 'Harris', 'Iverson', 'Jackson', 'Kowalski', 'Larson',
    'Malone', 'Nelson', 'O\'Brien', 'Peterson', 'Ramirez', 'Schmidt',
    'Thompson', 'Underwood', 'Valenzuela', 'Westbrook', 'Yamamoto', 'Zhang',
]

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

HANDEDNESS = ['left', 'right', 'ambidextrous']
HANDEDNESS_WEIGHTS = [10, 85, 5]  # left, right, ambidextrous percentages

ZONES = ['TL', 'TR', 'BL', 'BR', 'FH']


def generate_students(count: int) -> List[Dict[str, Any]]:
    """Generate list of fictional students with unique nicknames."""
    students = []
    used_nicknames = set()

    for i in range(count):
        # Generate unique nickname (2 letter code + number)
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        initials = first_name[0].upper() + last_name[0].upper()

        while True:
            number = random.randint(10, 99)
            nickname = f'{initials}{number}'
            if nickname not in used_nicknames:
                used_nicknames.add(nickname)
                break

        # Realistic middle-school heights: 140-200 cm, wingspan ~1-5% more than height
        min_height = 140
        max_height = 200
        height = round(random.uniform(min_height, max_height), 1)
        wingspan = round(height * random.uniform(1.00, 1.05), 1)
        skate_size = round(4 + (height - min_height) * (12 - 4) / (max_height - min_height), 0) + random.choice([-0.5, 0, 0.5])

        # Reaction times: 200-450ms (realistic range for middle school)
        reaction_times = [
            random.randint(200, 450),
            random.randint(200, 450),
            random.randint(200, 450),
        ]
        avg_reaction = sum(reaction_times) // len(reaction_times)

        student = {
            'nickname': nickname,
            'first_name': first_name,
            'last_name': last_name,
            'group': (i // 10) + 1,  # 10 students per group
            'height_cm': height,
            'wingspan_cm': wingspan,
            'skate_size': skate_size,
            'handedness': random.choices(HANDEDNESS, weights=HANDEDNESS_WEIGHTS, k=1)[0],
            'birth_month': random.choice(MONTHS),
            'reaction_time_ms': avg_reaction,
            'resting_heart_rate': random.randint(60, 100),
        }
        students.append(student)

    return students


def submit_demographics(student: Dict[str, Any]) -> bool:
    """Submit student demographics data to the API."""
    payload = {
        'nickname': student['nickname'],
        #'group': student['group'], # Group number is not needed in demographics, only in shots
        'height_cm': student['height_cm'],
        'wingspan_cm': student['wingspan_cm'],
        'skate_size': student['skate_size'],
        'handedness': student['handedness'],
        'birth_month': student['birth_month'],
        'reaction_time_ms': student['reaction_time_ms'],
        'resting_heart_rate': student['resting_heart_rate'],
    }

    try:
        response = requests.post(TRAITS_URL, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"  ✗ Demographics submission failed: {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  ✗ Demographics submission error: {e}")
        return False

def submit_shots(student: Dict[str, Any]) -> bool:
    """Submit student activity data (6 shot attempts per distance)"""
    success_count = 0
    fail_count = 0

    for distance in [2, 5, 7, 10]:
        # Each student attempts 6 shots per distance
        shots_made = random.randint(0, 6)
        payload = {
            'nickname': student['nickname'],
            'group': student['group'],
            'distance': distance,
            'shots_made': shots_made,
        }

        try:
            response = requests.post(SHOTS_URL, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            fail_count += 1

    return fail_count == 0

def generate(n: int = 70):

    students = generate_students(n)
    print(f"✓ Generated {len(students)} students")

    demographics_success = 0
    demographics_failed = 0
    activities_success = 0
    activities_failed = 0

    for idx, student in enumerate(students, 1):
        print(f"[{idx:2d}/{n}] {student['nickname']} ({student['first_name']} {student['last_name']})")

        if submit_demographics(student):
            print(f"  ✓ Demographics submitted")
            demographics_success += 1
        else:
            demographics_failed += 1
        
        if submit_shots(student):
            print(f"  ✓ Shots submitted")
            activities_success += 1
        else:
            activities_failed += 1
        
    print(f"Demographics: {demographics_success} successful, {demographics_failed} failed")
    print(f"Activities: {activities_success} successful, {activities_failed} failed")

generate(70)