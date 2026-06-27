import os
import csv
from django.core.management.base import BaseCommand
from crash_data.models import LocalityReference, LocalityPopulation

class Command(BaseCommand):
    help = 'Seeder that accepts a trailing file path argument to append or update annual population estimate figures as an array'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Absolute path to your population CSV file (copied via Ctrl+Shift+C)')

    def handle(self, *args, **options):
        raw_input_path = options['file_path']
        clean_file_path = raw_input_path.strip().strip('"').strip("'")

        if not os.path.exists(clean_file_path):
            self.stdout.write(self.style.ERROR(f"File not found! Verified targeted path: {clean_file_path}"))
            return

        self.stdout.write("Processing database updates...")

        try:
            populations_to_insert = []
            populations_to_update = []
            
            # Fetch all valid geographic keys to ensure data integrity
            valid_jcodes = set(LocalityReference.objects.values_list('jcode', flat=True))
            
            # Look up keys that already physically exist in the population table
            existing_pop_records = set(LocalityPopulation.objects.values_list('locality_id', flat=True))
            
            # Track duplicates within the CSV itself
            seen_in_file = set()

            with open(clean_file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=',')
                reader.fieldnames = [str(h).strip() for h in reader.fieldnames] if reader.fieldnames else []

                for row in reader:
                    if not row:
                        continue

                    row_dict = {str(k).strip(): str(v).strip() for k, v in row.items() if k}
                    jcode_target = row_dict.get('CensusPlaceCode', '')
                    
                    if not jcode_target or jcode_target not in valid_jcodes:
                        continue
                    
                    # Skip if we already processed this exact jcode earlier in this specific file
                    if jcode_target in seen_in_file:
                        continue

                    def parse_int(val):
                        if not val:
                            return 0
                        clean_val = val.replace(',', '').split('.')[0].strip()
                        return int(clean_val) if clean_val.isdigit() or (clean_val.startswith('-') and clean_val[1:].isdigit()) else 0

                    pop_array = [0] * 26
                    pop_array[20] = parse_int(row_dict.get('POPESTIMATE2020', '0'))
                    pop_array[21] = parse_int(row_dict.get('POPESTIMATE2021', '0'))
                    pop_array[22] = parse_int(row_dict.get('POPESTIMATE2022', '0'))
                    pop_array[23] = parse_int(row_dict.get('POPESTIMATE2023', '0'))
                    pop_array[24] = parse_int(row_dict.get('POPESTIMATE2024', '0'))
                    pop_array[25] = parse_int(row_dict.get('POPESTIMATE2025', '0'))

                    instance = LocalityPopulation(
                        locality_id=jcode_target,
                        population_estimates=pop_array
                    )

                    # Route rows dynamically based on current database state
                    if jcode_target in existing_pop_records:
                        populations_to_update.append(instance)
                    else:
                        populations_to_insert.append(instance)
                        
                    seen_in_file.add(jcode_target)

            # 1. Execute regular bulk insert for fresh entries
            if populations_to_insert:
                total_inserted = len(populations_to_insert)
                self.stdout.write(f"Bulk inserting {total_inserted} new population records...")
                LocalityPopulation.objects.bulk_create(populations_to_insert, batch_size=500)
                
            # 2. Execute bulk update for existing records requiring data refresh
            if populations_to_update:
                total_updated = len(populations_to_update)
                self.stdout.write(f"Bulk updating {total_updated} pre-existing population matrices...")
                LocalityPopulation.objects.bulk_update(populations_to_update, ['population_estimates'], batch_size=500)

            if populations_to_insert or populations_to_update:
                self.stdout.write(self.style.SUCCESS("Successfully loaded and synced all population array matrices!"))
            else:
                self.stdout.write(self.style.WARNING("No records matched operational parameters."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Seeding process error context: {e}"))