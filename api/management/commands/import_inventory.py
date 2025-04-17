import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Inventory, Supplier, Warehouse

class Command(BaseCommand):
    help = 'Import inventory data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['excel_file']
        df = pd.read_excel(file_path)

        for _, row in df.iterrows():
            try:
                supplier = Supplier.objects.get(pk=row['Supplier_ID'])
                warehouse = Warehouse.objects.get(pk=row['Location_ID'])

                Inventory.objects.update_or_create(
                    Item_ID=row['Item_ID'],
                    defaults={
                        'Name': row['Name'],
                        'Category': row['Category'],
                        'Quantity': row['Quantity'],
                        'Location_ID': warehouse,
                        'Supplier_ID': supplier,
                        'Restock_Level': row.get('Restock_Level', 10)  # 如果你有这个字段
                    }
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to import row {row['Item_ID']}: {e}"))
        
        self.stdout.write(self.style.SUCCESS('Inventory data imported successfully!'))
