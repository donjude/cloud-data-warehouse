# Cloud Data Warehouse with Amazon Redshift

## Project Summary

Sparkify is a music straming startup that has grown their user base and song database and would want to move their processes and data onto the cloud. Their data consist of user activities on using the music streaming up as well as metadata on the songs in their app. These data are currently stored on Amazon s3 storage bucket on Amazon Web Service.

Sparkify requires an ETL pipeline to be built that extracts their data from s3, stages the data in Redshift, and transforms the data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. The database and ETL pipeline would be tested by running queries given by Sparkify analytics team and compare results with their expected results.


## Project Description

In this Project an ETL pipeline would be built for a datawarehouse hosted on Amazon Redshift using Amazon Webservice(AWS) cloud computing platform. The ETL pipleine would load data from s3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

## How to run the Python Scripts

1. Install AWS Command Line Interface awscli from the Terminal/Bash Shell.

    On Linux:<br/>
    ```$sudo apt install awscli```

    On Windows:<br/>
     ```C:\> msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi```


2. Run pip to install AWS Python SDK(boto3), pandas and psycopg2-binary.

    ```$pip install boto3 pandas psycopg2-binary```


3. Run the below on your local git bash/Terminal to clone the github repository.

    ```$git clone https://github.com/donjude/cloud-data-warehouse.git```

4. In the cloned repository on your local computer, open the jupyter notebook file `aws_sdk_create_redshift_cluster.ipynb`, follow the instruction and run the notebook cells.

5. 

TODO:
- Summary of Project
- How to run the Python Scripts
- Explanation of the files in the repository
- Comments are used effectively, and each function has a docstring
- Scripts have an intuitive, easy-to-follow structure


- Document Process
- Do the following steps in your README.md file.

- Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.
- State and justify your database schema design and ETL pipeline.
- [Optional] Provide example queries and results for song play analysis.

