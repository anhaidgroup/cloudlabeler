# Cloud Labeler

Cloud labeler is a cloud-based tool for manual labeling of candidate pairs. This tool is meant to be deployed in a remote web server so that multiple users can use this tool for labeling purposes.

## Installation

### Requirements

Python 2.7

### Platforms

Cloud labeler has been tested on Ubuntu 18. For other version of Ubuntu, you may need to do some configurations.

### Dependencies

* Apache2
* Sqlite3
* Pandas

If you want to deploy it in AWS, you need Docker.

### Installing in Local Machine

First, clone the cloud labeler package from GitHub

    git clone https://github.com/anhaidgroup/cloudlabeler.git
    
Next, copy or replace the html and cgi-bin folder in the Apache Web Root (usually /var/www/).

Then, enable cgi for both /cgi-bin/ and /html/api/ folders. You can learn how to enable cgi from https://httpd.apache.org/docs/2.4/howto/cgi.html. If you are using Ubuntu 18, you can replace /etc/apache2/apache2.conf and /etc/apache2/conf-available/serve-cgi-bin.conf using the [apache2.conf](./apache2.conf) and [serve-cgi-bin.conf](./serve-cgi-bin.conf) we have provided.

After that, set the permission of every python files in /cgi-bin/ (including download.csv) and /html/api/ to be executable. Set the read and write access for all users to the files in /cgi-bin/data.

Finally, enable cgi and restart Apache2. You are all set.

    a2enmod cgi
    service apache2 restart

### Deploying in AWS

First, build the docker file by running [deploy.sh](./deploy.sh) we have provided.

Next, install [AWS Command Line Interface](https://docs.aws.amazon.com/cli/) to help you push docker image. You can find the document for installation at https://docs.aws.amazon.com/cli/latest/userguide/installing.html. After installed cli, you need to [configure your cgi and set keys](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

Then, [create your repositories in AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html). Note that the name of repository is better to be 'apache_labeler' (or you need to do more configurations to let docker identify your image). After you have created your repository, you should be able to find a 'View Push Commands' button. Here it will list all the commands needed to push docker image. **Note: 1. you don't need to recreate docker image. 2. read the step 2 of push commands carefully**.

After that, create Task Definitions in [AWS ECS](https://aws.amazon.com/ecs/). You should use the url of the repository you have created as the container.

Afterwords, create Cluster in [AWS ECS](https://aws.amazon.com/ecs/). The cluster template should be EC2 Linux and the Launch type should be EC2. After you have created a cluster, you should be able to create service in cluster page. Notice to choose the task you just created.
 
Finally, you should be able to find the instance in [AWS EC2](https://aws.amazon.com/ec2/). Find 'instance' on the left and find the service you have just created. You can get the url of your instance in the IPv4 Public IP below. 

## User Manual

### Page Content

On the right side, there are three panels:

1. The top panel is Label Summary Panel. It shows a summary counts of different label types **saved**.

2. The middle panel is Filter Panel. It allows users to select a subset of label types and view or re-label them in the Main Panel. Users can select multiple label types. 

3. The bottom panel is Upload Panel. It allows users to upload and create their own tables.

Main Panel is on the left side. You can label and view tupe pairs for each pair. On the top there are three buttons. The 'Load Table' button allows you to load new table from database (and you should save current table before loading new one). The 'Download CSV' button allows you to download the CSV of current table. The 'Save and Continue' button allows you to save current table in database.

### Labeling

In order to label your own table, you need to follow the steps below:

First, upload your CSV files and choose your table name in Upload Panel.

Next, load the table you have uploaded using 'Load Table' button.

Then, label your pairs in the Main Panel. 

After that, save your table using 'Save and Continue' button. You can close the page and label the pairs later if you have saved the table.

Finally, download the final CSV file of the table you have saved using 'DownLoad CSV' button.
