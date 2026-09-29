def calculate_fitness_level(
    age: int,
    height: float,
    weight: float,
    bmi: float,
    workout_freq_per_week: int,
    workout_duration_per_day: int,
) -> int:
    """Calculate fitness level (1-3) based on user metrics.

    Level 1: Beginner
    Level 2: Intermediate
    Level 3: Advanced
    """
    score = 0

    # Workout frequency scoring
    if workout_freq_per_week >= 5:
        score += 3
    elif workout_freq_per_week >= 3:
        score += 2
    else:
        score += 1

    # Workout duration scoring
    if workout_duration_per_day >= 60:
        score += 3
    elif workout_duration_per_day >= 30:
        score += 2
    else:
        score += 1

    # BMI scoring (healthy range = 18.5-24.9)
    if 18.5 <= bmi <= 24.9:
        score += 3
    elif 25.0 <= bmi <= 29.9 or 17.0 <= bmi < 18.5:
        score += 2
    else:
        score += 1

    # Age scoring (younger tends to recover faster)
    if age < 30:
        score += 3
    elif age < 50:
        score += 2
    else:
        score += 1

    # Map total score to level 1-3
    if score >= 10:
        return 3
    elif score >= 7:
        return 2
    else:
        return 1
