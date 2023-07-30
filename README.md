# Machine Learning-Driven Alexa Skill: Predicting Dota 2 Match Outcomes
![image](https://github.com/edwintyx/Dota-Analyst/assets/23330497/b4329773-e1a1-460e-ad0e-8eb69e6fb59b)

## Description
Dota Analyst is an Alexa Skill I designed for Amazon Echo devices, offering a wealth of Dota 2 information and match predictions. Now available on the Amazon Store [https://www.amazon.com/Edwin-Dota-Analyst/dp/B07WDJDWRJ](url), it serves Dota 2 fans by providing match schedules, results, team achievements, rosters, and predictions for ongoing tournaments like "The Internationals".

## Key Features
- **Predictive Analytics**: The application implements machine learning models like Logistic Regression, Support Vector Machine, and K-nearest Neighbors to predict match outcomes. The prediction model is evaluated using standard performance measures. 
- **User Interaction Management**: Dialog management is implemented to handle conversations between the Dota Analyst skill and users. The skill uses utterances, intents, and slots in the interaction models between the users and Alexa to facilitate effective communication.
- **Data Integration**: The Dota Analyst retrieves match data using the OpenDota API and selected feature sets are used to build the prediction models.

## System Design
The back-end relies on Amazon Web Services (AWS) Lambda, while the front-end is crafted using Alexa Skills Kit's interaction model. A Python match predictor is integrated to anticipate professional match outcomes.

## Implementation
Dota Analyst consists of an interaction model for user engagement, an AWS Lambda function for dialog management, and a Python match predictor.

## Testing and Evaluation
To ensure the robustness of the skill, I employed various testing techniques such as general testing, user slot testing, and Amazon Alexa app testing. User feedback, collected via an online survey, was also incorporated for continuous improvement.

## Outcome and Future Improvements
While the project met all the key requirements, enhancing the predictive power of the application is an area for future work. My aim is to develop a more intricate and autonomous design, integrating more real-time game data for improved prediction accuracy.

## Conclusion
Dota Analyst contributes to the thrilling realm of digital technology by offering insights and predictions to Dota 2 enthusiasts globally. My predictive model demonstrates high accuracy, yet the unpredictable nature of Dota matches requires me to consider real-time game data in future enhancements.

## Note
Dota Analyst is available for use via the Alexa Skills Store [https://www.amazon.com/Edwin-Dota-Analyst/dp/B07WDJDWRJ](url). I'm proud to present this Alexa Skill as a valuable tool for the Dota community.
