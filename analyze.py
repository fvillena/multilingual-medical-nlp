from src.data.gms_data import GmsParser
from src.data.text_data import TextProcessor

gms_parser = GmsParser(r"data/raw/gms/")
gms_parser.parse(r"data/interim/")

processor = TextProcessor(r'data/interim/')
processor.process()