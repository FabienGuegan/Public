# Overview
In the capstone, we’re not going to treat you as a student. You will be treated as an employee.

The scenario is the following: you’ve been hired by a consulting firm, and have just had the first exchange of emails with your new boss.

You already know you have 3 deliverables:
- The analysis report
- An API endpoint
- The deployment retrospective report

In order to simulate the real world scenario, the requirements may be ambiguous. A big part of your job as a data scientist in the real world will be turning business requirements into clear cut data science requirements. In the capstone, the starting point is the emails. You will have to send a clarification email to your client with any follow up questions to fully understand what you need to do.  

Once you feel comfortable that you understand what is required of you, you produce the report, API endpoint, deal with the data as it comes, and then produce the second report. 

# Timeline
- Week 1 is for understanding the dataset and asking questions, at the end of which you will receive answers disambiguating the issues;
- Weeks 2 and 3 are for training your model, writing your first report, and deploying your app - close to the end of week 3 we will do a trial round for you to test your app; By the end of week 3, you will need to submit the app and the first report
- In week 4 the observations will be sent to your deployed model and instructors will be checking your reports;
- By the end of week 4, you will receive comments on your reports;
- Weeks 5 and 6 are for retraining and re-deploying your model and writing up the second report. You should also address comments made to the first report by the end of week 6;
- By the end of week 6, you will need to resubmit the app and the first report, submit the second report and submit your code.
- By the end of week 7, you will receive comments to your second report;
- Week 8 is for addressing comments to the second report;
- By the end of week eight, you will need to resubmit the second report.

# Activities
1. Carefully read the client briefing.
2. Disambiguate any requirements, by sending an email to your client.
3. Get very familiar with the training set. Expect to spend quite a few hours experimenting, exploring, and getting to know it. Focus on the analysis 4. needed to answer the business questions.
5. Train the model that you will require for your API, and understand its limitations.
6. Produce a report that satisfies your client’s requirements, using this structure. 
7. Deploy your model, using these instructions.
8. Deal with the data as it arrives and ensure your API is responding successfully.
9. Write the second report using this structure.

# Understanding the data you’ll receive
You will receive data in 3 moments:

Receiving the train set:
The first is when you receive these instructions. The email from your client will already link to your training dataset. You will, however, have to build your own target, as it’s not already in clean binary (0’s and 1’s) form.

Receiving the test set 1:
Later (see timeline), the data will start flowing from the client via HTTP. First, you will only receive the labels (not the target).
After this data has stopped flowing, you will receive the respective targets. At this time you will be able to adjust your model and re-deploy if you feel that it’s worth updating. This model update is optional.

Receiving the test set 2:
Finally, the data will restart flowing, and the second test set will arrive via HTTP. You will never receive the true labels for this dataset.

# Success Criteria
The passing criteria is also similar to that in the professional world. We expect you to deliver something that would be acceptable by a client. There isn’t a single number we are expecting you to hit, nor is there a grader to tell you if you are right.

That will lead to a bit of subjectivity. In general, if you deliver on all the requirements with an acceptable level of quality you will pass. If you deliver something that would get you a bad performance review, you won’t.

# Hints and advice
This is a capstone. It contains data science, data engineering, and project management. Don’t worry if it feels a bit overwhelming at first, take a breath and read everything twice. Make a plan for how you will approach each challenge. Ask questions. This is going to be difficult, but you can do it!

You may find that part of this assignment contains some pretty tricky questions. For instance, you may find that every model you train discriminates against some protected group. You will most likely find it impossible to completely remove this effect. That’s how the real world works.  

You may also discover that there are trade-offs where diminishing one type of discrimination actually increases another. Or that your model performance would go down on some metrics as you attempt to fix others. You may also find that as you attempt to fix true positive rates, your true negative rates will become unequal. To be clear, there is no perfect solution.

Any solution will be subjective, and we are not expecting you to find the “right one”. What we are expecting is that you are able to do your best to deal with this, and then support your decisions in an informed way.

You will be building your own target, which is new in the Academy, but very frequent in the real world. There is of course an objective truth, but here is a hint: make sure that you always answer either true or false, and that you aren’t caught off and answer np.nan. Look for edge cases. Be skeptical of assuming things will work, and look hard at your predictions on the training set, not just as aggregate numbers.

