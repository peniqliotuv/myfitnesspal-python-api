def get_meals(date):
  jsonObj = {}
  for meal in date.meals:
    mealObj = {}
    for entry in meal:
      entryDict = entry.get_as_dict()
      mealObj[entryDict['name']] = entryDict['nutrition_information']
    jsonObj[meal.name] = mealObj
  return jsonObj
    
    