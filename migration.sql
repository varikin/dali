#PostgreSQL format
ALTER TABLE "gallery_gallery" ADD COLUMN "order" smallint CHECK ("order" >= 0) NULL;
ALTER TABLE "gallery_gallery" ADD COLUMN "parent_gallery_id" integer NULL;
CREATE INDEX "gallery_gallery_parent_gallery_id" ON "gallery_gallery" ("parent_gallery_id");
UPDATE "gallery_gallery" SET "parent_gallery_id" = "parentGallery_id";
ALTER TABLE "gallery_gallery" ADD CONSTRAINT parent_gallery_id_refs_id_20dee1b9 FOREIGN KEY ("parent_gallery_id") REFERENCES "gallery_gallery" ("id") DEFERRABLE INITIALLY DEFERRED; 
DROP INDEX "gallery_gallery_parentGallery_id";
ALTER TABLE "gallery_gallery" DROP COLUMN "parentGallery_id";
