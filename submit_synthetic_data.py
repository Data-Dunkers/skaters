#!/usr/bin/env python3
"""
Submit synthetic data for 75 fictional middle-school students from Manitoba
to both the Data Skaters Activities and Traits forms.
"""

import requests
import random
import time
import sys
from typing import Dict, List, Any

# API endpoints
ACTIVITIES_URL = 'https://api.datadunkers.ca/api/collections/data_skaters_activities/records'
TRAITS_URL = 'https://api.datadunkers.ca/api/collections/data_skaters_traits/records'

# Manitoba-themed first and last names for authenticity
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

ACTIVITIES = [
    'Sniper', 'Playmaker', 'Power Forward', 'Two-way Forward',
    'Speed Winger', 'Defensive Defenseman', 'Offensive Defenseman'
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
        # Generate unique nickname (2-3 letter code + number)
        while True:
            letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(2, 3)))
            number = random.randint(10, 99)
            nickname = f'{letters}{number}'
            if nickname not in used_nicknames:
                used_nicknames.add(nickname)
                break

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        # Realistic middle-school heights: 140-180 cm, wingspan ~1-5% more than height
        height = round(random.uniform(140, 180), 1)
        wingspan = round(height * random.uniform(1.00, 1.05), 1)
        skate_size = round(random.uniform(3.0, 8.0), 1)

        # Reaction times: 150-350ms (realistic range for middle school)
        reaction_times = [
            random.randint(150, 350),
            random.randint(150, 350),
            random.randint(150, 350),
        ]
        avg_reaction = sum(reaction_times) // len(reaction_times)

        # Resting heart rate: 60-100 bpm (middle school range)
        resting_hr = random.randint(60, 100)

        student = {
            'nickname': nickname,
            'first_name': first_name,
            'last_name': last_name,
            'height_cm': height,
            'wingspan_cm': wingspan,
            'skate_size': skate_size,
            'reaction_time_ms': avg_reaction,
            'resting_heart_rate': resting_hr,
            'handedness': random.choices(HANDEDNESS, weights=HANDEDNESS_WEIGHTS, k=1)[0],
            'brith_month': random.choice(MONTHS),
            'group_number': (i // 10) + 1,  # 10 students per group
        }
        students.append(student)

    return students


def submit_traits(student: Dict[str, Any]) -> bool:
    """Submit student traits data to the API."""
    payload = {
        'nickname': student['nickname'],
        'height_cm': student['height_cm'],
        'wingspan_cm': student['wingspan_cm'],
        'reaction_time_ms': student['reaction_time_ms'],
        'skate_size': student['skate_size'],
        'handedness': student['handedness'],
        'brith_month': student['brith_month'],
        'resting_heart_rate': student['resting_heart_rate'],
    }

    try:
        response = requests.post(TRAITS_URL, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"  ✗ Traits submission failed: {response.status_code}")
            print(f"    Response: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"  ✗ Traits submission error: {e}")
        return False


def submit_activities(student: Dict[str, Any]) -> bool:
    """Submit student activity data (6 shot attempts per activity) to the API."""
    nickname = student['nickname']
    group = student['group_number']
    success_count = 0
    fail_count = 0

    # Submit data for all activities
    for activity in ACTIVITIES:
        # Each student completes all 6 attempts per activity
        for attempt_num in range(1, 7):
            payload = {
                'group_number': group,
                'nickname': nickname,
                'activity': activity,
                'attempt_number': attempt_num,
                'success': random.choice([True, False]),
            }

            # Add activity-specific fields based on config
            if activity in ['Sniper', 'Playmaker', 'Two-way Forward', 'Defensive Defenseman', 'Offensive Defenseman']:
                payload['target_zone'] = random.choice(ZONES)

            if activity in ['Sniper', 'Playmaker', 'Two-way Forward']:
                payload['time_seconds'] = round(random.uniform(2.5, 12.0), 2)

            try:
                response = requests.post(ACTIVITIES_URL, json=payload, timeout=10)
                if response.status_code in [200, 201]:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1

            # Small delay to avoid overwhelming the API
            time.sleep(0.1)

    return fail_count == 0


def test():
    """Test submission with a single student."""
    print("=" * 60)
    print("DATA SKATERS - TEST SUBMISSION (1 STUDENT)")
    print("=" * 60)
    print()

    # Generate a single student
    students = generate_students(1)
    student = students[0]

    print(f"Test Student: {student['nickname']} ({student['first_name']} {student['last_name']})")
    print(f"  Height: {student['height_cm']} cm")
    print(f"  Handedness: {student['handedness']}")
    print(f"  Reaction Time: {student['reaction_time_ms']} ms")
    print(f"  Resting HR: {student['resting_heart_rate']} bpm")
    print()

    traits_ok = False
    activities_ok = False

    print("Submitting traits...")
    if submit_traits(student):
        print("  ✓ Traits submitted successfully")
        traits_ok = True
    else:
        print("  ✗ Traits submission failed")

    print()
    print("Submitting activities...")
    if submit_activities(student):
        print("  ✓ Activities submitted successfully")
        activities_ok = True
    else:
        print("  ✗ Activities submission failed")

    print()
    print("=" * 60)
    if traits_ok and activities_ok:
        print("✓ TEST PASSED: All submissions successful")
    else:
        print("✗ TEST FAILED: Some submissions failed")
    print("=" * 60)


def main():
    """Generate and submit data for 75 students."""
    print("=" * 60)
    print("DATA SKATERS - SYNTHETIC DATA SUBMISSION")
    print("=" * 60)
    print()

    # Generate students
    print("Generating 75 fictional Manitoba middle-school students...")
    students = generate_students(75)
    print(f"✓ Generated {len(students)} students")
    print()

    # Submit data
    traits_success = 0
    traits_failed = 0
    activities_success = 0
    activities_failed = 0

    print("Submitting traits and activity data...")
    print()

    for idx, student in enumerate(students, 1):
        print(f"[{idx:2d}/75] {student['nickname']} ({student['first_name']} {student['last_name']})")

        # Submit traits
        if submit_traits(student):
            print(f"  ✓ Traits submitted")
            traits_success += 1
        else:
            traits_failed += 1

        # Submit activities
        if submit_activities(student):
            print(f"  ✓ Activities submitted")
            activities_success += 1
        else:
            activities_failed += 1

        # Small delay between students
        time.sleep(0.1)

    # Summary
    print()
    print("=" * 60)
    print("SUBMISSION SUMMARY")
    print("=" * 60)
    print(f"Traits:     {traits_success} successful, {traits_failed} failed")
    print(f"Activities: {activities_success} successful, {activities_failed} failed")
    print()
    print("✓ Data submission complete!")


if __name__ == '__main__':
    #test()
    main()
