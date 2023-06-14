# Overview

In this hackathon, we will enter the mysterious world of algorithmic trading.

Every day millions of crypto transactions occur across all blockchains (e.g., Bitcoin, Ethereum). These transactions are public, meaning that everyone can see them. And they can be analysed to understand the behaviour of each user.

We will focus on one of these users and will aim to model their behaviour. The user in question is running a trading algorithm that generates transactions aimed at profiting from small discrepancies in prices. For example, if Bitcoin is being priced at $19,500 in exchange A and $19,600 in exchange B, the algorithm will trigger a transaction where Bitcoin is bought in exchange A and another where it is sold in exchange B for a profit of $100. These transactions happen at the same time and thus can be considered, for all intents and purposes, a single transaction.

To model the behaviour of this user, data was collected from February 2022 to May 2022. Both instances where the algorithm decided to trade and instances where the algorithm decided NOT to trade were gathered. In total, ~338k of these instances (or events) were collected, from which ~23k resulted in a transaction being triggered. Thus, our goal is to predict whether a transaction will occur in each of the events provided, based on the underlying market conditions.

To give you some intuition, you can expect that when the price between exchanges differs significantly, a transaction is likely to occur. On the other hand, if the discrepancy is not significant there’s less of an incentive to send transactions. Additionally, note that all transactions incur a fee. You can think about the balance in each exchange and reason that enough balance must be available for the transaction.

In order to save you time, there is a document named requirements.txt in the hackathon directory which identifies some basic packages that you should install right away when setting up your virtual environment for the hackathon. Please bear in mind that they are not mandatory to use, and if you are more comfortable using other packages please be free to do it.

The model you are about to develop is used in practice to anticipate trades of competing algorithms so that your algorithm can adjust its strategy accordingly. It’s a ruthless world out there. Good luck!
Disclaimer: This exercise is only meant for educational purposes. Algorithmic trading is hard and there’s a very high likelihood you will lose your money.

# Objective

The main goal is to predict whether a blockchain transaction is going to occur.
For each event in the test dataset, you’ll have to predict the probability of it triggering a transaction.

Your submission file should be a CSV with two columns:
- id: the id of the event
- result: the probability of a transaction occurring

When you submit your predictions, some validations will be run that will check the following:
- Your file has the two columns with the right name
- Your file has the right number of events
- Your file has the same event ids as the test dataset. The submission is sorted by id, so the order doesn’t matter
- Your predictions are probabilities and not just 0s and 1s

