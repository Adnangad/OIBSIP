def bmi_class(bm):
    if bm <= 16:
        return "Very Severely underweight"
    elif bm <= 16.9:
        return "Severely underweight"
    elif bm <= 18.4:
        return "Underweight"
    elif bm <= 24.9:
        return "Normal"
    elif bm <= 29.9:
        return "Overweight"
    elif bm <= 34.9:
        return "Obese class 1"
    elif bm <= 39.9:
        return "Obese class 2"
    else:
        return "Obese class 3"
    

def bmi_category_text(bm):
    if bm <= 16:
        return "You are very severely underweight"
    elif bm <= 16.9:
        return "You are severely underweight"
    elif bm <= 18.4:
        return "You are Underweight"
    elif bm <= 24.9:
        return "You have a normal body weight"
    elif bm <= 29.9:
        return "You are overweight"
    elif bm <= 34.9:
        return "You are classified as obese class 1"
    elif bm <= 39.9:
        return "You are classified as obese class 2"
    else:
        return "You are classified as obese class 3"