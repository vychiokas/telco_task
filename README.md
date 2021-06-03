# telco_task

You started working for "Telco Relax" as the only technical expert in DWH project.

In the project directory there is usage data file in CSV format of the following structure:
**Customer ID Event Start Time Event Type Rate Plan ID Billing Flag 1 Billing Flag 2 Duration Charge Month**

Business owner sent you the requirements:
This is initial data, load it to database. We will get new data like this every week from our billing provider. And yeah, they usually have poor data quality so we need to send them alert if it’s bad asap.
Product guys want to see usage distribution and number of customers by Service Type and Rate Plan. They said they will get more data sources later.
Data must be removed after 6 months - legal requirement.
...and departed for 6 week vacation.

Your task
1. Based on what you have got, design initial data structure for the Data Warehouse. Deploy it on the database of your choice.
2. Build ETL scripts (preferably using Python) to populate it and check data quality.
3. Explain how you would implement support and monitoring process.
4. How do you see the evolution of the DWH project in "Telco Relax"? What will be major organisational and technical challenges?