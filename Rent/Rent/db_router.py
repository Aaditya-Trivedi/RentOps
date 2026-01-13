class ShopDatabaseRouter:
    """
    Routes database operations for shop-related apps
    """

    shop_apps = {'inventory', 'rentals', 'notifications'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.shop_apps:
            return getattr(model, 'shop_db', None)
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.shop_apps:
            return getattr(model, 'shop_db', None)
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.shop_apps:
            return db != 'default'
        return db == 'default'
