import json
from django.core.files import File
from .models import Category, Product

def import_data_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        category_name = item.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        product = Product(
            name=item.get('name'),
            description=item.get('description'),
            price=item.get('price'),
            category=category
        )

        # Handle image import
        image_path = item.get('image')
        if image_path:
            with open(image_path, 'rb') as img_file:
                product.image.save(image_path.split('/')[-1], File(img_file))

        product.save()

if __name__ == '__main__':
    import_data_from_json(r'F:\Python_Trainings\Batch1\Django\ecom\static\dataset\elec_product_output.json')