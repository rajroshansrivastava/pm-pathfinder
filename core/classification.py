def classify_pm_readiness(total_score):
    if total_score < 15:
        return "Exploratory"
    elif total_score < 25:
        return "Early Transitional"
    elif total_score < 35:
        return "Strong Transitional"
    else:
        return "Advanced PM Fit"
