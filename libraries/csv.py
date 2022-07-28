from . import configuration
from os import listdir
from os.path import join
import csv


class CSVHandlers:
    def __init__(self, abs_instance_path):
        self.config_handler = configuration.ConfigurationHandler(abs_instance_path)
        self.DEFAULT_SECTION = self.config_handler.read_section_by('DEFAULT')
        self.CSV_SECTION = self.config_handler.read_section_by('csv')
        self.MAPPING_SECTION = self.config_handler.read_section_by('mapping')

    def key_pair_build(self):
        """Build old_key: new_key dictionary.

        Loop over 'ExportDir'. Process items inside with DictReader method.
        Build and return old_key: new_key dict. Mapping is defined in 'mapping' section.
        """
        issue_key_delta = {}
        for export_unit in listdir(self.DEFAULT_SECTION['ExportDir']):
            if export_unit.endswith('.csv'):
                with open(join(self.DEFAULT_SECTION['ExportDir'], export_unit), 'r', encoding='utf-8', newline='\n') as blank:
                    cached_unit = list(csv.DictReader(blank, dialect=self.CSV_SECTION['Dialect'], delimiter=self.CSV_SECTION['Delimiter']))
                for row in cached_unit:
                    if row.get(self.MAPPING_SECTION['NewField']) is not None and row.get(self.MAPPING_SECTION['OldField']) is not None:
                        issue_key_delta[row.get(self.MAPPING_SECTION['OldField'])] = row.get(self.MAPPING_SECTION['NewField'])
        return issue_key_delta

