'''
Program calculates total daily estimated energy expenditure in calories

Author: Heidi Ye
Last modified: Feb. 11 2019
'''

#FUNCTION DEFINITIONS
def weight(lbs):
  '''Turns weight from lbs to kg and rounds to 5 decimal places'''
  kg = lbs * 0.45359237
  return round(kg,5)

assert weight(100) == 45.35924
assert weight(155) == 70.30682

def height(inches):
  '''Turns height from inches to cm and rounds to 5 decimal places'''
  cm = inches * 2.54
  return round(cm,5)

assert height(63) == 160.02
assert height(70) == 177.8

def BMR_female(lbs,inches,age):
  '''Calculates BMR of a female using weight in kg and height in cm. Rounds to 5 decimal places'''
  BMR = 655 + (9.6 * weight(lbs)) + 1.8 * (height(inches)) - (4.7 * age)
  return round(BMR,5)

assert BMR_female(100,63,25) == 1260.98470

def BMR_male(lbs,inches,age):
  '''Calculates BMR of a male using weight in kg and height in cm. Rounds to 5 decimal places.'''
  BMR = 66 + (13.7 * weight(lbs)) + 5 * height(inches) - (6.8 * age)
  return round(BMR,5)

assert BMR_male(155,70,47) == 1598.60343

def BMR(gender,lbs,inches,age):
  '''Determines the correct BMR function to call based on gender'''
  if gender == "Female":
    return float(BMR_female(lbs,inches,age))
  elif gender == "female":
    return float(BMR_female(lbs,inches,age))
  elif gender == "Male": 
    return float(BMR_male(lbs,inches,age))
  elif gender == "male": 
    return float(BMR_male(lbs,inches,age))

assert BMR("Female",100,63,25) == 1260.98470
assert BMR("male",155,70,47) == 1598.60343
 
def food_exp(calorie_intake):
  '''Calculates thermic effect of food expenditure'''
  exp = 0.05 * calorie_intake
  return exp

assert food_exp(1500) == 75
assert food_exp(2000) == 100

def physical_activity(activity_score,gender,lbs,inches,age):
  '''Determines user activity level and returns physical activity calculation. Rounds to 5 decimal places.'''
  if activity_score == 1:
    activity_level = 0.25 * BMR(gender,lbs,inches,age)
    return round(activity_level,5)
  elif activity_score == 2:
    activity_level = 0.375 * BMR(gender,lbs,inches,age)
    return round(activity_level,5)
  elif activity_score == 3:
    activity_level = 0.55 * BMR(gender,lbs,inches,age)
    return round(activity_level,5)
  elif activity_score == 4:
    activity_level = 0.78 * BMR(gender,lbs,inches,age)
    return round(activity_level,5)

assert physical_activity(3,"Female",100,63,25) == 693.54159
assert physical_activity(3,"Male",155,70,47) == 879.23189

def total_energy_exp(gender,lbs,inches,age,activity_score,calorie_intake):
  '''Calculates total daily estimated energy expenditure in calories. Rounds to 5 decimal places.'''
  total = BMR(gender,lbs,inches,age) + physical_activity(activity_score,gender,lbs,inches,age) + food_exp(calorie_intake)
  return round(total,5)

assert total_energy_exp("Female",100,63,25,3,1500) == 2029.52629
assert total_energy_exp("male",155,70,47,3,2000) == 2577.83532

#MAIN FUNCTION
def main():
  '''Main function which asks user for input and prints total daily energy expenditure in calories. Rounds to nearest whole calorie'''
  print("This program collects information on your weight, height, gender, calorie intake and activity level to determine your total energy expenditure for one day. Begin by answering these questions:")
  print('''
  ''')
  lbs = int(input("What is your weight in pounds? "))
  inches = int(input("What is your height in inches? "))
  gender = input("Are you male or female? ")
  age = int(input("How old are you? "))
  calorie_intake = float(input("What is your approxiamate daily calorie intake? "))
  #print(weight(lbs))
  #print(BMR_female(lbs,inches,age))
  #print(BMR(gender,lbs,inches,age))
  print ('''
Activity levels are scored based on the chart below:'''
    '''

Activity Level| Description
            1 | Sedentary - mostly resting with little or                           no activity
            2 | Light - occasional unplanned activity                               e.g. going for a walk, or a swim or skiing    
            3 | Moderate - daily planned activity such                             as short jogs,brisk walk
            4 | Heavy - daily planned workouts (hours or                           several hours of continuous activity
''')
  activity_score = int(input("Choose an activity level (1-4) based on the options above. "))
  #print(total_energy_exp(gender,lbs,inches,age,activity_score,calorie_intake))
  print('''
  ''')
  print("Based on the information provided, your total estimated energy expediture is",int(total_energy_exp(gender,lbs,inches,age,activity_score,calorie_intake)),"calories per day.")

main()