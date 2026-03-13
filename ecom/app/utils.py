import os
from django.conf import settings

def load_nutrition_data():
    """Read the `product.text` file and return nutrition info keyed by product name.

    The file lives under the ecom application directory and each line follows
    one of the two formats used by the author:

        Pizza,266:11:33:10
        Burger,295:17:30:12
        ...
        Banana,210,5,20,16   # commas instead of colons

    We normalise separators and ignore empty/malformed lines.  Names are
    stored lowercase so lookups can be case insensitive.
    """

    nutrition_dict = {}
    # `BASE_DIR` points at the Django project root (same directory as manage.py)
    # product.text is stored right alongside manage.py.
    file_path = os.path.join(settings.BASE_DIR, "product.text")

    if not os.path.exists(file_path):
        return nutrition_dict  # simply return empty dict if file is missing

    with open(file_path, "r") as file:
        for row in file:
            row = row.strip()
            if not row:
                continue

            # split off the product name from the rest of the values
            parts = row.split(",", 1)
            if len(parts) != 2:
                # malformed line
                continue

            product, values = parts
            # normalise any commas within the values to colons so we can split
            values = values.replace(",", ":")
            fields = values.split(":")
            if len(fields) < 4:
                continue

            kcal, protein, carbs, fat = fields[:4]
            try:
                nutrition_dict[product.lower()] = {
                    "calories": int(kcal),
                    "protein": int(protein),
                    "carbs": int(carbs),
                    "fat": int(fat),
                }
            except ValueError:
                # skip lines with non-integer values
                continue

    return nutrition_dict