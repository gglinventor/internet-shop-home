from django.core.cache import cache


class CacheMixin:
    def set_get_cache(self, query, cache_name, cache_time):
        data = cache.get(cache_name)
        if data:
            return data[0], data[1]
        else:
            data = query
            all_price = {}
            for order in data:
                order_price = 0
                for item in order.orderitem_set.all():
                    order_price += item.price * item.quantity
                    all_price[order.id] = order_price
            cache.set(cache_name, [data, all_price], cache_time)
            return data, all_price