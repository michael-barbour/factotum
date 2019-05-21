# Factotum Docker

A collection of `docker-compose` scripts for running the Factotum service stack.

### Compositions

There are three Docker compositions you can use:

* ["elk"](#elk-composition)
* ["elk_sql"](#elk_sql-composition)
* ["full"](#full-composition)

### Setup

Make sure you have the following repos and branches checked out:
* [`factotum_elastic/799_factotum_chemicals_envvar`](/HumanExposure/factotum_elastic/tree/799_factotum_chemicals_envvar)
* *("full" only)* [`factotum_ws/dev`](/HumanExposure/factotum_ws/tree/dev)

Also, make sure you don't have a preexisting service running on one of the [ports your composition will occupy](#services).

1. Make a copy of the "template.env" to a file named ".env". Edit it to what you want.
2. Make corrections to your "settings_secret.py" as suggested in the composition's "docker.settings_secret.py.template"
3. Run `docker-compose up -d`. It will take a while the first time.
4. *("elk_sql" and "full" only)* Run `manage.py migrate` and `manage.py loadalldata`
5. Run `manage.py rebuild_index` to populate the legacy Elasticsearch v2 indexes.
6. Run `docker-compose run --rm logstash` to populate the Elasticsearch v6 indexes.

#### Rebuilding images

Whenever...

* pipelines are added to "factotum_elastic/pipelines/"
* mappings are added to "factotum_elastic/mappings/"
* a "requirements.txt" file is changed

...you must rebuild the images with`docker-compose build`.

#### Changing the ".env"

Whenever you change your ".env" file, you must restart the services with `docker-compose down` followed by `docker-compose up -d`.

### Command Cheatsheet

* `docker-compose up -d`: start services in the background
* `docker-compose up -d mysql elasticsearch2`: just start these services
* `docker-compose down`: stop services
* `docker-compose run --rm logstash`: run Logstash pipelines
* `docker-compose build`: rebuild the containers after making any changes to your configuration

With the "full" composition, replace your `python manage.py` command with `docker-compose run --rm factotum` or `docker-compose run --rm factotum-ws`.

### Services

#### "elk" composition

* **Elasticsearch v2:** `localhost:9202`, `localhost:9302`
* **Elasticsearch v6:** `localhost:9200`, `localhost:9300`
* **Logstash:** n/a
* **Kibana:** `localhost:5601`

#### "elk_sql" composition

* all of the above
* **MySQL:** `localhost:3306`
* **MySQL Test:** n/a *(config'd for faster testing)*

#### "full" composition

* all of the above
* **Factotum:** `localhost:8000`
* **Factotum web services:** `localhost:5000`
