DROP DATABASE IF EXISTS vgadatabase;
CREATE DATABASE vgadatabase;
USE vgadatabase;

/*Regular Tables*/
/*Describes the games themselves*/
DROP TABLE IF EXISTS table_games;
CREATE TABLE table_games(
    game_id INT NOT NULL,
    game_title TEXT NOT NULL,
    game_aka TEXT,
    game_desc TEXT,
    game_rdate TEXT,
    game_rstate TEXT, /*Describes the game's release state. E.G: Early Access*/
    PRIMARY KEY(game_id)
);

/*Describes the developers who make the games. Or the publishers*/
DROP TABLE IF EXISTS table_developers;
CREATE TABLE table_developers(
    developer_id INT NOT NULL,
    developer_name TEXT NOT NULL,
    developer_desc TEXT,
    developer_foundDate TEXT,
    developer_status TEXT,
    developer_defunctDate TEXT,
    developer_isPub BOOLEAN NOT NULL,
    PRIMARY KEY(developer_id)
);

DROP TABLE IF EXISTS table_platforms;
CREATE TABLE table_platforms(
    platform_id INT NOT NULL,
    platform_name TEXT NOT NULL,
    platform_desc TEXT,
    platform_rDate TEXT,
    platform_specs TEXT,
    platform_generation INT,
    PRIMARY KEY(platform_id)
);

DROP TABLE IF EXISTS table_tags;
CREATE TABLE table_tags(
    tag_id INT NOT NULL,
    tag_name TEXT NOT NULL,
    tag_desc TEXT,
    tag_type TEXT,
    tag_isNSFW BOOLEAN NOT NULL,
    PRIMARY KEY(tag_id)
);

DROP TABLE IF EXISTS table_aliases;
CREATE TABLE table_aliases(
    alias_id INT NOT NULL,
    alias_name TEXT NOT NULL,
    PRIMARY KEY(alias_id)
);

DROP TABLE IF EXISTS table_users;
CREATE TABLE table_users(
    user_id INT NOT NULL,
    user_name TEXT NOT NULL,
    user_pass TEXT NOT NULL,
    user_email TEXT,
    user_desc TEXT,
    user_pfp TEXT,
    user_isAdmin BOOLEAN NOT NULL,
    user_isMod BOOLEAN NOT NULL,
    PRIMARY KEY(user_id)
);

DROP TABLE IF EXISTS table_genres;
CREATE TABLE table_genres(
    genre_id INT NOT NULL,
    genre_name TEXT NOT NULL,
    genre_desc TEXT,
    genre_isNSFW BOOLEAN NOT NULL,
    PRIMARY KEY(genre_id)
);

DROP TABLE IF EXISTS table_age_ratings;
CREATE TABLE table_age_ratings(
    age_id INT NOT NULL,
    age_name TEXT NOT NULL,
    age_origin TEXT NOT NULL,
    PRIMARY KEY(age_id)
);

DROP TABLE IF EXISTS table_languages;
CREATE TABLE table_languages(
    lang_id INT NOT NULL,
    lang_name TEXT NOT NULL,
    lang_icon_url TEXT,
    PRIMARY KEY(lang_id)
);

DROP TABLE IF EXISTS table_characters;
CREATE TABLE table_characters(
    char_id INT NOT NULL,
    char_name TEXT NOT NULL,
    char_desc TEXT,
    char_type TEXT, /*Describes the species of the character. If left null, it will default to human.*/
    char_gender TEXT, /*The contraversial one.*/
    char_age INT,
    char_playable BOOLEAN NOT NULL,
    PRIMARY KEY(char_id)
);

DROP TABLE IF EXISTS table_screenshots;
CREATE TABLE table_screenshots(
    sshot_id INT NOT NULL,
    sshot_isCover BOOLEAN NOT NULL, /*Determines where the image will be shown. THERE CAN ONLY BE ONE COVER!!!!*/
    sshot_url TEXT,
    PRIMARY KEY(sshot_id)
);

DROP TABLE IF EXISTS table_ratings;
CREATE TABLE table_ratings(
    rating_id INT NOT NULL,
    rating_value INT NOT NULL, /*Can only be -1 to 1*/
    rating_desc TEXT,
    PRIMARY KEY(rating_id)
);

DROP TABLE IF EXISTS table_update_history;
CREATE TABLE table_update_history(
    update_id INT NOT NULL,
    update_desc TEXT,
    PRIMARY KEY(update_id)
);