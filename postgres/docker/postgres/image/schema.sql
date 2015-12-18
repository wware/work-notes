CREATE SEQUENCE organization_id_seq;
CREATE SEQUENCE user_id_seq;

CREATE TABLE organization (
    id smallint NOT NULL DEFAULT nextval('organization_id_seq'),
    name text NOT NULL,
    active boolean DEFAULT false
);

CREATE TABLE users (
    id smallint NOT NULL DEFAULT nextval('user_id_seq'),
    name character varying(16) NOT NULL,
    password text NOT NULL,
    organization_id smallint
);

ALTER SEQUENCE organization_id_seq OWNED BY organization.id;
ALTER SEQUENCE user_id_seq OWNED BY users.id;
