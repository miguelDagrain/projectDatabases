CREATE ROLE pdb WITH LOGIN PASSWORD 'hunter2';
ALTER ROLE pdb CREATEDB;
CREATE DATABASE pdbDatabase owner pdb;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pdb;
--voor ubuntu moet ge eerst nog als postgress in de database gaan en  'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pdb' typen