CREATE DATABASE if not exists email_accounts;

USE email_accounts;

CREATE TABLE if not exists mailboxes (
    id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    domain_id INT(10) NOT NULL,
    local_part VARCHAR(250) NOT NULL,
    password VARCHAR(100) NULL,
    description VARCHAR(250) NULL,
    active TINYINT(1) NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    modified TIMESTAMP NULL
);
CREATE TABLE if not exists aliases (
    id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    domain_id INT(10) NOT NULL,
    local_part VARCHAR(250) NOT NULL,
    goto VARCHAR(250) NOT NULL,
    description VARCHAR(250) NULL,
    active TINYINT(1) NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    modified TIMESTAMP NULL
);
CREATE TABLE if not exists vacations (
    id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    mailbox_id INT(10) NOT NULL,
    subject VARCHAR(250) NOT NULL,
    body TEXT NOT NULL,
    description VARCHAR(250) NULL,
    active TINYINT(1) NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    modified TIMESTAMP NULL
);
 
CREATE TABLE if not exists domains (
    id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fqdn VARCHAR(250) NOT NULL,
    type ENUM('local','relay') NOT NULL DEFAULT 'local',
    description VARCHAR(250) NULL,
    active TINYINT(1) NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    modified TIMESTAMP NULL
);

INSERT INTO domains VALUES(NULL,'box.lan','local','My nice domain for local delivery',1,NOW(),NOW());
INSERT INTO mailboxes VALUES(NULL,1,'admin',MD5('changeme'),'My account for admin@box.lan',1,NOW(),NOW());
