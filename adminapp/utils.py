months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]
days=[
    "Sunday","Monday","Teusday","Wednesday","Thursday","Friday","Saturday"
]
month_days=[ "1","2","3","4","5","6","7","8","9","10","11","12","13",
            "14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"

]
colorPalette = ["#55efc4", "#81ecec", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]


def get_month_dict():
    month_dict=dict()
    for day in month_days:
        month_dict[day]=0
    return month_dict

def get_week_dict():
    week_dict=dict()
    for day in days:
        week_dict[day]=0
    return week_dict


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette