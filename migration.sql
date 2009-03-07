ALTER TABLE "gallery_gallery" ADD COLUMN "order" smallint unsigned;
ALTER TABLE "gallery_gallery" ADD COLUMN "parent_gallery_id" integer;
CREATE INDEX "gallery_gallery_parent_gallery_id" ON "gallery_gallery" ("parent_gallery_id");
UPDATE "gallery_gallery" SET "parent_gallery_id" = "parentGallery_id";
DROP INDEX "gallery_gallery_parentGallery_id";
ALTER TABLE "gallery_gallery" DROP COLUMN "parentGallery_id";
