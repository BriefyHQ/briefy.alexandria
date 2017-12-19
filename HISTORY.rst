=======
History
=======

1.0.0 (2017-12-19)
------------------

    * Initial implementation (rudaporto).
    * Added models for Asset and Collection (rudaporto).
    * Added views for Asset and Collection (rudaporto).
    * Added all code to run pyramid application (rudaporto).
    * Added alembic support and first migration (rudaporto).
    * Added docker support (rudaporto).
    * Added tags ARRAY of strings to mixins.LibraryItemMixin and respective migration (rudaporto).
    * Review .travis and tox.ini configuration (rudaporto).
    * Improve many to many relationship between Asset and Collection models (rudaporto).
    * Config colanderalchemy attribute in Asset and Collection models (rudaporto).
    * Config to_dict attributes and customize to_dict for Asset and Collection (rudaporto).
    * Added customized create and update method for Asset and Collection to deal with relationship field (rudaporto).
    * Added customized validation for many to many relationship field to get instance from database from ID (rudaporto).
    * Define to_listing_dict attributes for Asset and Collection (rudaporto).
    * Customize Collection.to_listing_dict to return also the assets attribute (rudaporto).
    * Added custom comparator to filter the tags field using customized query (rudaporto).
    * Added to Assets view the option to filter the collections field (rudaporto).
    * Added to Collections view the option to filter the assets field (rudaporto).
    * Upgrade docker base container to version 1.4.5 (rudaporto).
    * Change to use gunicorn + gevent as default in all environments except test (rudaporto).
    * Fix asset source_path validation to only raise ValueError if we are not updating the current asset (rudaporto).
    * Fix: properties field not being persisted since colander needs JSONType to know how to handle mapping attributes (rudaporto).
