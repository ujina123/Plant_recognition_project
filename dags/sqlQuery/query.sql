-- JngMkk
CREATE TABLE weather (
    weatherID   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    areaNo      BIGINT NOT NULL,
    si          VARCHAR(30) NOT NULL,
    time        INT NOT NULL,
    condi       VARCHAR(30) NOT NULL,
    isDay       INT NULL,
    temp        INT NULL,
    humidity    INT NULL,
    rainRatio   INT NULL,
    snowRatio   INT NULL
);
