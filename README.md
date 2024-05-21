
### 

for creating tables inside container postgres db
GET http://localhost:8000/setup/

companies GET API:
GET: http://localhost:8000/companies/?filter_text=sam&filter_name=company_name&filter_type=fuzzy

contacts GET API:
GET: http://localhost:8000/contacts/?limit=5&job_level=Senior&job_function=Sales&job_title=baba55c144


Running on Local:

```docker-compose up --build```

For testing test cases

Run ```pytest```

API Documentation avaialble on: 

```http://localhost:8000/docs```

API Gateway Research Doc:
```https://docs.google.com/document/d/1mosND-Kw8jRGsJ20Fz4n6EVa3wnMdxQrG-Gm3OZPd7U/edit?usp=sharing```


Note:  I had created JWT authentication as well as demostrated auth0 authentication

################################ API Gateway Example ################################

Run API Gateway:
```uvicorn api_gateway:app --host 0.0.0.0 --port 8000```

service 1 will run on: ```http://localhost:8000``` command: (python3 start_server.py)
service 2 will run on: ```http://localhost:8001``` command: (python3 api_v2.py)



all request will come to : http://localhost:8005 and target respective endpoint server 

service 1 API:
    APIs auth based on JWT auth:
        GET root API       : http://localhost:8005/v1/
        POST register API  : http://localhost:8005/v1/register/

        Headers bearer token need to pass in following APIs:
            GET profile API    : http://localhost:8005/v1/users/me/
            GET contacts API   : http://localhost:8005/v1/contacts/
            GET companies API  : http://localhost:8005/v1/companies/

service 2 api:
    GET http://localhost:8005/v2/


Note: i had implamented auth0 integration as well to get access_tokemn as well for this seprate function for this 

#####################################################################################

