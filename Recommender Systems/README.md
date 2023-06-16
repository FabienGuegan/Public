# Overview

CheersTM is a revolutionizing social network in the world of beverage intake, specialized in beer. It enables its users to be a part of a community of like-minded individuals who all appreciate the exhilarating moment of drinking a beer. 
Through our patented mechanism Re-View ™, Cheers allows users to record their memorable experience in multi-media  in text, video or audio (the latter two are still under development).
Whether you are at a BBQ with family, at the newest brewery in town with friends, or having a date at the gastropub, Cheers will elevate your experience.

# Task

You are hired by Cheers, a hip new startup that allows app users to review beers that they drink and see the reviews on your network.
Cheers wants to increase user engagement by recommending new beers for their users by using their reviews database. Your task is to create these recommendations.

# Dataset

train_ratings.csv
- Beer_id (int) - Beer id for the reviewed beer
- User_name (str) - User that performed the review
- Review_score (int) - Score on the review, in a 1-20 scale
- Review_time (int) - Review timestamp
Metadata.csv (with new beers in the market)
- Beer_id (int)  - Beer Id
- beer_name (str) - Name of the beer
- brewer_id (int) - Id of the brewery, authors of the beer
- Beer_abv (float) - Alcohol volume, in percentage
- Beer_style (str) - Beer Style (ex. IPA, APA, etc)

# Objective

Using a combination of everything we learned in the BLU's, produce 50 recommendations with the most relevant new beers for each test user, based on data that you have.
