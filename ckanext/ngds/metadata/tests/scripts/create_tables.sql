-- Table: spatial_ref_sys --

CREATE TABLE spatial_ref_sys
(
  srid integer NOT NULL,
  auth_name character varying(256),
  auth_srid integer,
  srtext character varying(2048),
  proj4text character varying(2048),
  CONSTRAINT spatial_ref_sys_pkey PRIMARY KEY (srid)
);

GRANT ALL ON TABLE spatial_ref_sys TO ckanuser;
GRANT ALL ON TABLE spatial_ref_sys TO public;

-- Table: geometry_columns --

CREATE TABLE geometry_columns
(
  f_table_catalog character varying(256) NOT NULL,
  f_table_schema character varying(256) NOT NULL,
  f_table_name character varying(256) NOT NULL,
  f_geometry_column character varying(256) NOT NULL,
  coord_dimension integer NOT NULL,
  srid integer NOT NULL,
  type character varying(30) NOT NULL,
  CONSTRAINT geometry_columns_pk PRIMARY KEY (f_table_catalog, f_table_schema, f_table_name, f_geometry_column)
);

GRANT ALL ON TABLE geometry_columns TO ckanuser;
GRANT ALL ON TABLE geometry_columns TO public;

-- Table: responsible_party --

CREATE TABLE responsible_party
(
  id serial NOT NULL,
  name text,
  email text,
  organization text,
  phone text,
  street text,
  state text,
  city text,
  zip text,
  CONSTRAINT responsible_party_pkey PRIMARY KEY (id)
);

-- Table: package_additional_metadata --

CREATE TABLE package_additional_metadata
(
  package_id text NOT NULL,
  author_id integer,
  maintainer_id integer,
  pub_date date,
  CONSTRAINT package_additional_metadata_pkey PRIMARY KEY (package_id),
  CONSTRAINT package_additional_metadata_author_id_fkey FOREIGN KEY (author_id)
      REFERENCES responsible_party (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT package_additional_metadata_maintainer_id_fkey FOREIGN KEY (maintainer_id)
      REFERENCES responsible_party (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Table: resource_additional_metadata --

CREATE TABLE resource_additional_metadata
(
  resource_id text NOT NULL,
  distributor_id integer,
  CONSTRAINT resource_additional_metadata_pkey PRIMARY KEY (resource_id),
  CONSTRAINT resource_additional_metadata_distributor_id_fkey FOREIGN KEY (distributor_id)
      REFERENCES responsible_party (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- Table: harvest_node --

CREATE TABLE harvest_node
(
  id serial NOT NULL,
  url text,
  frequency text,
  CONSTRAINT harvest_node_pkey PRIMARY KEY (id)
);

-- Table: harvested_record --

CREATE TABLE harvested_record
(
  id serial NOT NULL,
  package_id text,
  harvest_node_id integer,
  harvested_xml text,
  CONSTRAINT harvested_record_pkey PRIMARY KEY (id),
  CONSTRAINT harvested_record_harvest_node_id_fkey FOREIGN KEY (harvest_node_id)
      REFERENCES harvest_node (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT harvested_record_package_id_fkey FOREIGN KEY (package_id)
      REFERENCES "package" (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)