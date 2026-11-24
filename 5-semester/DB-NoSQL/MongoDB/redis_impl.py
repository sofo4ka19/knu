import redis
import json

# ===================== НАЛАШТУВАННЯ REDIS =====================
REDIS_HOST = "localhost"
REDIS_PORT = 6379

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True  # Автоматичне декодування
)


# ===================== 1. КЕШУВАННЯ ЦІН =====================
def cache_prices():
    """Базове кешування цін продуктів у Redis"""
    products = [
        {"id": 101, "price": 499},
        {"id": 205, "price": 1299},
        {"id": 310, "price": 850},
    ]

    for product in products:
        redis_client.setex(f"price:{product['id']}", 3600, product['price'])

    # Перевірка
    return {p['id']: redis_client.get(f"price:{p['id']}") for p in products}


# ===================== 2. КОШИК =====================
def demo_cart():
    """Базові операції з кошиком"""
    cart_key = "cart:1001"
    redis_client.delete(cart_key)

    # Додавання товарів
    redis_client.hset(cart_key, "101", 2)
    redis_client.hset(cart_key, "205", 1)

    # Збільшення кількості
    redis_client.hincrby(cart_key, "101", 1)

    # Отримання всього кошика
    return redis_client.hgetall(cart_key)


# ===================== 3. ЛІЧИЛЬНИКИ =====================
def demo_counters():
    """Лічильники переглядів та продажів"""
    redis_client.incr("views:101")
    redis_client.incrby("sales:101", 5)

    return {
        "views": redis_client.get("views:101"),
        "sales": redis_client.get("sales:101")
    }


# ===================== 4. ТОП-ПРОДУКТИ =====================
def demo_top_products():
    """Базовий топ продуктів через Sorted Set"""
    top_key = "popular:products"
    redis_client.delete(top_key)

    redis_client.zadd(top_key, {"iPhone": 1500, "Ноутбук": 1200})

    # Топ-2
    return redis_client.zrevrange(top_key, 0, 1, withscores=True)


# ===================== 5. СЕСІЇ =====================
def demo_sessions():
    """Базові сесії користувачів"""
    session_data = {"user_id": 1001, "cart_items": 2}
    redis_client.setex("sess:abc123", 1800, json.dumps(session_data))

    return json.loads(redis_client.get("sess:abc123"))


# ===================== 6. ОСТАННІ ПЕРЕГЛЯДИ =====================
def demo_recent_views():
    """Список останніх переглядів користувача"""
    key = "recent:1001"
    redis_client.delete(key)

    redis_client.lpush(key, "Ноутбук", "iPhone")
    return redis_client.lrange(key, 0, 1)


# ===================== 7. АКЦІЇ =====================
def demo_promotions():
    """Базові набори продуктів у акціях"""
    black_friday_key = "promo:black_friday"
    redis_client.delete(black_friday_key)

    redis_client.sadd(black_friday_key, "101", "205")
    return redis_client.smembers(black_friday_key)


# ===================== MAIN =====================
if __name__ == "__main__":
    print("✅ Redis підключено\n")

    print("Кеш цін:", cache_prices())
    print("Кошик:", demo_cart())
    print("Лічильники:", demo_counters())
    print("Топ продукти:", demo_top_products())
    print("Сесія:", demo_sessions())
    print("Останні перегляди:", demo_recent_views())
    print("Акції:", demo_promotions())


