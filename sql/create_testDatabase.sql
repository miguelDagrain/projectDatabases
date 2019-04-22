CREATE ROLE testpdb WITH LOGIN PASSWORD 'test';
ALTER ROLE testpdb CREATEDB;
CREATE DATABASE testpdbDatabase owner testpdb;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testpdb;
--voor ubuntu moet ge eerst nog als postgress in de database gaan en  'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pdb' typen