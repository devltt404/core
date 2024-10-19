# Django Financial Data Analysis System

This is a Django-based backend system that fetches financial data from the Alpha Vantage API, implements a basic backtesting module, integrates a machine learning model for stock price predictions, and generates performance reports.

## Live website

[View live website here](https://trial-task.devltt.site/backtest)

## Table of Contents

1. [Endpoints](#endpoints)
2. [Commands](#commands)
3. [Installation](#installation)

   - [Prerequisites](#prerequisites)
   - [Run Locally](#run-locally)

4. [Deployment to EC2](#deployment-to-ec2)

   - [Setup RDS](#setup-rds)
   - [Setup Github](#setup-github)
   - [Setup EC2](#setup-ec2)

## Endpoints

### Fetch Stock Data

- **URL:** `/fetch-data`
- **Description:** Fetches historical AAPL stock prices over the last 2 years.

### Backtest

- **URL:** `/backtest`
- **Description:** Executes a backtesting strategy on the fetched stock data.

### Predictions

- **URL:** `/predictions`
- **Description:** Provides stock price predictions for the next 30 days based on the trained model.

### Reports

- **URL:** `/reports`
- **Description:** Generates performance reports.
- **Parameters:**
  - `response` (optional): `pdf`
    - Specifies the format of the report. If provided, the report will be generated as a PDF file.
  - `download` (optional): `true`
    - If set to **true** and `response` param is **pdf**, the report will be downloaded. If omitted, the report may be displayed in the browser.

## Commands

### Fetch Stock Data

This command fetches and stores historical AAPL stock prices over the last 2 years.

```
python manage.py fetch_stock_data
```

### Train Model

This command trains a machine-learning model to predict future stock prices for AAPL using historical data. After training, the model will also make predictions on the historical data to make comparisons between predicted and actual prices.

```
python manage.py train_model
```

## Installation

### Prerequisites

- Python 3.12+
- PostgreSQL
- [Alpha Vantage API Key](https://www.alphavantage.co/)

### Run Locally

#### Clone the Repository

```
git clone https://github.com/your_username/financial-data-backend.git
cd financial-data-backend
```

#### Install Dependencies

```
pip install -r requirements.txt
```

#### Setup PostgreSQL

Create a new local PostgreSQL database.

#### Setup Environment Variables

Create a `.env` file:

```
cp .env.example .env
```

Open the `.env` file in a text editor and fill in all keys.

| Variables               | Description                                        |
| ----------------------- | -------------------------------------------------- |
| `DEBUG`                 | Set to `True` to enable Django debug               |
| `SECRET_KEY`            | Django secret key for cryptographic signing.       |
| `ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key for financial data.     |
| `DB_HOST`               | The hostname of your database server.              |
| `DB_PORT`               | The port number for your database (default: 5432). |
| `DB_USER`               | Your database username.                            |
| `DB_PASSWORD`           | Your database password.                            |
| `DB_NAME`               | The name of your database.                         |

#### Run Migrations

```
python manage.py migrate
```

#### Setup Data

Fetch and store stock (AAPL) data over the past 2 years:

```
python manage.py fetch_stock_data
```

Train prediction model and predict old data:

```
python manage.py train_model
```

#### Start Server

```
python manage.py runserver
```

## Deployment to EC2

### Setup RDS

1. **Go to RDS Console**:

- Sign in to the AWS Management Console.
- Navigate to the [RDS Console](https://console.aws.amazon.com/rds/).

2. **Create a Database**:

- Click on **Create database**.
- Choose **Standard create**.

3. **Select Engine**:

- Choose `PostgreSQL` as the database engine.

4. **Templates**: Select `Free tier` template.

5. **Settings**

- **DB Instance Identifier**: Provide a name for your database instance.
- **Master Username**: Set the master username.
- **Master Password**: Set and confirm a strong password.

6. **Public Access**: Select Yes to allow public access to your database.

7. **Create Database**: Review your settings and click on the **Create database button.**

### Setup GitHub

1. Push your code to a GitHub repo.

2. **Setup Secrets Variables**:

   - Go to your GitHub repository.
   - Click on the **Settings** tab.
   - In the left sidebar, click on **Secrets and variables** and then select **Actions**.
   - Click on the **New repository secret** button.

   Add the following secrets:

   | Secret Name             | Description                                        |
   | ----------------------- | -------------------------------------------------- |
   | `SECRET_KEY`            | Django secret key for cryptographic signing.       |
   | `ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key for financial data.     |
   | `DB_HOST`               | The hostname of your database server.              |
   | `DB_PORT`               | The port number for your database (default: 5432). |
   | `DB_USER`               | Your database username.                            |
   | `DB_PASSWORD`           | Your database password.                            |
   | `DB_NAME`               | The name of your database.                         |
   | `DOCKERHUB_USERNAME`    | Your Docker Hub username.                          |
   | `DOCKERHUB_TOKEN`       | Your Docker Hub access token.                      |

### Setup EC2

1. **Access Console**:

   - Sign in to AWS Management Console
   - Go to the [AWS EC2 Console](https://console.aws.amazon.com/ec2/).

2. **Launch Instance**:

   - Click on the "Launch Instance" button.
   - Select an instance type.
   - Adjust the storage size as necessary.
   - Create a new security group or select an existing one.
   - Add rules to allow inbound traffic:
     - HTTP (port 80)
     - HTTPS (port 443) if you plan to set up SSL
     - Custom TCP (port 8000) if you want to run the Django server on its default port.

3. **Review and Launch**:

   - Review your configuration and click **"Launch"**.
   - Select an existing key pair or create a new one to connect to your instance.

4. **Connect to Your Instance**:

   - Choose **Connect** and select **EC2 Instance Connect** tab.
   - For Connection type, choose **Connect using EC2 Instance Connect**.

5. **Install Python 3.12**:

   Execute these commands one by one:

   ```
   sudo yum update -y
   sudo yum groupinstall "Development Tools" -y
   sudo yum install openssl-devel bzip2-devel libffi-devel zlib-devel wget -y
   wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
   tar -xzf Python-3.12.0.tgz
   cd Python-3.12.0
   ./configure --enable-optimizations
   make
   sudo make altinstall
   ```

   Install pip:

   ```
   wget https://bootstrap.pypa.io/get-pip.py
   sudo python3.12 get-pip.py
   ```

   Make python alias for python3.12:

   ```
   alias python=python3.12
   ```

6. **Setup Nginx**:

   Install:

   ```
   sudo dnf install -y nginx
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

   Edit Nginx configuration file:

   ```
   sudo nano /etc/nginx/conf.d/django_app.conf
   ```

   Add the following to `django_app.conf` file:

   ```
   server {
       listen 80;
       server_name your_domain.com;  # Change this to your domain

       location /static/ {
           alias /path-to-your-project/staticfiles/ # Change this
       }

       location / {
           proxy_pass http://127.0.0.1:8000;  # The address where Gunicorn is running
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       error_log /var/log/nginx/my_django_app_error.log;
       access_log /var/log/nginx/my_django_app_access.log;
   }
   ```

   Reload Nginx:

   ```
   sudo systemctl reload nginx
   ```

7. **Install Docker**:

   ```
   sudo yum install docker -y
   ```

8. **Setup GitHub Runner**:

   - Download the GitHub Actions runner:

   - In your GitHub repository, navigate to Settings > Actions > Runners.
   - Click **New self-hosted runner**.
   - Choose **Linux** OS.
   - Follow the GitHub instructions to download the runner application and configure it.
   - Start the runner:

   ```
   ./svc.sh install
   ./svc.sh start
   ```

9. **Access Your Web Server**:

   After configuring everything, you can access your application by navigating to `http://your_ec2_ip_address` in your web browser.
