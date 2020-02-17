CREATE database ims_drugicomp;
use ims_drugicomp;

CREATE TABLE drug(
  name VARCHAR(50) NOT NULL,
  subst_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (name),
  FOREIGN KEY (subst_name) REFERENCES substance (name)
);

CREATE TABLE substance(
  accession_num VARCHAR(30) NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (name)
);

CREATE TABLE interactions(
  subst_a VARCHAR(50) NOT NULL,
  subst_b VARCHAR(50) NOT NULL,
  level INT NOT NULL,
  FOREIGN KEY (subst_a) REFERENCES substance (name),
  FOREIGN KEY (subst_b) REFERENCES substance (name)
);
