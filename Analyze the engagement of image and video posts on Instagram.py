# -*- coding: utf-8 -*-
"""Perbandingan_Engagement_Post_Gambar_dan_Video_Instagram_pada_1_Akun.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mP3EaMSUhx4GqBfICZ9w7EXPCCtoUZxl
"""

import random
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

"""### Create a Random Instagram Dataset"""

data_posts = []
start_date = datetime(2023, 8, 1)  # start_date
end_date = datetime(2023, 8, 31)   # end_date

for i in range(31):
    likes = random.randint(10, 1000000)
    comments = random.randint(20, 500)
    shares = random.randint(0, 200)
    upload_datetime = start_date + timedelta(days=random.randint(0, (end_date - start_date).days),
                                             hours=random.randint(8, 23),
                                             minutes=random.randint(0, 59),
                                             seconds=random.randint(0, 59))
    content_type = random.choice(['image', 'video'])

    data_posts.append({
        'post': f"post {i+1}",
        'content_type': content_type,
        'likes': likes,
        'comments': comments,
        'shares': shares,
        'upload_date': upload_datetime.date().strftime('%Y-%m-%d'),
        'upload_time': upload_datetime.time().strftime('%H:%M:%S'),
        })

df = pd.DataFrame(data_posts)
df.head()

# Calculating engagement for each post
total_engagement = sum(post['likes'] + post['comments'] + post['shares'] for post in data_posts)

for post in data_posts:
    post['engagement'] = post['likes'] + post['comments'] + post['shares']
    post['engagement_percentage_%'] = round((post['engagement'] / total_engagement) * 100, 2)

"""### Engagement Results"""

df = pd.DataFrame(data_posts)
df.head()

"""### Sort posts by upload date and time"""

df.sort_values(by=['upload_date','upload_time']).head()

"""### Calculating engagement per week"""

# Categorize post data by week
weekly_data = {}
for post in data_posts:
    upload_date = datetime.strptime(post['upload_date'], '%Y-%m-%d')
    week_start = upload_date - timedelta(days=upload_date.weekday())
    week_end = week_start + timedelta(days=6)
    week_range = f"{week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')}"

    if week_range not in weekly_data:
        weekly_data[week_range] = {'total_engagement': 0, 'total_percentage': 0}

    weekly_data[week_range]['total_engagement'] += post['engagement']
    weekly_data[week_range]['total_percentage'] += post['engagement_percentage_%']

sorted_weekly_data = dict(sorted(weekly_data.items()))

# Creating a DataFrame
df = pd.DataFrame(sorted_weekly_data.values(), index=sorted_weekly_data.keys())
df.index.name = 'Week'
df['Total Percentage of Engagement'] = df['total_percentage'].apply(lambda x: f"{x:.2f}%")
df

# Making diagrams
week_ranges = list(sorted_weekly_data.keys())
percentage_values = [data['total_percentage'] for data in sorted_weekly_data.values()]

plt.figure(figsize=(6, 2))
plt.bar(week_ranges, percentage_values, color='skyblue')
plt.xlabel('Week')
plt.ylabel('Percentage of Engagement (%)')
plt.title('Percentage of Engagement Per Week')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Calculating engagement in one month (August 2023)
target_month = 8  # Agustus
target_year = 2023

engagement_in_target_month = sum(post['likes'] + post['comments'] + post['shares']
                                 for post in data_posts
                                 if datetime.strptime(post['upload_date'], '%Y-%m-%d').month == target_month
                                 and datetime.strptime(post['upload_date'], '%Y-%m-%d').year == target_year)


print(f"Total engagement in months {target_month}/{target_year} is {engagement_in_target_month}")

"""### Image and video post engagement rate comparison"""

# Calculating total engagement for image and video posts
total_image_engagement = sum(post['engagement'] for post in data_posts if post['content_type'] == 'image')
total_video_engagement = sum(post['engagement'] for post in data_posts if post['content_type'] == 'video')

# Persentase engagement
total_engagement = total_image_engagement + total_video_engagement
persentase_image = (total_image_engagement / total_engagement) * 100
persentase_video = (total_video_engagement / total_engagement) * 100

# Data for plotting
labels = ['Image', 'Video']
sizes = [persentase_image, persentase_video]
colors = ['skyblue', 'orange']

# Make pie chart
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Image and Video Post Engagement Comparison')
plt.show()