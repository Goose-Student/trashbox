from pathlib import Path
from os import mkdir
from shutil import rmtree
from base64 import b64encode
from json import dump

# Запрос имени файла у пользователя
filename = input('Enter filename: ')
filepath = Path(filename)

if not filepath.exists():
	raise RuntimeError(f'Invalid filepath {filepath}.')

# Получаем имя файла без расширения и расширение
stem = filepath.stem
extension = filepath.suffix
catalog = Path(stem)

# Удаляем каталог, если он существует, и создаем новый
if catalog.exists():
	rmtree(catalog)
mkdir(catalog)

# Создаем файл meta.json и записываем в него имя файла и его расширение
meta_data = {
	'filename': stem,
	'extension': extension
}
meta_filepath = catalog / 'meta.json'
with open(meta_filepath, 'w') as meta_file:
	dump(meta_data, meta_file, indent=4)

# Определяем размер блока 80 МБ
chunk_size = 80 * 1024 * 1024

# Чтение файла и разбиение на блоки
file = open(filepath, 'rb')
counter = 0
while True:
	# Чтение порции данных
	content = file.read(chunk_size)
	if not content:
		break # Если конец файла, выходим из цикла

	# Кодирование блока в Base64
	encoded_content = b64encode(content)

	# Запись закодированного блока в новый файл
	part_filepath = catalog / f'part_{counter}.b64'
	with open(part_filepath, 'wb') as part_file:
		part_file.write(encoded_content)

	print(f'Created: {part_filepath}') # Информация о созданном файле
	counter += 1
file.close()
print(f'Metadata saved to: {meta_filepath}') # Информация о созданном файле метаданных
