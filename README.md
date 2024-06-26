# Car Park Utilisation 

## Description

This project is a comprehensive data pipeline designed to provide an extensive overview of car parking usage across Singapore. It facilitates effective planning and resource allocation, ultimately aiming for improved management of car parking facilities.

The data pipeline, deployed on the Google Cloud Platform (GCP), operates by pulling data every 15 minutes from the data.gov.sg API via a batch job. This data is then enhanced with car park location details and subsequently stored in a data lake, specifically Google Cloud Storage. At the close of each day, another batch job is executed to further transform the data and transfer it to a data warehouse, Google BigQuery. Visualization of this data is carried out in Google Looker Studio, which provides users with vital insights into peak usage times of car parks both island-wide and at individual parking facilities.

This project aims to improve car parking planning and management by providing detailed hourly data on parking utilization, enabling informed resource allocation. It addresses the critical need for effective planning solutions, recognizing the impact of parking availability on traffic congestion, urban mobility, and business operations. By enhancing understanding of parking space utilization, it seeks to support better planning decisions, improve efficiency, and enhance urban transportation systems.

![Project Architecture](https://github.com/rxl204/car-parking-project/blob/main/car-parking-proj-architecture-diagram.png)

## Installation

### Prerequisites

1. Git
2. Terraform
3. Docker
4. Set up a GCP account and install gcloud CLI
5. Mage - an open-source, hybrid framework for transforming and integrating data

### Usage

#### For the pipeline scripts:

1. Clone the repository:
    ```
    git clone https://github.com/rxl204/car-parking-project.git
    ```
2. Navigate to the project directory:
    ```
    cd car-parking-project
    ```
3. Install gcloud CLI. For detailed steps see: [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs/install)

#### Set up Google Cloud Permissions:

1. Set up permissions for the service account, download the JSON credential file
2. Set GOOGLE_APPLICATION_CREDENTIALS to point to the JSON credential file

#### Deploying Mage pipeline to Google Cloud using Terraform:

To reproduce the steps, you'll need to install Terraform. For detailed steps see: [Using Terraform with Mage](https://docs.mage.ai/production/deploying-to-cloud/using-terraform)

You may choose to work within the mage-ai-terraform-templates directory, navigate to gcp. Before running any Terraform commands for deployment, change the default value of the `project_id` variable in `./gcp/variables.tf`:

    ```
    terraform
    variable "project_id" {
        type        = string
        description = "The name of the project"
        default     = "unique-gcp-project-id"
    }
    ```

To prepare your working directory for other commands, run:
    ```
    terraform init
    ```

To show changes required by the current configuration, run:
    ```
    terraform plan
    ```

To create or update infrastructure, run:
    ```
    terraform apply
    ```
Note: This step will take a few minutes. Once ready, navigate to Cloud Run.
- Select the 'Networking' tab, modify Ingress control to 'All' temporarily
- Navigate to the url like  https://mage-data-prep-xxxx-wl.a.run.app

### Run Mage on Google Cloud
Import pipeline zip files into Mage environment that is running. The pipeline has two parts:
1. Pull car parking data from API, transform and load to data lake (scheduled a trigger at 15 minutes interval, use cron '*/15 * * * *')
2. Pull data from GCS, transform and load to BigQuery data warehouse (scheduled a trigger on a daily basis)
The pipeline has been designed to pull live data. For testing purposes, you may select 'Run@once' to get a sample of the live data.

Finally, to destroy previously-created infrastructure, run:
    ```
    terraform destroy
    ```

### Looker Studio Dashboard
A sample dashboard showing a subset of data extracted using the data pipeline
![Car Parking Dashboard](https://github.com/rxl204/car-parking-project/blob/main/looker_studio.png)
https://lookerstudio.google.com/s/kzuK_HM4K38

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
