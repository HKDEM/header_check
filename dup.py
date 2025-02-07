def calculate_area_rectangle(length, width):
    """Dikdörtgenin alanını hesaplar."""
    return length * width
def calculate_area_rectangle_duplicate(length, width):
    """Tekrar eden kod: Dikdörtgenin alanını hesaplar."""
    return length * width
def calculate_area_circle(radius):
    """Dairenin alanını hesaplar."""
    return 3.14 * radius * radius
def calculate_area_circle_duplicate(radius):
    """Tekrar eden kod: Dairenin alanını hesaplar."""
    return 3.14 * radius * radius
def print_message(message):
    """Mesajı ekrana yazdırır."""
    print(message)
def print_message_duplicate(message):
    """Tekrar eden kod: Mesajı ekrana yazdırır."""
    print(message)
# Örnek kullanım
length = 10
width = 5
radius = 7
area_rectangle = calculate_area_rectangle(length, width)
area_rectangle_duplicate = calculate_area_rectangle_duplicate(length, width)
area_circle = calculate_area_circle(radius)
area_circle_duplicate = calculate_area_circle_duplicate(radius)
print_message("Dikdörtgen Alanı:", area_rectangle)
print_message_duplicate("Tekrar Eden Dikdörtgen Alanı:", area_rectangle_duplicate)
print_message("Daire Alanı:", area_circle)
print_message_duplicate("Tekrar Eden Daire Alanı:", area_circle_duplicate)
