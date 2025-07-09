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

/*Link Tables*/

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