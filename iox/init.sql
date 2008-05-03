BEGIN;
CREATE TABLE "music_playlist" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL
)
;
CREATE TABLE "music_song" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "artist" varchar(200) NOT NULL,
    "album" varchar(200) NOT NULL,
    "play_count" integer unsigned NULL,
    "last_played" datetime NULL,
    "rating" integer unsigned NULL,
    "filename" varchar(100) NULL
)
;
CREATE TABLE "music_playlist_songs" (
    "id" integer NOT NULL PRIMARY KEY,
    "playlist_id" integer NOT NULL REFERENCES "music_playlist" ("id"),
    "song_id" integer NOT NULL REFERENCES "music_song" ("id"),
    UNIQUE ("playlist_id", "song_id")
)
;
CREATE TABLE "music_song_songs_played_after" (
    "id" integer NOT NULL PRIMARY KEY,
    "from_song_id" integer NOT NULL REFERENCES "music_song" ("id"),
    "to_song_id" integer NOT NULL REFERENCES "music_song" ("id"),
    UNIQUE ("from_song_id", "to_song_id")
)
;
COMMIT;
