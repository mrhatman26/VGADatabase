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

/*Link Tables*/
DROP TABLE IF EXISTS link_developer_user;
CREATE TABLE link_developer_user(
    developer_id INT NOT NULL,
    user_id INT NOT NULL,
    developer_link_created BOOLEAN NOT NULL,
    developer_cDate TEXT,
    developer_link_approved BOOLEAN NOT NULL,
    developer_aDate TEXT,
    PRIMARY KEY(developer_id),
    FOREIGN KEY(developer_id) REFERENCES table_developers(developer_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_platform_user;
CREATE TABLE link_platform_user(
    platform_id INT NOT NULL,
    user_id INT NOT NULL,
    platform_link_created BOOLEAN NOT NULL,
    platform_cDate TEXT,
    platform_link_approved BOOLEAN NOT NULL,
    platform_aDate TEXT,
    PRIMARY KEY(platform_id),
    FOREIGN KEY(platform_id) REFERENCES table_platforms(platform_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_tags_aliases;
CREATE TABLE link_tags_aliases(
    tag_id INT NOT NULL,
    alias_id INT NOT NULL,
    user_id INT NOT NULL,
    link_date TEXT,
    PRIMARY KEY(tag_id),
    FOREIGN KEY(tag_id) REFERENCES table_tags(tag_id),
    FOREIGN KEY(alias_id) REFERENCES table_aliases(alias_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_developer;
CREATE TABLE link_game_developer(
    developer_id INT NOT NULL,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    developer_link_created BOOLEAN NOT NULL,
    developer_cDate TEXT,
    developer_link_approved BOOLEAN NOT NULL,
    developer_aDate TEXT,
    PRIMARY KEY(developer_id),
    FOREIGN KEY(developer_id) REFERENCES table_developers(developer_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_platform;
CREATE TABLE link_game_platform(
    platform_id INT NOT NULL,
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    platform_link_created BOOLEAN NOT NULL,
    platform_cDate TEXT,
    platform_link_approved BOOLEAN NOT NULL,
    platform_aDate TEXT,
    PRIMARY KEY(platform_id),
    FOREIGN KEY(platform_id) REFERENCES table_platforms(platform_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_tag;
CREATE TABLE link_game_tag(
    game_id INT NOT NULL,
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    tag_link_created BOOLEAN NOT NULL,
    tag_cDate TEXT,
    tag_link_approved BOOLEAN NOT NULL,
    tag_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(tag_id) REFERENCES table_tags(tag_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_tag_user;
CREATE TABLE link_tag_user(
    tag_id INT NOT NULL,
    user_id INT NOT NULL,
    tag_link_created BOOLEAN NOT NULL,
    tag_cDate TEXT,
    tag_link_approved BOOLEAN NOT NULL,
    tag_aDate TEXT,
    PRIMARY KEY(tag_id),
    FOREIGN KEY(tag_id) REFERENCES table_tags(tag_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_alias_user;
CREATE TABLE link_alias_user(
    alias_id INT NOT NULL,
    user_id INT NOT NULL,
    alias_link_created BOOLEAN NOT NULL,
    alias_cDate TEXT,
    alias_link_approved BOOLEAN NOT NULL,
    alias_aDate TEXT,
    PRIMARY KEY(alias_id),
    FOREIGN KEY(alias_id) REFERENCES table_aliases(alias_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_games;
CREATE TABLE link_games(
    parent_game_id INT NOT NULL,
    child_game_id INT NOT NULL,
    user_id INT NOT NULL,
    game_isSequel BOOLEAN NOT NULL,
    game_isDLC BOOLEAN NOT NULL,
    game_link_created BOOLEAN NOT NULL,
    game_cDate TEXT,
    game_link_approved BOOLEAN NOT NULL,
    game_aDate TEXT,
    PRIMARY KEY(parent_game_id),
    FOREIGN KEY(parent_game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(child_game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_user;
CREATE TABLE link_game_user(
    game_id INT NOT NULL,
    user_id INT NOT NULL,
    fave_datetime TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_age_rating;
CREATE TABLE link_game_age_rating(
    game_id INT NOT NULL,
    age_id INT NOT NULL,
    user_id INT NOT NULL,
    age_link_created BOOLEAN NOT NULL,
    age_cDate TEXT,
    age_link_approved BOOLEAN NOT NULL,
    age_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(age_id) REFERENCES table_age_ratings(age_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_language;
CREATE TABLE link_game_language(
    game_id INT NOT NULL,
    lang_id INT NOT NULL,
    user_id INT NOT NULL,
    lang_link_created BOOLEAN NOT NULL,
    lang_cDate TEXT,
    lang_link_approved BOOLEAN NOT NULL,
    lang_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(lang_id) REFERENCES table_languages(lang_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_character;
CREATE TABLE link_game_character(
    game_id INT NOT NULL,
    char_id INT NOT NULL,
    user_id INT NOT NULL,
    char_link_created BOOLEAN NOT NULL,
    char_cDate TEXT,
    char_link_approved BOOLEAN NOT NULL,
    char_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(char_id) REFERENCES table_characters(char_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_screenshot;
CREATE TABLE link_game_screenshot(
    game_id INT NOT NULL,
    sshot_id INT NOT NULL,
    user_id INT NOT NULL,
    sshot_link_created BOOLEAN NOT NULL,
    sshot_cDate TEXT,
    sshot_link_approved BOOLEAN NOT NULL,
    sshot_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(sshot_id) REFERENCES table_screenshots(sshot_id)
);

DROP TABLE IF EXISTS link_game_rating;
CREATE TABLE link_game_rating(
    game_id INT NOT NULL,
    rating_id INT NOT NULL,
    user_id INT NOT NULL,
    rating_link_created BOOLEAN NOT NULL,
    rating_cDate TEXT,
    rating_link_approved BOOLEAN NOT NULL,
    rating_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(rating_id) REFERENCES table_ratings(rating_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_game_genre;
CREATE TABLE link_game_genre(
    game_id INT NOT NULL,
    genre_id INT NOT NULL,
    user_id INT NOT NULL,
    genre_link_create BOOLEAN NOT NULL,
    genre_cDate TEXT,
    genre_link_approved BOOLEAN NOT NULL,
    genre_aDate TEXT,
    PRIMARY KEY(game_id),
    FOREIGN KEY(game_id) REFERENCES table_games(game_id),
    FOREIGN KEY(genre_id) REFERENCES table_genres(genre_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_genre_user;
CREATE TABLE link_genre_user(
    genre_id INT NOT NULL,
    user_id INT NOT NULL,
    genre_link_created BOOLEAN NOT NULL,
    genre_cDate TEXT,
    genre_link_approved BOOLEAN NOT NULL,
    genre_aDate TEXT,
    PRIMARY KEY(genre_id),
    FOREIGN KEY(genre_id) REFERENCES table_genres(genre_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_age_user;
CREATE TABLE link_age_user(
    age_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(age_id),
    FOREIGN KEY(age_id) REFERENCES table_age_ratings(age_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_lang_user;
CREATE TABLE link_lang_user(
    lang_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(lang_id),
    FOREIGN KEY(lang_id) REFERENCES table_languages(lang_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);

DROP TABLE IF EXISTS link_character_user;
CREATE TABLE link_character_user(
    char_id INT NOT NULL,
    user_id INT NOT NULL,
    char_link_created BOOLEAN NOT NULL,
    char_cDate TEXT,
    char_link_approved BOOLEAN NOT NULL,
    char_aDate TEXT,
    PRIMARY KEY(char_id),
    FOREIGN KEY(char_id) REFERENCES table_characters(char_id),
    FOREIGN KEY(user_id) REFERENCES table_users(user_id)
);