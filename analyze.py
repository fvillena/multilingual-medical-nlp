from src.data.gms_data import GmsParser
from src.data.scielo_data import ScieloParser
from src.data.text_data import TextProcessor
from src.data.text_data import TextAnalyzer

gms_parser = GmsParser(r"data/raw/gms/")
gms_parser.parse(r"data/interim/")

scielo_parser = ScieloParser(r"data/raw/scielo/")
scielo_parser.parse(r"data/interim/")

processor = TextProcessor(r'data/interim/')
processor.process(output_folder = r'data/processed/', punctutation=False)

analyzer = TextAnalyzer(r'data/processed/')
analyzer.load_files()
analyzer.tfidf_analysis()
analyzer.generate_report()