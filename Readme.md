<h1> CRYPTO PRICE CHECKER </h1>

 - <b>Programming language:</b> Python
 - <b>Database:</b> sqllite
 - <b>Deployed using:</b> Docker


<h2> Points to Note </h2>

- The Database file is "crypto.db" and already has the table created
- Schema of the table can be viewed in <b>tables.sql </b> file

<h2>Following containers are configured:</h2>

1. base_image
<br>
Constructs the base image for running python code
2. api
<br>
Exposes API to query the data for a date and range
3. poller
<br>
Polls the CoinGecko API to load the prices every 30 seconds

<h2> Prerequisites</h2>

1. You need to have port 5005 free on your machine for the API to run, if you need to still have it busy, change system port in "ports" section of api service in <b>docker-compose.yml</b>
2. Internet connection is required to download resource to create the base image


<h2> Sample API call</h2>

You can test the API using following call

```bash
curl --location --request GET 'http://localhost:5005/api/prices/btc?date=14-08-2022&offset=0&limit=10' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id" : "bitcoin"
}'
```