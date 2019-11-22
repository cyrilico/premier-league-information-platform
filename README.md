# feup-dapi
Work developed for DAPI course @ MIEIC, FEUP. Made with @diogotorres97

## 2nd Milestone
### Start Solr, define schema and import/index data
Given local binaries and terminal session inside main folder (e.g., `solr-8.2.0`):
1) Start Solr instance: `./bin/solr start -f` (-f = foreground execution, optional)
2) Create collection (core), if not existent: `./bin/solr create -c dapi` (to delete previous instance, run `delete` command with same arguments)
3) Copy synonyms from `my_synonyms.txt` to synonyms.txt file to be indexed by Solr (`.../solr-8.2.0/server/solr/dapi/conf/synonyms.txt`)
3) Define document schema (import `DAPI.json` into Postman and run the endpoint stored)
4) Import documents into Solr: `./bin/post -c dapi path/to/repository/clone/feup-dapi/games.json`
5) Open Solr Admin UI at `localhost:8983` and get to work!
