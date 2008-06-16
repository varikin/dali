BEGIN;
CREATE TABLE "blag_post" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(200) NOT NULL,
    "content" text NOT NULL,
    "author" varchar(200) NOT NULL,
    "created" datetime NOT NULL,
    "modified" datetime NOT NULL
)
;
CREATE TABLE "blag_media" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "folder_id" integer NOT NULL
)
;
CREATE TABLE "blag_image" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "webName" varchar(200) NOT NULL UNIQUE,
    "original_id" integer NOT NULL REFERENCES "blag_media" ("id"),
    "viewable_id" integer NOT NULL REFERENCES "blag_media" ("id"),
    "thumbnail_id" integer NOT NULL REFERENCES "blag_media" ("id"),
    "description" text NOT NULL,
    "gallery_id" integer NOT NULL,
    "order" smallint unsigned NOT NULL
)
;
CREATE TABLE "blag_linklist" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL
)
;
CREATE TABLE "blag_tag" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL
)
;
CREATE TABLE "blag_link" (
    "id" integer NOT NULL PRIMARY KEY,
    "url" varchar(200) NOT NULL,
    "text" varchar(200) NOT NULL
)
;
CREATE TABLE "blag_folder" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "path" varchar(200) NOT NULL,
    "parent_folder" integer NULL,
    "webEnabled" bool NOT NULL
)
;
CREATE TABLE "blag_gallery" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(200) NOT NULL,
    "webName" varchar(200) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "parentGallery_id" integer NULL
)
;
CREATE TABLE "blag_post_tags" (
    "id" integer NOT NULL PRIMARY KEY,
    "post_id" integer NOT NULL REFERENCES "blag_post" ("id"),
    "tag_id" integer NOT NULL REFERENCES "blag_tag" ("id"),
    UNIQUE ("post_id", "tag_id")
)
;
CREATE TABLE "blag_linklist_links" (
    "id" integer NOT NULL PRIMARY KEY,
    "linklist_id" integer NOT NULL REFERENCES "blag_linklist" ("id"),
    "link_id" integer NOT NULL REFERENCES "blag_link" ("id"),
    UNIQUE ("linklist_id", "link_id")
)
;
CREATE INDEX "blag_media_folder_id" ON "blag_media" ("folder_id");
CREATE INDEX "blag_image_original_id" ON "blag_image" ("original_id");
CREATE INDEX "blag_image_viewable_id" ON "blag_image" ("viewable_id");
CREATE INDEX "blag_image_thumbnail_id" ON "blag_image" ("thumbnail_id");
CREATE INDEX "blag_image_gallery_id" ON "blag_image" ("gallery_id");
CREATE INDEX "blag_folder_parent_folder" ON "blag_folder" ("parent_folder");
CREATE INDEX "blag_gallery_parentGallery_id" ON "blag_gallery" ("parentGallery_id");
COMMIT;
