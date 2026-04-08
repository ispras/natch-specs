#!/bin/bash

settingsFile="/usr/bin/snatch/snatch/settings.py"


# Update path function
updatePath() {
    local newPath="$1"
    
    # Check if the path is valid
    if [ ! -d "$newPath" ]; then
        echo "Создание директории: $newPath"
        mkdir -p "$newPath"
        if [ $? -ne 0 ]; then
            echo "Ошибка: Не могу создать каталог $newPath"
            return 1
        fi
    fi
    
    # Set permissions
    chown "$USER":"$USER" "$newPath"
    chmod 750 "$newPath"
    
    # Create backup for the settings file
    sudo cp "$settingsFile" "$settingsFile.bak"
    
    # Update path
    sudo sed -i "s|^MEDIA_ROOT = .*|MEDIA_ROOT = '$newPath'|" "$settingsFile"
    
    echo "Путь для данных проектов изменен на $newPath"
    echo "Конфиг обновлен: $settingsFile"
    echo "Архивная копия настроек: $settingsFile.bak"

    # Removing the old path
    rm -rf $currentPath

    echo "Перезапуск Snatch ..."
    /usr/bin/snatch/snatch_stop.sh
    /usr/bin/snatch/snatch_start.sh
    
    return 0
}


# Detecting a logged in user
if [ -n "$SUDO_USER" ]; then
    USER="$SUDO_USER"
else
    USER="$(whoami)"
fi
#echo "Текущий пользователь: $USER"

currentPath=$(grep "^MEDIA_ROOT = " "$settingsFile" | cut -d'=' -f2)
if [[ $currentPath == *"os.path"* ]]; then
    currentPath=$(/usr/bin/python3 -c "import os; print($currentPath)")
else
    currentPath=$(echo $currentPath | sed "s/'//g")
fi
echo "Текущий путь для хранения данных проектов: $currentPath"

# Removing the dir makes the already created projects unavailable, so this was not a good idea
# if [ -d $currentPath ]; then 
#     if [ ! -z "$(ls -A $currentPath)" ]; then
#         echo "Каталог не пуст. Существующие проекты будут удалены в случае продолжения."
#     else
#         echo "В указанном каталоге нет проектов."
#     fi
# else
#     echo "Каталога $currentPath не существует."
# fi

read -p "Введите новый путь (или оставьте пустым для отмены): " newPath

if [ -n "$newPath" ]; then
    updatePath "$newPath"
else
    echo "Операция отменена"
fi
