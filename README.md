# Machine Learning-Driven Alexa Skill: Predicting Dota 2 Match Outcomes
![image](https://github.com/edwintyx/Dota-Analyst/assets/23330497/b4329773-e1a1-460e-ad0e-8eb69e6fb59b)

## Description
The Dota Analyst is an Alexa Skill developed for Amazon Echo devices, designed to provide users with important Dota 2 information such as match schedules, results, team achievements, rosters, and predictions for ongoing tournaments like "The Internationals". This project, which took approximately three months to develop, is now live and available on the online Amazon Store.

## Key Features
- **Predictive Analytics**: The application implements machine learning models like Logistic Regression, Support Vector Machine, and K-nearest Neighbors to predict match outcomes. The prediction model is evaluated using standard performance measures. 
- **User Interaction Management**: Dialog management is implemented to handle conversations between the Dota Analyst skill and users. The skill uses utterances, intents, and slots in the interaction models between the users and Alexa to facilitate effective communication.
- **Data Integration**: The Dota Analyst retrieves match data using the OpenDota API and selected feature sets are used to build the prediction models.

## System Design
The Alexa skill relies on Amazon Web Services (AWS) Lambda for the back-end, while the front-end is built on the interaction model provided by Alexa Skills Kit. Additionally, a Python-based match predictor is integrated with the system to predict professional match outcomes.

## Implementation
The Dota Analyst skill comprises of multiple components including an interaction model for user communication, an AWS Lambda function to manage state machines for dialog management, and a Python match predictor.

## Testing and Evaluation
The skill went through rigorous testing including general testing, user slot testing, and Amazon Alexa app testing to ensure reliable performance. User feedback was also incorporated from an online survey questionnaire to make necessary improvements.

## Outcome and Future Improvements
While the project successfully achieved all mandatory and desirable requirements, there is room for improvement, especially with respect to the predictive power of the application. Future work includes developing a more complex and autonomous design to enhance the performance of the predictive model.

## Conclusion
The Dota Analyst is a rewarding project contributing to the fascinating world of digital technology, providing insights and predictions to millions of Dota 2 enthusiasts worldwide. Though the prediction accuracy is quite high, Dota outcomes prove to be inherently unpredictable, indicating the exciting nature of the game.

## Note
The project's final outcome is realized in the application's publication in the Apple Skills Store. We proudly present the Dota Analyst as an Alexa Skill for the community of Dota enthusiasts.
