CREATE SCHEMA `bbs` ;
use bbs;

CREATE TABLE `bbs`.`collections` (
  `star_id` INT NOT NULL,
  `usr_id` INT NULL,
  `post_id` INT NULL,
  PRIMARY KEY (`star_id`));

  CREATE TABLE `bbs`.`likes` (
  `id` INT NOT NULL,
  `usr_id` INT NULL,
  `post_id` INT NULL,
  `opinion` INT NULL,
  PRIMARY KEY (`id`));
  
  CREATE TABLE `bbs`.`posts_info` (
  `post_id` INT NOT NULL,
  `usr_id` INT NULL,
  `next_id` INT NULL,
  `state` INT NULL,
  `topic` VARCHAR(1000) NULL,
  `content` VARCHAR(1000) NULL,
  `comment_id` INT NULL,
  `type` INT NULL,
  `date` DATETIME(6) NULL,
  `comment_num` INT NULL,
  `total_comment_num` INT NULL,
  PRIMARY KEY (`post_id`));

CREATE TABLE `bbs`.`register_info` (
  `reg_id` INT NOT NULL,
  `reg_name` VARCHAR(45) NULL,
  `post_history_id` INT NULL,
  `usr_pswd` VARCHAR(200) NULL,
  `date` DATETIME(6) NULL,
  `usr_gender` VARCHAR(45) NULL,
  `usr_email` VARCHAR(45) NULL,
  `usr_phone_num` BIGINT(16) NULL,
  `usr_age` INT NULL,
  `usr_school` VARCHAR(45) NULL,
  `usr_photo_location` VARCHAR(45) NULL,
  `usr_nickname` VARCHAR(45) NULL,
  PRIMARY KEY (`reg_id`));
  
CREATE TABLE `bbs`.`kinds` (
  `kind_id` INT NOT NULL,
  `kind_name` VARCHAR(45) NULL,
  PRIMARY KEY (`kind_id`));

insert into kinds values (1, '信息科学技术学院');
insert into kinds values (2, '三角地');
insert into kinds values (3, '跳蚤市场');
insert into kinds values (4, '燕园食宿');
insert into kinds values (5, '流浪猫关爱协会');
