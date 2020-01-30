/*

For more information on how to load the script and explanation of code:
http://www.mysqltutorial.org/import-csv-file-mysql-table/

*/

LOAD DATA INFILE '.drug.csv'
INTO TABLE drug
FEILDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '.substance.csv'
INTO TABLE substance
FEILDS TERMINATED BY ','
LINES TERMINATED BY '\n';

LOAD DATA INFILE '.interactions.csv'
INTO TABLE interactions
FEILDS TERMINATED BY ','
LINES TERMINATED BY '\n';
