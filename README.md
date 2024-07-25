# Wildfires & Recreational Trails Data Engineering Project
As part of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by [DataTalks.Club](https://datatalks.club), this project marks the final component of the course. Sending my thanks to the instructors that contributed to building this educational resource.

## Purpose
The purpose of this project is to design a prototype of a data pipeline based on wildfire activity and recreational trails in British Columbia (BC), Canada.

[Statistics](https://www2.gov.bc.ca/gov/content/safety/wildfire-status/about-bcws/wildfire-history) from the 2023 wildfire season:
  - 2,245 wildfires burned more than 2.84 million hectares of forest and land.
  - 29,900 calls were made to the Provincial Wildfire Reporting Centre, generating 18,200 wildfire reports.
  - An estimated 208 evacuation orders which affected approximately 24,000 properties and roughly 48,000 people. An estimated 386 evacuation alerts which affected approximately 62,000 properties and roughly 137,000 people.


With summers in BC being the main period for wildfires, it is also the season during which outdoor recreational activity is most popular. The province is well-known for its beautiful, mountainous, and coastal landscape with ample opportunity for hiking, camping, mountain biking, and more.

This project produces a web map application displaying wildfire perimeters and recreational trails identified within 20 kilometers.

## Web Map

## Data Stack
- **Development Platform**: Docker
- **Infrastructure as Code (IAC)**: Terraform
- **Orchestration**: Apache Airflow
- **Data Lake**: Google Cloud Storage
- **Data Warehouse**: Google Big Query
- **Transformation Manager**: Data Built Tool (DBT)
- **Data Visualization**: Dekart (built on top of kepler.gl and mapbox)

### Architecture

## Data Sources and Limitations
- All data was obtained through the BC Data Catalogue.
  - (Attribution: Contains information licensed under the [Open Government Licence – British Columbia](https://www2.gov.bc.ca/gov/content/data/policy-standards/open-data/open-government-licence-bc))
- **BC Wildfire Fire Perimeters - Current**:
  - This is a spatial layer of polygons showing both active and inactive fires for the current fire season. The data is refreshed from operational systems every 15 min. These perimeters are rolled over to Historical Fire Polygons on April 1 of each year.
  - Limitations: *Wildfire data may not reflect the most current fire situation as fires are dynamic and circumstances may change quickly. Wildfire data is refreshed when practicable and individual fire update frequency will vary.*
- **Recreation Line**:
  - This is a spatial layer of polylines shows features such as recreation trails.
  - Limitations: *These polylines represent recreational trails and may not include recreational projects where polygon features would be more appropriate. Trails that are not registered within the BC Minstry of Forests are not included. Data is not updated on a regular schedule.*
