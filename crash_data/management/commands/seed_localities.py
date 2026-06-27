import os
import csv
from django.core.management.base import BaseCommand
from crash_data.models import LocalityReference

class Command(BaseCommand):
    help = 'Seeds database capturing all descriptive fields from CensusPlaceCode layout with Proper Title Case strings'

    def add_arguments(self, parser):
        # Requests the explicit file path as an argument
        parser.add_argument('file_path', type=str, help='Absolute file path to the national_places file (copied via Ctrl+Shift+C)')

    def handle(self, *args, **options):
        # Clean Windows path wrapping quotes out if present
        raw_path = options['file_path']
        txt_file_path = raw_path.strip().strip('"').strip("'")
        
        if not os.path.exists(txt_file_path):
            self.stdout.write(self.style.ERROR(f"File missing at calculated location: {txt_file_path}"))
            return

        # REMOVED: LocalityReference.objects.all().delete()
        self.stdout.write("Analyzing existing database records to prevent duplicate key crashes...")
        
        try:
            localities_to_create = []
            
            # Pre-populate your tracking set with jcodes already saved in PostgreSQL
            seen_jcodes = set(LocalityReference.objects.values_list('jcode', flat=True))
            initial_count = len(seen_jcodes)
            self.stdout.write(f"Found {initial_count} existing records. Appending new records from file...")

            with open(txt_file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                # Strip spaces from column keys
                reader.fieldnames = [str(h).strip() for h in reader.fieldnames] if reader.fieldnames else []

                for row in reader:
                    if not row:
                        continue
                        
                    # Clean up blank keys or trailing text gaps per item
                    row_dict = {str(k).strip(): str(v).strip() for k, v in row.items() if k}
                    
                    jcode = row_dict.get('CensusPlaceCode', '')
                    raw_st = row_dict.get('ST', '')
                    raw_st_name = row_dict.get('STName', '')
                    raw_county = row_dict.get('County', '')
                    raw_long_name = row_dict.get('PlaceNameLong', '')
                    raw_short_name = row_dict.get('PlaceNameShort', '')
                    raw_census_name = row_dict.get('CensusPlaceName', '')

                    # Skip broken rows or records that are already present in the database or loop
                    if not jcode:
                        continue
                    if jcode in seen_jcodes:
                        continue

                    localities_to_create.append(
                        LocalityReference(
                            jcode=jcode,
                            st=raw_st,
                            st_name=raw_st_name,
                            county=raw_county,
                            place_name_long=raw_long_name,
                            place_name_short=raw_short_name,
                            census_place_name=raw_census_name
                        )
                    )
                    # Add to the set so duplicate rows inside the file text itself are handled
                    seen_jcodes.add(jcode)

            if localities_to_create:
                total_records = len(localities_to_create)
                self.stdout.write(f"Bulk-uploading {total_records} new census records into PostgreSQL...")
                LocalityReference.objects.bulk_create(localities_to_create, batch_size=500)
                self.stdout.write(self.style.SUCCESS(f"Successfully appended database records without affecting pre-existing entries!"))
            else:
                self.stdout.write(self.style.WARNING("No new records found to populate. All entries inside file are already inside the database table."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Processing error context: {e}"))