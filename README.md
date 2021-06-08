# YouTubeApi
To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given search query in a paginated response.
# Installation Guide
Follow the Below steps (execute them in the root directory of project)
1. Build a Docker Image
```bash
docker build -t youtubeapi .
```
2. Run the image for running docker container
```bash
docker-compose up -d
```
3. Create a superuser to access the Django Admin Panel
* Access the powershell by running the command
```bash
  docker container exec -it containername/containerId powershell
```
* In the bash run the following command and add username and password for the superuser
```bash
  python manage.py createsuperuser
```
# Api Use
##### A GET API Which Returns The Stored Video Data In A Paginated Response Sorted In Descending Order Of Published Datetime.
##### number of results per page are 10
Give the query parameter page=page_number
```
127.0.0.1:8000/api/v1/view?page=1
```
##### A Basic Search API To Search The Stored Videos Using Their Title And Description.
Give the query parameter q=searchQuery
```
127.0.0.1:8000/api/v1/search?q=priyanka
```
##### Dashboard To View The Stored Videos With Filters On Title Of Videos
```
127.0.0.1:8000/
```
##### To Search From Web Page
```
http://127.0.0.1:8000/searchmain
```
