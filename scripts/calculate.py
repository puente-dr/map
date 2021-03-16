from datetime import timedelta, date

def calculate_age(born):
    if "-" in born:
        mod = born.split('-')
        today = date.today()
        return int(today.year - int(mod[0]))
    elif "/" in born:
        mod = born.split("/")
        today = date.today()
        try:
            return int(today.year - int(mod[2]))
        except:
            return None 
    else:   
        return None