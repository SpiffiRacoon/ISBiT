import pandas as pd
import csv
import re
import os

from ..shared import IsbitClassifierModel

class QaqcTestModel(IsbitClassifierModel):

    def _format_data(self, file_name: str):
        """
        Function to format the QAQC data set, replaces comma signs iniside the question data with pipe sign |
        and removes outer qutation marks from the questions, also adds escape characters where its needed.
        """
        source_data_path = f"src/data/{file_name}.csv"
        output_data_path = f"src/data/output/{file_name}_prep.csv"
        with open(source_data_path, 'r', encoding='utf-8') as infile:
            modified_lines = [[x for x in self.replace_commas(line.strip()).split(",")] for line in infile]

        temp_data = pd.DataFrame(modified_lines[1:], columns = modified_lines[0])
        questions = temp_data["text"].tolist()
        no_comma_questions = [self.strip_outer_quotationmarks(q) for q in questions]

        coarse_labels = list(map(lambda x: x.split(":")[0], temp_data["verbose label"].tolist()))  
        zipped = list(zip(no_comma_questions, coarse_labels))

        os.makedirs(os.path.dirname(output_data_path), exist_ok=True)
        with open(output_data_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["text", "coarse label"])
            writer.writerows(zipped)

    # helper to remove outer quotation marks, specific for qaqc data set
    def strip_outer_quotationmarks(q):
        if q.startswith('"') and q.endswith('"'):
            q = q[1:-1]  
        return q.strip()
    
    # helper to remove commas in the question text, specific for qaqc data set
    def replace_commas(line):
        pattern = r'"([^"]*?)"'
        def replace_commas(match):
            return '"' + match.group(1).replace(',', '|') + '"'
        return re.sub(pattern, replace_commas, line)

    def first_run(self, df: pd.DataFrame):
        self._format_data(df)
        # more stuff to come, needs to set the self.df as a panda dataFrame with question data and point data (x,y)
