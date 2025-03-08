import csv
import datetime
import matplotlib.pyplot as plt

# Lists to store data
date_time = []
traffic_volume = []
rainfall = []
snowfall = []

# Read CSV file & handle exceptions
try:
    with open('TrafficVolumeData.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                date_time.append(row[0])
                traffic_volume.append(int(row[-1]))  # Ensure correct index for traffic volume
                rainfall.append(float(row[9]))  # Adjusted to correct CSV column index
                snowfall.append(float(row[10]))  # Adjusted to correct CSV column index
            except (ValueError, IndexError):
                print(f"Skipping invalid row: {row}")  # Debugging message
except FileNotFoundError:
    print("Error: File not found. Please check the file location.")
    exit()

# Extract hour and day of the week
hours = []
days_of_week = []
for dt in date_time:
    try:
        dt_obj = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        hours.append(dt_obj.hour)
        days_of_week.append(dt_obj.strftime("%A"))
    except ValueError:
        print(f"Skipping invalid date format: {dt}")  # Debugging message
        continue

# Group traffic volume by hour
hourly_traffic = [0] * 24
hour_count = [0] * 24
for i in range(len(hours)):
    if 0 <= hours[i] < 24:
        hourly_traffic[hours[i]] += traffic_volume[i]
        hour_count[hours[i]] += 1
hourly_avg_traffic = [hourly_traffic[i] / hour_count[i] if hour_count[i] != 0 else 0 for i in range(24)]

# Separate weekday and weekend traffic
weekdays = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
weekday_traffic = [traffic_volume[i] for i in range(len(traffic_volume)) if days_of_week[i] in weekdays]
weekend_traffic = [traffic_volume[i] for i in range(len(traffic_volume)) if days_of_week[i] not in weekdays]

# Rain and snow impact
traffic_on_rainy_days = [traffic_volume[i] for i in range(len(traffic_volume)) if rainfall[i] > 0]
traffic_on_dry_days = [traffic_volume[i] for i in range(len(traffic_volume)) if rainfall[i] == 0]
traffic_on_snowy_days = [traffic_volume[i] for i in range(len(traffic_volume)) if snowfall[i] > 0]
traffic_on_non_snowy_days = [traffic_volume[i] for i in range(len(traffic_volume)) if snowfall[i] == 0]

# Insights & Analysis
print(f"Loaded {len(date_time)} rows successfully.")
print(f"Sample Extracted Data - Hour: {hours[:5]}, Days: {days_of_week[:5]}")
print(f"Peak Traffic Hour: {hours[hourly_avg_traffic.index(max(hourly_avg_traffic))]}:00")
print(f"Average Traffic on Weekdays: {sum(weekday_traffic)/len(weekday_traffic):.2f}")
print(f"Average Traffic on Weekends: {sum(weekend_traffic)/len(weekend_traffic):.2f}")
print(f"Average Traffic on Rainy Days: {sum(traffic_on_rainy_days)/len(traffic_on_rainy_days):.2f}")
print(f"Average Traffic on Snowy Days: {sum(traffic_on_snowy_days)/len(traffic_on_snowy_days):.2f}")

# Visualizations
plt.figure()
plt.plot(range(24), hourly_avg_traffic, marker='o')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Traffic Volume')
plt.title('Traffic Volume by Hour')
plt.grid()
plt.savefig('traffic_by_hour.png')
plt.show()

plt.figure()
plt.bar(['Weekdays', 'Weekends'], [sum(weekday_traffic) / len(weekday_traffic), sum(weekend_traffic) / len(weekend_traffic)])
plt.xlabel('Day Type')
plt.ylabel('Average Traffic Volume')
plt.title('Traffic Volume: Weekdays vs. Weekends')
plt.savefig('traffic_weekday_vs_weekend.png')
plt.show()

plt.figure()
plt.bar(['Rainy Days', 'Dry Days'], [sum(traffic_on_rainy_days) / len(traffic_on_rainy_days), sum(traffic_on_dry_days) / len(traffic_on_dry_days)])
plt.xlabel('Condition')
plt.ylabel('Average Traffic Volume')
plt.title('Impact of Rain on Traffic')
plt.savefig('traffic_rain_impact.png')
plt.show()

plt.figure()
plt.bar(['Snowy Days', 'Non-Snowy Days'], [sum(traffic_on_snowy_days) / len(traffic_on_snowy_days), sum(traffic_on_non_snowy_days) / len(traffic_on_non_snowy_days)])
plt.xlabel('Condition')
plt.ylabel('Average Traffic Volume')
plt.title('Impact of Snow on Traffic')
plt.savefig('traffic_snow_impact.png')
plt.show()

print("Analysis complete. Visualizations saved.")
