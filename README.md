# Stellar-Dashboard

Scan the history archives of a stellar network, and create a dashboard to monitor all payments/trustline for an asset.

![Screenshot](https://i.imgur.com/iSoIHey.png)

## How does it work?
The python script constantly downloads files from a given S3 bucket, parses them using [xdrparser](https://github.com/kinecosystem/xdrparser), filters payments and trustlines for a given asset and store these operations in a [postgres SQL](https://www.postgresql.org/) database.  
In addition, [grafana](https://grafana.com/) is also available and can be used to create graphs from the collected data.

## Notes
* Only payment and trustline operations are saved to database.
* For payments, only : source, destination,amount,memo **text**,tx hash, and timestamp are saved.
* For truslines, only: source, memo **text**, tx hash, and timestamp are saved.
* The source account will be the source of the operation, if it exists.
* The services have persistent storage, so if any of them fails/crashes, you should be able to turn them on again and everything will continue from the same place, no need to start scanning all the files from the start again.

## Prerequisites
1. Install [docker](https://docs.docker.com/install/)
2. Install [docker-compose](https://docs.docker.com/compose/install/)

## Configuration
Edit the docker-compose file to configure it

|          Variable          | Description                                                                                                                                                                                                                     |
|:--------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| POSTGRES_PASSWORD          | Master password for the postgres database                                                                                                                                                                                       |
| PYTHON_PASSWORD            | Password for the postgres user 'python'                                                                                                                                                                                         |
| GRAFANA_PASSWORD           | Password for the postgres user 'grafana'                                                                                                                                                                                        |
| ASSET_CODE                 | Asset code to track                                                                                                                                                                                                             |
| ASSET_ISSUER               | Issuer of the asset to trust                                                                                                                                                                                                    |
| FIRST_FILE                 | The first file to download If you know the ledger sequnce, it can be calculated by: X = Ledger number Y = Round up the result of X/64 File = hex(Y * 64 - 1) Add '0' from the left until its 8 letter long (0x5b3f >> 00005b3f) |
| NETWORK_PASSPHRASE         | The passpharse/network id of the network                                                                                                                                                                                        |
| MAX_RETRIES                | Max number of tries to download a file before quitting, there is a 3 minute wait time between each try.                                                                                                                         |
| BUCKET_NAME                | S3 bucket name                                                                                                                                                                                                                  |
| CORE_DIRECTORY             | The path leading to transactions/ledger/results... folders, can be empty                                                                                                                                                        |
| GF_AUTH_ANONYMOUS_ENABLED  | Allow unsigned users to view the grafana dashboards                                                                                                                                                                             |
| GF_SECURITY_ADMIN_USER     | Grafana admin username                                                                                                                                                                                                          |
| GF_SECURITY_ADMIN_PASSWORD | Grafana admin password                                                                                                                                                                                                          |

## Usage
To start the proccess with a clean slate (**THIS WILL DELETE ANY PREVIOUS DATA IN YOUR DATABASE/GRAFANA**)
```
$ ./init.sh
```
To turn on a service that crashed:
```
$ sudo docker-compose up -d <name of service> (either grafana/db/ETL)
```
You can now access grafana on [localhost](http://localhost), and the postgres database on localhost:5432.

Add the database as a datasource for grafana:  
![Screenshot](https://i.imgur.com/6Xpq64O.png)

An example preconfigured dashboard (The one from the first pic) can be imported from the grafana folder.
