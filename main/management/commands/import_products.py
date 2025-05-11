# main/management/commands/import_products.py

from django.core.management.base import BaseCommand
import pandas as pd
from main.models import ProductCategory, ProductOption

class Command(BaseCommand):
    help = 'ייבוא מוצרים מקובץ Excel'

    def handle(self, *args, **kwargs):
        file_path = 'media/import/products.xlsx'  # איפה ששמרנו את האקסל

        df = pd.read_excel(file_path)

        for column in df.columns:
            category, created = ProductCategory.objects.get_or_create(name=column)
            for value in df[column].dropna():
                ProductOption.objects.get_or_create(category=category, name=value)

        self.stdout.write(self.style.SUCCESS('✅ המוצרים יובאו בהצלחה!'))
