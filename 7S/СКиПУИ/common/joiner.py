from pathlib import Path
from base64 import b64decode
from json import load

# Запрос имени каталога у пользователя
catalog_name = input('Enter the directory containing parts: ')
catalog_path = Path(catalog_name)

# Проверка существования каталога
if not catalog_path.is_dir():
	raise RuntimeError(f'Invalid directory: {catalog_path}.')

# Загрузка метаданных из meta.json
meta_filepath = catalog_path / 'meta.json'
if not meta_filepath.exists():
	raise RuntimeError(f'Metadata file not found: {meta_filepath}.')

with open(meta_filepath, 'r') as meta_file:
	meta_data = load(meta_file)
	filename = meta_data['filename']
	extension = meta_data['extension']

# Подготовка к объединению файлов
output_filepath = Path(f"{filename}{extension}")

# Открываем выходной файл для записи
output_file = open(output_filepath, 'wb')
# Считываем и объединяем закодированные части
counter = 0
while True:
	part_filepath = catalog_path / f'part_{counter}.b64'
	if not part_filepath.exists():
		break # Если файл не существует, прерываем цикл

	with open(part_filepath, 'rb') as part_file:
		encoded_content = part_file.read()
		decoded_content = b64decode(encoded_content)
		output_file.write(decoded_content)

	print(f'Added: {part_filepath}') # Информация о добавлении части
	counter += 1
	
output_file.close()
print(f'Combined file saved as: {output_filepath}') # Финальное сообщение об объединении
