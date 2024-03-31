from pathlib import Path

source_dir = Path(__file__).resolve().parent
data_dir = Path(source_dir, 'data')

deputados_path = Path(data_dir, 'dataset_deputados.json')
frentes_path = Path(data_dir, 'dataset_frentes.json')
