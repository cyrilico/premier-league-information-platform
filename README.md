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

### Things to quickly show (features to be explored):
1) Normal search by field (e.g., all matches played by Arsenal at home: `home:arsenal`)
2) Synonym search (e.g., repeat last query but instead of arsenal, use synonym `gunners`; search `arena:anfield` and then `arena:kop` for example in other field; **multi-word synonyms need to be queried in one of the two following ways: 1) setting df to the desired search field, passing parameter sow=false and entering search query normally or 2) phrase search by field, e.g., home:"red devils"**)
3) Wildcard search (e.g., search for `home:man*`, should return 190 results, 95 home games by Manchester United + 95 home games by Manchester City)
4) Boosts (some fields more relevant than others) - *To be added*
5) Boolean queries (e.g., search for all matches between Arsenal and Chelsea (10 results, 2 games per season): `(home:arsenal AND away:chelsea) OR (home:chelsea AND away:arsenal)`)
6) Faceting (group by) - (e.g., simple example number of matches grouped by date: leave default query `*:*`, set `facet` on, `facet.field` to date and `rows` to 0 for clearer output of facets)
7) Proximity search - (e.g., search for all matches whose report mention "eriksen free kick" within 10 words of each other: `report:"eriksen free kick"~10` - note that Christian Eriksen is a famous and the usual free kick taker at Tottenham)
7) Fuzziness (typos/edit distance) (e.g., search for all Tottenham's home games, misspelling its name: `home:tottnam~2` - 2 represents max edit distance, which can vary between 0 and 2 in standard query parser)
8) Custom ranking - *To be added/Haven't checked how to do yet*
9) Range filters - *To be added/Haven't checked how to do yet*

### Stuff
- If no fields specified in query, the search will default to the report field (there is no native support for all fields, must create a [copy field](https://lucene.apache.org/solr/guide/8_2/copying-fields.html) that captures all document text into one field, which envolves double the memory usage and double the indexing effort (pointless here)

### Questions
Check Google Keep note.
