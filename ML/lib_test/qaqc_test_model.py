import pandas as pd
import csv
import re
import os

from .shared_model import IsbitClassifierModel

class QaqcTestModel(IsbitClassifierModel):

    def __init__(self, df: pd.DataFrame = None, source_data_path: str = None):
        super().__init__(df, source_data_path)
        self.processed_data_path = "data/QAQC_v1/swe_qaqc_prep_train.csv"

    def _format_data(self):
        """ Overrides base class method for specific dataset processing """
        if self.df is None and self.source_data_path:
            self.process_csv(self.source_data_path, self.processed_data_path)
            self.df = pd.read_csv(self.processed_data_path)

    # helper to remove outer quotation marks, specific for qaqc data set
    def strip_outer_quotationmarks(q):
        if q.startswith('"') and q.endswith('"'):
            q = q[1:-1]  
        return q.strip()
    
    def run(self):
        self._format_data
        # more stuff to come
    
    # helper to remove commas in the question text, specific for qaqc data set
    def replace_commas(line):
        pattern = r'"([^"]*?)"'
        def replace_commas(match):
            return '"' + match.group(1).replace(',', '|') + '"'
        return re.sub(pattern, replace_commas, line)

    def process_csv(self, source_data_path, output_data_path, temp_file_path="temp_file.csv"):
        with open(source_data_path, 'r', encoding='utf-8') as infile:
            modified_lines = [self.replace_commas(line.strip()) for line in infile]

        with open(temp_file_path, 'w', encoding='utf-8', newline='') as outfile:
            outfile.write('\n'.join(modified_lines))

        temp_data = pd.read_csv(temp_file_path, quoting=csv.QUOTE_NONE)
        questions = temp_data["text"].tolist()
        no_comma_questions = [self.strip_outer_quotationmarks(q) for q in questions]

        coarse_labels = list(map(lambda x: x.split(":")[0], temp_data["verbose label"].tolist()))  
        zipped = list(zip(no_comma_questions, coarse_labels))

        with open(output_data_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["text", "coarse label"])
            writer.writerows(zipped)

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
