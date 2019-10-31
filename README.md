# feup-dapi
Work developed for DAPI course @ MIEIC, FEUP. Made with @diogotorres97

## 2nd Milestone
### Start Solr, define schema and import/index data
Given local binaries and terminal session inside main folder (e.g., `solr-8.2.0`):
1) Start Solr instance: `./bin/solr start -f` (-f = foreground execution, optional)
2) Create collection (core), if not existent: `./bin/solr create -c dapi`
3) Append synonyms from our synonyms file to synonyms.txt file to be indexed by Solr (`.../solr-8.2.0/server/solr/dapi/conf/synonyms.txt`)
3) Define document schema (import `DAPI.json` into Postman and run the endpoint stored)
4) Import documents into Solr: `./bin/post -c dapi path/to/repository/clone/feup-dapi/games.json`
5) Open Solr Admin UI at `localhost:8983` and get to work!

### Things to quickly show (features to be explored):
1) Normal search by field (e.g., all matches played by Arsenal at home: `home:arsenal`)
2) Synonym search (e.g., repeat last query but instead of arsenal, use synonym `gunners`; search `arena:anfield` and then `arena:kop` for example in other field)
3) Wildcard search (e.g., search for `home:man*`, should return 190 results, 95 home games by Manchester United + 95 home games by Manchester City)
4) Boosts (some fields more relevant than others) - *To be added*
5) Boolean queries - *To be added*
6) Faceting (group by) - *To be added*
7) Fuzziness (typos/edit distance) - *To be added*
8) Custom ranking - *To be added/Haven't checked how to do yet*
9) Range filters - *To be added/Haven't checked how to do yet*


### Questions
Check Google Keep note.