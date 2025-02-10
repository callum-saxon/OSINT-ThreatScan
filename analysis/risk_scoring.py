def compute_risk_score(nlp_result):

    score = 0
    polarity = nlp_result["sentiment"]

    # Negative sentiment => higher score
    if polarity < -0.5:
        score += 50
    elif polarity < -0.2:
        score += 25

    # Possibly suspicious named entity categories
    for ent, label in nlp_result["named_entities"]:
        if label in ["ORGANIZATION", "GPE"]:
            score += 5

    # Cap at 100
    return min(score, 100)
