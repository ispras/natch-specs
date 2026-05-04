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
    su -c "cp $settingsFile $settingsFile.bak"

    # Update path
    su -c "sed -i \"s|^MEDIA_ROOT = .*|MEDIA_ROOT = '$newPath'|\" $settingsFile"

    echo "Путь для данных проектов изменен на $newPath"
    echo "Файл настроек обновлен: $settingsFile"
    echo "Архивная копия настроек: $settingsFile.bak"

    read -p "Хотите удалить каталог старый каталог с проектами? (y/n): " answer

    if [[ $answer == "y" || $answer == "Y" ]]; then
        su -c "rm -rf $currentPath"
        echo "Каталог $currentPath удален"
    fi

    echo "Перезапуск Snatch ..."
    su -c "/usr/bin/snatch/snatch_stop.sh"
    su -c "/usr/bin/snatch/snatch_start.sh"

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

read -p "Введите новый путь (или оставьте пустым для отмены): " newPath

if [ -n "$newPath" ]; then
    updatePath "$newPath"
else
    echo "Операция отменена"
fi
