-- create language table
CREATE TABLE `yourdb`.`language` 
(
    `id_language` VARCHAR(10) NOT NULL  
    PRIMARY KEY (`id_language`(10))
) 
ENGINE = InnoDB; 

-- create categ_2
CREATE TABLE `yourdb`.`categ_2` 
(
    `id_categ_2` VARCHAR(20) NOT NULL ,
    PRIMARY KEY (`id_categ_2`(20))
) 
ENGINE = InnoDB; 

-- create categ_1
CREATE TABLE `yourdb`.`categ_1` 
(
    `id_categ_1` VARCHAR(20) NOT NULL , 
    `id_categ_2` VARCHAR(20) NOT NULL , 
    PRIMARY KEY (`id_categ_1`(20))
) 
ENGINE = InnoDB; 

-- create channels
CREATE TABLE `yourdb`.`channels` 
(
    `id_channel` VARCHAR(30) NOT NULL , 
    `name` VARCHAR(100) NOT NULL , 
    `interest` FLOAT NULL , 
    `date` DATETIME NOT NULL , 
    `id_categ_1` VARCHAR(20) NOT NULL , 
    `id_language` VARCHAR(2) NOT NULL , 
    PRIMARY KEY (`id_channel`(30))
) 
ENGINE = InnoDB; 


-- create videos
CREATE TABLE `yourdb`.`videos` 
(
    `id_video` VARCHAR(30) NOT NULL ,
    `title` VARCHAR(300) NOT NULL ,
    `author` VARCHAR(100) NOT NULL ,
    `published` DATETIME NOT NULL ,
    `stars` FLOAT NOT NULL ,
    `views` INT NOT NULL ,
    `id_channel` VARCHAR(30) NOT NULL ,
    PRIMARY KEY (`id_video`(30))
) 
ENGINE = InnoDB; 