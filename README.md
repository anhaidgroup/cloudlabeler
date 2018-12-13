# Cloud Labeler

Cloud labeler is a cloud-based tool for manual labeling of candidate tuple pairs. This tool is meant to be deployed on a remote web server so that multiple users can use it for labeling purposes.

## Table of Contents
* [Installing on Local Machine](#installing-on-local-machine)
* [Deploying on AWS](#deploying-on-aws)
  + [Approach 1](#approach-1)
  + [Approach 2](#approach-2)
* [User Manual](#user-manual)
  
Notice that you can choose either "Installing on Local Machine" or "Deploying on AWS". You can choose first build cloud labeler on your local machine, make some changes, create your docker image and deploy it on AWS. However, "Installing on Local Machine" is **not** a prerequisite of "Deploying on AWS". We will provide existing docker image for easy use when deploying cloud labeler on AWS.

## Installing on Local Machine

### Requirements

Python 2 version 2.7+ or Python 3 version 3.5+

<details><summary markdown='span'>Want to use your own python?</summary>
<br />
    
If you need to use a different python, make sure to configure all the shebangs of python files. Shebang is a character sequence used to specify interpreter program in Unix-like operating systems. You can find the default shebang on the first line of all pythons files in /cgi-bin/ and /html/api/. For example, if you want to use python 3 and your python 3 is under '/usr/bin/python3', you need to change the shebang of all python files to '#!/usr/bin/python3' .
</details>

### Platforms

Cloud labeler has been tested on Ubuntu 18.04. For other versions of Ubuntu, you may need to do some configurations. For example, some operating system has a different Apache Web Root. You need to change the directory of your Apache Web Root in /cgi-bin/model.py so that it can find the data to read.

### Dependencies

* Apache2 (the version we have tested is 2.4.29)
* Sqlite3 (the version we have tested is 3.25.2)
* Pandas (the version we have tested is 0.23.4)

### Steps

1. Clone the cloud labeler package from GitHub by typing the following command.

    ```
    git clone https://github.com/anhaidgroup/cloudlabeler.git
    ```

2. Copy or replace the /html and /cgi-bin folders in the Apache Web Root (usually /var/www/html). If your Apache Web Root is /var/www/html, you can copy or replace the /html and /cgi-bin folders by typing the following command.

  ```
  rm -r /var/www/html
  rm -r /var/www/cgi-bin
  cp -r /html /var/www/html
  cp -r /cgi-bin /var/www/cgi-bin
  ```
  
  If you are asked 'rm: remove directory?', type 'y'.
  If you are told that 'rm: cannot remove directory: No such file or directory', it's fine.
  
  <details><summary markdown='span'>Don't know where is your Apache Web Root?</summary> 
  <br />
  You can find your Apache Web Root in the file '/etc/apache2/sites-available/000-default.conf'. Type the following command:
  
  ```
  cat /etc/apache2/sites-available/000-default.conf
  ```
  
  In this file, you should find a line like this: 'DocumentRoot /somepath'
  The path after DocumentRoot (/somepath in the example) is your Apache Web Root.
</details>
  
3. Set both /cgi-bin/ and /html/api/ folders to have CGI execution permission. You can learn how to set CGI execution permission from https://httpd.apache.org/docs/2.4/howto/cgi.html. If you are using Ubuntu 18.04, you can add execution permission for /cgi-bin/ and /html/api/ folders by replacing /etc/apache2/apache2.conf and /etc/apache2/conf-available/serve-cgi-bin.conf using the [apache2.conf](./apache2.conf) and [serve-cgi-bin.conf](./serve-cgi-bin.conf) files we have provided.

4. Set every python file in /cgi-bin/ (including download.csv) and /html/api/ to have execution permission for all users. Set the files in /cgi-bin/data to have read and write permission for all users. For example, if your Apache Web Root is /var/www/html, type:

    ```
    chmod -R 755 /var/www/cgi-bin
    chmod -R 755 /var/www/html/api
    chmod -R 666 /var/www/cgi-bin/data
    chmod 755 /var/www/cgi-bin/data
    ```

5. Enable CGI service and restart Apache2. You are all set.
    
    ```
    sudo a2enmod cgi
    sudo service apache2 restart
    ```
    
## Deploying on AWS

### Platforms

Ubuntu Server 18.04 LTS (HVM)

### Dependencies

* Docker (the version we have tested is 18.06.1-ce)

In the approaches below, we will provide existing docker image for easy use. If you want to customize your docker image, we also prepare [deploy.sh](./deploy.sh) file to help you build your own docker image and [takedown.sh](takedown.sh) file to help you clean up the docker image later. You may need to create your [Docker Hub](https://docs.docker.com/docker-hub/) account and push your docker images so that you can access them later from AWS machine.

We offer two approaches to deploy cloud labeler on AWS. Approach 1 is to connect to your AWS machine directly and run docker image yourself. Approach 2 is to use Elastic Container Service, an advanced container orchestration service, to run docker image automatically. 

<details><summary markdown='span'>How can I know which approach to use?</summary> 
<br />
If you are unsure about which approach to choose, you can consider the following factors:
<br />
<br />
    
Use Approach 1 if you
* know how to connect to AWS machine using SSH.
* want to deploy cloud labeler quickly and easily.
* only have access to an existed EC2 instance but don't have permission to launch a new EC2 instance.

Use Approach 2 if you
* want to run cloud labeler in an existed ECS cluster.
* want to run cloud labeler at a high scalability and performance.
* want to let different people manage cloud labeler and also ensure security.
</details>

### Approach 1

1. We use [AWS](https://aws.amazon.com/), a secure cloud services platform, as the platform to deploy cloud labeler. If you don't have an AWS account, click [here](https://portal.aws.amazon.com/billing/signup#/start) to create a new account. 

      - After you have created your account, you need to sign up. In [AWS](https://aws.amazon.com/) homepage, click "complete sign up" button at the top-right corner. You need to enter Email address and Password of your AWS account to sign up.
      - After you have signed up, you need to sign in the console. In [AWS](https://aws.amazon.com/) homepage, the button at the top-right corner should display: "sign in the console". Click it and sign in your console. Now you are in your console page.

2. We use [EC2](https://aws.amazon.com/ec2/), a cloud computing service provided by AWS, to help you deploy cloud labeler.
      
      - In your console page, you can find a panel named 'AWS services' in the beginning which allows you to search for all AWS services. Search and enter [EC2](https://aws.amazon.com/ec2/) in the 'AWS services' panel. Now, you should be in EC2 home page. 
      
3. EC2 provides instance, a cloud virtual machine, as the server to deploy cloud labeler. We now need to create an EC2 instance.   

      - First find 'Instances' in the right panel of EC2 home page and click it. You are now in the EC2 instance page. 
      
      - Next, find and click on the blue button 'Launch Instance' in the EC2 instance page. You are now in your EC2 instance configuration page.
      
4. Now, you need to configure our EC2 instance in the EC2 instance configuration page so that cloud labeler could be successfully deployed.      
   
      - Choose 'Ubuntu Server 18.04 LTS (HVM)' as your Amazon Machine Image in "Step 1: Choose an Amazon Machine Image (AMI)" in your EC2 instance configuration page. 
   
      - EC2 provides different 'Instance Types' optimized to fit different use cases. You can choose your 'Instance Type' in "Step 2: Choose an Instance Type" in your EC2 instance configuration page.
      
        - If you are a new user, we recommend 't2.micro' as your 'Instance Type' because AWS provides 750 Hours free 't2.micro' EC2 instance usage for 12 months.
        
        - If you are an old user, or if you run out of your free tier, you can choose a different 'Instance Type' to meet your demands. For example, you may choose 't2.nano' EC2 instance which is sufficient in the common cases.
        
        - <details><summary markdown='span'>Don't know whether I have run out of free tier?</summary>
            You can find your free tier in AWS bill. Go to https://console.aws.amazon.com/billing/home to enter AWS bill Page. You then need to find the bill for current month. In AWS bill Page, click 'bills' to enter AWS bills page. AWS bills page list your bills for all months. In the drop-down list under 'Dates', choose current month. You now can find the bill for current month. In the bill for current month, you can find a section called 'Elastic Compute Cloud'. Click and expand this section. You can find the number of hours your free tier has been consumed in the row starting with '$0.00 per Linux t2.micro instance-hour (or partial hour) under monthly free tier'. For example, if you have run 'Linux t2.micro instance' for 700 Hours, you are likely to run out of free tier soon.</details>
    
      - For "Step 3: Configure Instance Details", "Step 4: Add Storage", "Step 5: Add Tags" in your EC2 instance configuration page, you can leave the options as default. 
   
      - In "Step 6: Configure Security Group" of your EC2 instance configuration page, you need to build a set of firewall rules to protect your EC2 instance from attacks.
      
         - You first need to determine the protocols that are open to your EC2 instance network traffic in the 'Type' column. Your protocols should include both 'SSH', by which you connect to your EC2 instance, and 'HTTP', by which users visit the cloud labeler. You can also add other protocols you need here.
         
         - Then, you need to determine the traffic that can reach your EC2 instance for each protocol in the 'Source' column. For 'SSH' protocol, you should choose 'My IP' in the common cases because it is unsafe to let other people access your EC2 instance directly by 'SSH'. For 'HTTP' protocol, you should choose 'Anywhere' in common cases because you want to let other people label tuple pairs through cloud labeler you have deployed by 'HTTP'.
      
      - In "Step 7: Review Instance Launch" of your EC2 instance configuration page, you can review all the configurations of your EC2 instance. You can go back to the steps before if you need to do some modifications. After that, you can click "launch" button at the bottom-right corner of your EC2 instance configuration page to complete your configuration.
   
      - After clicking 'Launch', you need to download a private key file to allow you to securely SSH into your instance. 
      
        - If you already have a private key file, you can use the old private key file to securely SSH into this EC2 instance without creating a new one. Select 'Choose a new key pair' in the first drop-down list, and select the key pair you want to use for this EC2 instance in the second drop-down list. 
        
        - If you don't have a private key file, choose 'Create a new key pair', enter your key pair name and download the private key file. You need to save the private key file in a secure place in your local machine.
      
   <details><summary markdown='span'>Already have your deployed instance?</summary><br /> 
      If you want to deploy cloud labeler on an existed EC2 instance, your existed EC2 instance must meet some requirements. Click on your instance in EC2 instance page and check its description shown below. 
   
      - Its AMI ID should include 'ubuntu-bionic-18.04'. 
   
      - In its Security groups, the inbound rules should include both 'SSH' and 'HTTP'. For 'SSH', your local IP should be included in its 'Source' so that your local machine can reach your EC2 instance by 'SSH'.
    
      - Otherwise, you need to launch a new instance to deploy cloud labeler.
 </details>

5. Now, you need to connect to EC2 instance you just created using [SSH](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html) to deploy cloud labler. After connection, you are now in the Command Shell of your EC2 instance.


    <details><summary markdown='span'> Don't know how to connect to EC2 instance using SSH? </summary><br /> 
  
  
   If the system of your local machine is Linux or Mac,
  
   - In the end of step 1, you should download a private key file and it is a pem file. Set the permission of the pem file to be read only for the owner. For example, if your pem file is at /path/my-key-pair.pem, type:
   
   ```
   chmod 400 /path/my-key-pair.pem
   ```
   
   - Use ssh command in your local machine to connect to the EC2 instance. You need to specify your private key file location, user name and host name in your ssh command. The user name should be 'ubuntu'. You can find the host name of your EC2 instance by clicking your EC2 instance in EC2 instance page and check 'Public DNS (IPv4)' in its description below. For example, if your pem file is at /path/my-key-pair.pem and your Public DNS (IPv4) is ec2-198-51-100-1.compute-1.amazonaws.com, type:
   
   ```
   ssh -i /path/my-key-pair.pem ubuntu@ec2-198-51-100-1.compute-1.amazonaws.com
   ```
   
   - Type 'yes' when asked. You are now in the Command Shell of your EC2 instance.
   
   If the system of your local machine is Windows, we recommend a convenient tool.
   
   - Download and install [Putty](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html), an SSH and telnet client，in your local machine.
     
   - In the end of step 1, you should download a private key file in your local machine and it is a pem file. In order to use ssh client on Windows, you need to first convert it the private key file to a ppk file. 
   
      - Open 'Putty Key Generator' in your local machine and Load the Key Pair pem file in 'Load an existing private key file' section. 
      
      - Then, choose 'Save private key' and save Key Pair as ppk file in your local machine. 
   
   - Now, open 'Putty' and build connection to your EC2 instance. First, you need to specify which machine you want to SSH. 
   
     - You need to find the 'Host name' of your EC2 instance.  In EC2 instance page, find the EC2 instance you want to connect and click on it. You can see its description appears below. You can find its 'Host name' in the 'Public DNS (IPv4)' or 'IPv4 Public IP' in its description.
     
     - Open Putty in your local machine. Enter the 'Host name' of the EC2 instance you want to connect in Putty. 
   
   - Then, you need to specify the private key file for SSH connection. In the left panel of 'Putty' in your local machine, choose Connection->SSH->Auth. In 'Private key file for authentication', choose the ppk file generated by 'Putty Key Generator' in your local machine.
   
   - Click 'Open' at the bottom-right corner of Putty. You are now in the Command Shell of your EC2 instance.
</details>
  
6. In the Command Shell of your EC2 instance, if you haven't logged in, the first prompt should be 'login as'. To login, type 'ubuntu' in the Command Shell of your EC2 instance because the default user name in ubuntu is 'ubuntu' and the default password is empty. 

7. Install Docker in your EC2 instance to help you deploy run cloud labeler in your EC2 instance. In the Command Shell of your EC2 instance, you should type the commands specified in [Docker installation tutorial](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce) to install Docker.

8. After you have installed Docker in your EC2 instance, you need to build the Docker image to run. You can pull the existing Docker image from Docker Hub we provide by typing the following command in the Command Shell of your EC2 instance.

    ```
    sudo docker pull zachary62/apache_labeler
    ```
   
    <details><summary markdown='span'> Using your own Docker image?</summary>
    <br />
  
    If you are using your own Docker image, you should pull it from your own Docker Hub. For example, if your Docker Hub repository name is John/apache_labeler, type:
   
     ```
    sudo docker pull John/apache_labeler
    ```
    </details>


9. After you have pulled Docker image, you can run it in your EC2 instance. In the Command Shell of your EC2 instance, run the Docker image in your EC2 instance by typing the following command:

    ```
    sudo docker run -dit --name labeler -p 80:80 zachary62/apache_labeler
    ```
    <details><summary markdown='span'> Using your own Docker image?</summary>
    <br /> 

    If you are using your own Docker image, you should use your own container name. For example, if your container name is John/apache_labeler, type
    
    ```
    sudo docker run -dit --name labeler -p 80:80 John/apache_labeler
    ```
</details>

10. Now, you should be able to use cloud labeler from the web. You can find the IP address of your EC2 instance by clicking on the EC2 instance in EC2 instance page and check 'IPv4 Public IP' in its description below. Append ':80' to your IPv4 Public IP. For example, if your 'IPv4 Public IP' is '1.2.3.4', you can visit cloud labeler in 'http://1.2.3.4:80/' in your local machine (or any other machine whose IP address is included in the 'Source' of 'HTTP' in step 3).
    
11. When you are done, you may need to remove the image and container in your EC2 instance. You should type the following command in the Command Shell of your EC2 instance:
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

3. [Configure your cgi and set keys](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html) on your local machine so that it has access to your AWS account. If you aren't an IAM user, you need to first [Creating an IAM User and Group (AWS CLI)](https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html).

4. [Create your repositories in AWS ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-create.html). Note that the name of repository should be 'apache_labeler' (or you will need to do more configurations to let docker identify your image). 

5. After you have created your repository, you should be able to find a 'View Push Commands' button in the repository page. Here it will list all the commands needed to push Docker image. Follow the commands carefully and push your Docker image to ECS repository. **Note: 1. you don't need to recreate docker image. 2. read the step 2 of push commands carefully**.

6. Create [Task Definition in AWS ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html). You should use the url of the repository you have pushed as the container.

7. Create [Cluster in AWS ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_clusters.html). The cluster template should be EC2 Linux and the Launch type should be EC2. 

8. After you have created a cluster, you should be able to create [service](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html) in cluster page. Notice to choose the task you just created.
 
9. You should be able to find the deployed instances in [AWS EC2](https://aws.amazon.com/ec2/). Find 'instance' on the left panel and find the service you have just created. You can get the address of your instance directly in the IPv4 Public IP below. 

## User Manual

### Page Content

On the left side, there are three panels:

1. The top panel is Label Summary Panel. It shows a summary counts of different label types **saved**.

2. The middle panel is Filter Panel. It allows users to select a subset of label types and view or re-label them in the Main Panel. Users can select multiple label types. 

3. The bottom panel is Upload Panel. It allows users to upload and create their own tables.

Main Panel is on the right side. You can label and view tuple pairs for each pair. On the top there are three buttons. The 'Load Table' button allows you to load new table from database (and you should save current table before loading new one). The 'Download CSV' button allows you to download the CSV of current table. The 'Save and Continue' button allows you to save current table in database.

### Labeling

In order to label your own table, you need to follow the steps below:

First, upload your CSV files and choose your table name in Upload Panel.

Next, load the table you have uploaded using 'Load Table' button.

Then, label your pairs in the Main Panel. 

After that, save your table using 'Save and Continue' button. You can close the page and label the pairs later if you have saved the table.

Finally, download the final CSV file of the table you have saved using 'DownLoad CSV' button.

### Rest API

You can learn how to use REST api from [notebook](./notebooks/api.ipynb) (you need to install requests package).
