# feup-dapi
Work developed for DAPI course @ MIEIC, FEUP. Made with @diogotorres97

## Solr instructions
Given local binaries and terminal session inside main folder (e.g., `solr-8.2.0`):
1) Start Solr instance: `./bin/solr start -f` (-f = foreground execution, optional)
2) Create collection (core), if not existent: `./bin/solr create -c dapi`
3) Add document schema (import `DAPI.json` into Postman and run the endpoint stored)
4) Import documents into Solr: `./bin/post -c dapi ~/Desktop/feup-dapi/games.json`
5) Open Solr Admin UI at `localhost:8983`and get to work!