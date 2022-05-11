-- JngMkk
DROP TABLE IF EXISTS weather;
CREATE TABLE weather (
    weatherID   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    areaNo      BIGINT NOT NULL,
    si          VARCHAR(30) NOT NULL,
    time        INT NOT NULL,
    condi       VARCHAR(30) NOT NULL,
    isDay       INT NULL,
    temp        INT NULL,
    humidity    INT NULL,
    humidInfo   VARCHAR(50) NULL,
    rainRatio   INT NULL,
    snowRatio   INT NULL,
    uv          INT NULL,
    uvInfo      VARCHAR(50) NULL
);

DROP TABLE IF EXISTS plants;
CREATE TABLE plants (
    plantID         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    URL             VARCHAR(255) NOT NULL,
    name            VARCHAR(255) NOT NULL,
    botanyNm        VARCHAR(255) NOT NULL,
    info            TEXT NOT NULL,
    waterCycle      VARCHAR(255) NOT NULL,
    waterInfo       VARCHAR(255) NOT NULL,
    waterExp        VARCHAR(255) NOT NULL,
    waterExpInfo    TEXT NOT NULL,
    light           VARCHAR(255) NOT NULL,
    lightInfo       VARCHAR(255) NOT NULL,
    lightExp        VARCHAR(255) NOT NULL,
    lightExpInfo    TEXT NOT NULL,
    humidity        VARCHAR(255) NOT NULL,
    humidInfo       VARCHAR(255) NOT NULL,
    humidExp        VARCHAR(255) NOT NULL,
    humidExpInfo    TEXT NOT NULL,
    tempExp         VARCHAR(255) NOT NULL,
    tempExpInfo     TEXT NOT NULL
    ) charset = utf8;

DROP TABLE IF EXISTS plantdisease;
CREATE TABLE plantdisease (
    diseaseId       VARCHAR(3),
    diseaseName     VARCHAR(30),
    englishName     VARCHAR(30),
    symptom         TEXT,
    environment     TEXT,
    precaution      TEXT,
    PRIMARY KEY(diseaseId)
    ) charset = utf8;