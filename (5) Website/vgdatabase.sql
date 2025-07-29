DROP DATABASE IF EXISTS vgadatabase;
CREATE DATABASE vgadatabase;
USE vgadatabase;

/*Regular Tables*/
/*Describes the games themselves*/
DROP TABLE IF EXISTS table_games;
CREATE TABLE table_games(
    game_id INT NOT NULL AUTO_INCREMENT,
    game_title TEXT NOT NULL,
    game_aka TEXT,
    game_desc TEXT,
    game_rdate TEXT,
    game_rstate TEXT, /*Describes the game's release state. E.G: Early Access*/
    game_url TEXT,
    PRIMARY KEY(game_id)
);

/*Describes the developers who make the games. Or the publishers*/
DROP TABLE IF EXISTS table_developers;
CREATE TABLE table_developers(
    developer_id INT NOT NULL AUTO_INCREMENT,
    developer_name TEXT NOT NULL,
    developer_desc TEXT,
    developer_foundDate TEXT,
    developer_status TEXT,
    developer_defunctDate TEXT,
    developer_isPub BOOLEAN DEFAULT 0,
    PRIMARY KEY(developer_id)
);

DROP TABLE IF EXISTS table_platforms;
CREATE TABLE table_platforms(
    platform_id INT NOT NULL AUTO_INCREMENT,
    platform_name TEXT NOT NULL,
    platform_desc TEXT,
    platform_rDate TEXT,
    platform_specs TEXT,
    platform_generation INT,
    PRIMARY KEY(platform_id)
);

DROP TABLE IF EXISTS table_tags;
CREATE TABLE table_tags(
    tag_id INT NOT NULL AUTO_INCREMENT,
    tag_name TEXT NOT NULL,
    tag_desc TEXT,
    tag_type TEXT,
    tag_isNSFW BOOLEAN DEFAULT 0,
    PRIMARY KEY(tag_id)
);

DROP TABLE IF EXISTS table_aliases;
CREATE TABLE table_aliases(
    alias_id INT NOT NULL AUTO_INCREMENT,
    alias_name TEXT NOT NULL,
    PRIMARY KEY(alias_id)
);

DROP TABLE IF EXISTS table_users;
CREATE TABLE table_users(
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name TEXT NOT NULL,
    user_pass TEXT NOT NULL,
    user_email TEXT,
    user_desc TEXT,
    user_pfp TEXT,
    user_isAdmin BOOLEAN DEFAULT 0,
    user_isMod BOOLEAN DEFAULT 0,
    PRIMARY KEY(user_id)
);

DROP TABLE IF EXISTS table_age_ratings;
CREATE TABLE table_age_ratings(
    age_id INT NOT NULL AUTO_INCREMENT,
    age_name TEXT NOT NULL,
    age_origin TEXT NOT NULL,
    PRIMARY KEY(age_id)
);

DROP TABLE IF EXISTS table_languages;
CREATE TABLE table_languages(
    lang_id INT NOT NULL AUTO_INCREMENT,
    lang_name TEXT NOT NULL,
    lang_icon_url TEXT,
    PRIMARY KEY(lang_id)
);

DROP TABLE IF EXISTS table_characters;
CREATE TABLE table_characters(
    char_id INT NOT NULL AUTO_INCREMENT,
    char_name TEXT NOT NULL,
    char_desc TEXT,
    char_type TEXT, /*Describes the species of the character. If left null, it will default to human.*/
    char_gender TEXT, /*The contraversial one.*/
    char_age INT,
    char_playable BOOLEAN DEFAULT 0,
    PRIMARY KEY(char_id)
);

DROP TABLE IF EXISTS table_screenshots;
CREATE TABLE table_screenshots(
    sshot_id INT NOT NULL AUTO_INCREMENT,
    sshot_isCover BOOLEAN DEFAULT 0, /*Determines where the image will be shown. THERE CAN ONLY BE ONE COVER!!!!*/
    sshot_url TEXT,
    PRIMARY KEY(sshot_id)
);

DROP TABLE IF EXISTS table_ratings;
CREATE TABLE table_ratings(
    rating_id INT NOT NULL AUTO_INCREMENT,
    rating_value INT NOT NULL, /*Can only be -1 to 1*/
    rating_desc TEXT,
    PRIMARY KEY(rating_id)
);

DROP TABLE IF EXISTS table_update_history;
CREATE TABLE table_update_history(
    update_id INT NOT NULL AUTO_INCREMENT,
    update_version INT NOT NULL DEFAULT 1,
    update_name TEXT NOT NULL,
    update_type TEXT NOT NULL,
    update_added TEXT,
    update_removed TEXT,
    PRIMARY KEY(update_id)
);

/*Link Tables*/
DROP TABLE IF EXISTS link_developer_user;
CREATE TABLE link_developer_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    developer_id INT NOT NULL,
    user_id INT NOT NULL,
    developer_cDate TEXT,
    developer_link_approved BOOLEAN DEFAULT 0,
    developer_aDate TEXT,
    developer_denied BOOLEAN DEFAULT 0,
    developer_dDate TEXT,
	developer_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(developer_id) REFERENCES table_developers(developer_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_platform_user;
CREATE TABLE link_platform_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    platform_id INT NOT NULL,
    user_id INT NOT NULL,
    platform_cDate TEXT,
    platform_link_approved BOOLEAN DEFAULT 0,
    platform_aDate TEXT,
    platform_denied BOOLEAN DEFAULT 0,
    platform_dDate TEXT,
	platform_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(platform_id) REFERENCES table_platforms(platform_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_tags_aliases;
CREATE TABLE link_tags_aliases(
    link_id INT NOT NULL AUTO_INCREMENT,
    tag_id INT NOT NULL,
    alias_id INT NOT NULL,
    user_id INT NOT NULL,
    tag_cDate TEXT,
    tag_link_approved BOOLEAN DEFAULT 0,
    tag_aDate TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(tag_id) REFERENCES table_tags(tag_id),
    FOREIGN KEY(alias_id) REFERENCES table_aliases(alias_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_developer;
CREATE TABLE link_game_developer(
    link_id INT NOT NULL AUTO_INCREMENT,
    developer_id INT NOT NULL,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    developer_cDate TEXT,
    developer_link_approved BOOLEAN DEFAULT 0,
    developer_aDate TEXT,
    developer_denied BOOLEAN DEFAULT 0,
    developer_dDate TEXT,
	developer_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(developer_id) REFERENCES table_developers(developer_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_platform;
CREATE TABLE link_game_platform(
    link_id INT NOT NULL AUTO_INCREMENT,
    platform_id INT NOT NULL,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    platform_cDate TEXT,
    platform_link_approved BOOLEAN DEFAULT 0,
    platform_aDate TEXT,
    platform_denied BOOLEAN DEFAULT 0,
    platform_dDate TEXT,
	platform_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(platform_id) REFERENCES table_platforms(platform_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_tag;
CREATE TABLE link_game_tag(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    tag_cDate TEXT,
    tag_link_approved BOOLEAN DEFAULT 0,
    tag_aDate TEXT,
    tag_denied BOOLEAN DEFAULT 0,
    tag_dDate TEXT,
	tag_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(tag_id) REFERENCES table_tags(tag_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_tag_user;
CREATE TABLE link_tag_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    tag_cDate TEXT,
    tag_link_approved BOOLEAN DEFAULT 0,
    tag_aDate TEXT,
    tag_denied BOOLEAN DEFAULT 0,
    tag_dDate TEXT,
	tag_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(tag_id) REFERENCES table_tags(tag_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_alias_user;
CREATE TABLE link_alias_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    alias_id INT NOT NULL,
    user_id INT NOT NULL,
    alias_cDate TEXT,
    alias_link_approved BOOLEAN DEFAULT 0,
    alias_aDate TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(alias_id) REFERENCES table_aliases(alias_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_games;
CREATE TABLE link_games(
    link_id INT NOT NULL AUTO_INCREMENT,
    parent_game_id INT NOT NULL,
    child_game_id INT NOT NULL,
    user_id INT NOT NULL,
    game_isSequel BOOLEAN DEFAULT 0,
    game_isDLC BOOLEAN DEFAULT 0,
    game_cDate TEXT,
    game_link_approved BOOLEAN DEFAULT 0,
    game_aDate TEXT,
    game_denied BOOLEAN DEFAULT 0,
    game_dDate TEXT,
	game_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(parent_game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(child_game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_user;
CREATE TABLE link_game_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    game_cDate TEXT,
    game_link_approved BOOLEAN DEFAULT 0,
    game_aDate TEXT,
    game_denied BOOLEAN DEFAULT 0,
    game_dDate TEXT,
	game_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_favourite;
CREATE TABLE link_game_favourite(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    fave_datetime TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_age_rating;
CREATE TABLE link_game_age_rating(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    age_id INT NOT NULL,
    user_id INT NOT NULL,
    age_cDate TEXT,
    age_link_approved BOOLEAN DEFAULT 0,
    age_aDate TEXT,
    age_denied BOOLEAN DEFAULT 0,
    age_dDate TEXT,
	age_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(age_id) REFERENCES table_age_ratings(age_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_language;
CREATE TABLE link_game_language(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    lang_id INT NOT NULL,
    user_id INT NOT NULL,
    lang_cDate TEXT,
    lang_link_approved BOOLEAN DEFAULT 0,
    lang_aDate TEXT,
    lang_denied BOOLEAN DEFAULT 0,
    lang_dDate TEXT,
	lang_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(lang_id) REFERENCES table_languages(lang_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_character;
CREATE TABLE link_game_character(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    char_id INT NOT NULL,
    user_id INT NOT NULL,
    char_cDate TEXT,
    char_link_approved BOOLEAN DEFAULT 0,
    char_aDate TEXT,
    char_denied BOOLEAN DEFAULT 0,
    char_dDate TEXT,
	char_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(char_id) REFERENCES table_characters(char_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_screenshot;
CREATE TABLE link_game_screenshot(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    sshot_id INT NOT NULL,
    user_id INT NOT NULL,
    sshot_cDate TEXT,
    sshot_link_approved BOOLEAN DEFAULT 0,
    sshot_aDate TEXT,
    sshot_denied BOOLEAN DEFAULT 0,
    sshot_dDate TEXT,
	sshot_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(sshot_id) REFERENCES table_screenshots(sshot_id)
);

DROP TABLE IF EXISTS link_game_rating;
CREATE TABLE link_game_rating(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    rating_id INT NOT NULL,
    user_id INT NOT NULL,
    rating_cDate TEXT,
    rating_link_approved BOOLEAN DEFAULT 0,
    rating_aDate TEXT,
    rating_denied BOOLEAN DEFAULT 0,
    rating_dDate TEXT,
	rating_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(rating_id) REFERENCES table_ratings(rating_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_age_user;
CREATE TABLE link_age_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    age_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(link_id),
    FOREIGN KEY(age_id) REFERENCES table_age_ratings(age_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_lang_user;
CREATE TABLE link_lang_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    lang_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(link_id),
    FOREIGN KEY(lang_id) REFERENCES table_languages(lang_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_character_user;
CREATE TABLE link_character_user(
    link_id INT NOT NULL AUTO_INCREMENT,
    char_id INT NOT NULL,
    user_id INT NOT NULL,
    char_cDate TEXT,
    char_link_approved BOOLEAN DEFAULT 0,
    char_aDate TEXT,
    char_denied BOOLEAN DEFAULT 0,
    char_dDate TEXT,
	char_dDes TEXT,
    PRIMARY KEY(link_id),
    FOREIGN KEY(char_id) REFERENCES table_characters(char_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_update;
CREATE TABLE link_game_update(
    link_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    update_id INT NOT NULL,
    user_id INT NOT NULL,
    update_cDate TEXT NOT NULL,
    PRIMARY KEY(link_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(update_id) REFERENCES table_update_history(update_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);