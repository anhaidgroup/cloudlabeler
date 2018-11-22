# Cloud Labeler

Cloud labeler is a cloud-based tool for manual labeling of candidate tuple pairs. This tool is meant to be deployed on a remote web server so that multiple users can use it for labeling purposes.

## Table of Contents
* [Installing on Local Machine](#installing-on-local-machine)
* [Deploying on AWS](#deploying-on-aws)
  + [Approach 1](#approach-1)
  + [Approach 2](#approach-2)
* [User Manual](#user-manual)
  
Notice that you can choose either "Installing on Local Machine" or "Deploying on AWS". "Installing on Local Machine" is **not** a prerequisite of "Deploying on AWS". We will provide existing docker image for easy use.

## Installing on Local Machine

### Requirements

Python 2 version 2.7+ or Python 3 version 3.6+

<details><summary markdown='span'>Want to use your own python?</summary>
<br />
    
If you need to use a different python, make sure to configure all the shebangs of python files. You can find the default shebang on the first line of all pythons files in /cgi-bin/ and /html/api/. For example, you may need to change the shebang of all python files to '#!/usr/bin/python3' if you want to use python 3.
</details>

### Platforms

Cloud labeler has been tested on Ubuntu 18.04. For other versions of Ubuntu, you may need to do some configurations. For example, some operating system has a different Apache Web Root. You need to change the directory of your Apache Web Root in /cgi-bin/model.py so that it can find the data to read.

### Dependencies

* Apache2 (the version we have tested is 2.4.29)
* Sqlite3 (the version we have tested is 3.25.2)
* Pandas (the version we have tested is 0.23.4)

### Steps

1. Clone the cloud labeler package from GitHub.

    ```
    git clone https://github.com/anhaidgroup/cloudlabeler.git
    ```

2. Copy or replace the html and cgi-bin folders in the Apache Web Root (usually /var/www/).

3. Enable cgi for both /cgi-bin/ and /html/api/ folders. You can learn how to enable cgi from https://httpd.apache.org/docs/2.4/howto/cgi.html. If you are using Ubuntu 18.04, you can replace /etc/apache2/apache2.conf and /etc/apache2/conf-available/serve-cgi-bin.conf using the [apache2.conf](./apache2.conf) and [serve-cgi-bin.conf](./serve-cgi-bin.conf) files we have provided.

4. Set the permission of every python file in /cgi-bin/ (including download.csv) and /html/api/ to be executable. Set the read and write access for all users to the files in /cgi-bin/data.

5. Enable cgi and restart Apache2. You are all set.
    
    ```
    sudo a2enmod cgi
    sudo service apache2 restart
    ```
    
## Deploying on AWS

### Platforms

Ubuntu Server 18.04 LTS (HVM)

### Dependencies

* Docker (the version we have tested is 18.06.1-ce)

In the approaches below, we will provide existing docker image for easy use. If you want to customize your docker image, we also prepare [deploy.sh](./deploy.sh) file to help you build your own docker image and [takedown.sh](takedown.sh) file to help you clean up the docker image later. You may need to create your [Docker Hub](https://docs.docker.com/docker-hub/) account and push your docker images so that you can access them later from AWS macine.

We offer two approaches to deploy cloud labeler on AWS. Approach 1 is to connect to your AWS machine directly and run docker image yourself. Approach 2 is to use Elastic Container Service, an advanced container orchestration service, to run docker image automatically. 

<details><summary markdown='span'>How can I know which approach to use?</summary> 
<br />
If you are unsure about which approach to choose, you can consider the following factors:
<br />
<br />
    
Use Approach 1 if you
* know how to connect to AWS machine using SSH.
* want to deploy cloud labeler quickly and easily.
* only have acccess to an existed EC2 instance but don't have permission to launch a new EC2 instance.

Use Appraoch 2 if you
* want to run cloud labeler in an existed ECS cluster.
* want to run cloud labeler at a high scalablility and performance.
* want to let different people manage cloud labeler and also ensure security.
</details>

### Approach 1

1. Create an AWS account if you don't have one. Login in [EC2](https://aws.amazon.com/ec2/). Find 'Instances' in the right panels.

   a. If you want to create a new instance. 
   
      - Find and click on 'Launch Instance' in the instances page. 
   
      - Choose Ubuntu Server 18.04 LTS (HVM) as your Amazon Machine Image. 
   
      - Choose General purpose Family t2.micro Type as your Instance Type if you want to use your free tier. 
   
      - In your Security Group, you should include both 'SSH' and 'HTTP'. If you are unsure whether you have included both, choose 'All Traffic' as the type of Security Group. If you are unsure about Source in the Security Group, choose 'Anywhere'. 
   
      - You can leave other options as default. 
   
      - After clicking 'Launch', choose 'Create a new key pair', enter your key pair name and Download Key Pair.
   
   b. If you want to deploy cloud labeler on an existed EC2 instance, click your instance and check its description. 
   
      - Its AMI ID should include 'ubuntu-bionic-18.04'. 
   
      - In its Security groups, the inbound rules should include both 'SSH' and 'HTTP'. 
   
      - Otherwise, you need to launch a new instance.

2. Connect to AWS machine using SSH. 


<details><summary markdown='span'> If you don't know how to connect to AWS machine using SSH, we recommend a convenient tool.  </summary>
    
   - Download and install [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), an SSH and telnet client. 
   
   - In the end of 1.a, you should download a Key Pair and it is a pem file. Open 'Putty Key Generator' and Load the Key Pair pem file in 'Load an existing private key file'. Then, choose 'Save private key' as ppk file. 
   
   - Open Putty and enter the 'Host name (or IP address)'. You can find the Host name of your AWS machine by clicking EC2 instance in [EC2](https://aws.amazon.com/ec2/) and check 'Public DNS (IPv4)' or 'IPv4 Public IP' in its description. 
   
   - In the left panel of Putty, choose Connection->SSH->Auth. In 'Private key file for authentication', choose the ppk file generated by 'Putty Key Generator'.
   
   - Click 'Open' in the right bottom.
</details>
  
   

   
3. Putty should open cmd of AWS machine for you. The first prompt should be 'login as'. Type 'ubuntu'.

4. Install [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce) by following the steps in the tutorial.

5. After you have installed Docker, pull the image from Docker Hub:

    ```
    sudo docker pull zachary62/apache_labeler
    ```
   
    <details><summary markdown='span'> Using your own Docker image?</summary>
    <br />
    If you are using your own Docker image, you should pull from your own Docker Hub. For example, if your Docker Hub repository name is John/apache_labeler, type:
   
     ```
    sudo docker pull John/apache_labeler
    ```
    </details>


6. Run the Docker image:

    ```
    sudo docker run -dit --name labeler -p 8080:80 zachary62/apache_labeler
    ```
    <details><summary markdown='span'> Using your own Docker image?</summary>
    <br /> 

    If you are using your own Docker image, you should use your own container name. For example, if your container name is John/apache_labeler, type
    ```
    sudo docker run -dit --name labeler -p 8080:80 John/apache_labeler
    ```
</details>

7. Now, you should be able to open cloud labeler. You can find the IP address of your AWS machine by clicking EC2 instance in [EC2](https://aws.amazon.com/ec2/) and check 'IPv4 Public IP' in its description. If your 'IPv4 Public IP' is '1.2.3.4', you can use cloud labeler in 'http://1.2.3.4:8080/'.
    
8. To clean up cloud labeler, run:
    ```
    sudo docker stop labeler
    sudo docker rm labeler
    sudo docker rmi zachary62/apache_labeler
    ``` 
    <details><summary markdown='span'> Using your own Docker image?</summary>
    <br /> 
    
    If you are using your own Docker image, you should use your own image name. For example, if your container name is John/apache_labeler and image name is cloud_labeler, type
    ```
    sudo docker stop cloud_labeler
    sudo docker rm cloud_labeler
    sudo docker rmi John/apache_labeler
    ``` 
</details>


### Approach 2

1. Pull the image from Docker Hub on your local machine:

    ```
    sudo docker pull zachary62/apache_labeler
    ```
    
   (If you are using your own Docker image, you should pull from your own Docker Hub)

2. Install [AWS Command Line Interface](https://docs.aws.amazon.com/cli/) on your local machine to help you push docker image. You can find the document for installation at https://docs.aws.amazon.com/cli/latest/userguide/installing.html. 

3. [Configure your cgi and set keys](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) on your local machine so that it has access to your AWS account.

4. [Create your repositories in AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html). Note that the name of repository should be 'apache_labeler' (or you will need to do more configurations to let docker identify your image). 

5. After you have created your repository, you should be able to find a 'View Push Commands' button in the repository page. Here it will list all the commands needed to push Docker image. Follow the commands carefully and push your Docker image to ECS repository. **Note: 1. you don't need to recreate docker image. 2. read the step 2 of push commands carefully**.

6. Create [Task Definition in AWS ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html). You should use the url of the repository you have pushed as the container.

7. Create [Cluster in AWS ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_clusters.html). The cluster template should be EC2 Linux and the Launch type should be EC2. 

8. After you have created a cluster, you should be able to create [service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html) in cluster page. Notice to choose the task you just created.
 
9. You should be able to find the deployed instances in [AWS EC2](https://aws.amazon.com/ec2/). Find 'instance' on the left panel and find the service you have just created. You can get the address of your instance in the IPv4 Public IP below. 

## User Manual

### Page Content

On the left side, there are three panels:

1. The top panel is Label Summary Panel. It shows a summary counts of different label types **saved**.

2. The middle panel is Filter Panel. It allows users to select a subset of label types and view or re-label them in the Main Panel. Users can select multiple label types. 

3. The bottom panel is Upload Panel. It allows users to upload and create their own tables.

Main Panel is on the right side. You can label and view tupe pairs for each pair. On the top there are three buttons. The 'Load Table' button allows you to load new table from database (and you should save current table before loading new one). The 'Download CSV' button allows you to download the CSV of current table. The 'Save and Continue' button allows you to save current table in database.

### Labeling

In order to label your own table, you need to follow the steps below:

First, upload your CSV files and choose your table name in Upload Panel.

Next, load the table you have uploaded using 'Load Table' button.

Then, label your pairs in the Main Panel. 

After that, save your table using 'Save and Continue' button. You can close the page and label the pairs later if you have saved the table.

Finally, download the final CSV file of the table you have saved using 'DownLoad CSV' button.

### Rest API

You can learn how to use REST api from [notebook](./notebooks/api.ipynb) (you need to install requests package).
