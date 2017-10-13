=======
History
=======

0.1.0 (Unreleased)
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
