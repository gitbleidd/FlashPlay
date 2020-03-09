# FlashPlay

Простой скрипт на Python 3.5.3, который воспроизводит музыкальный файл (mp3 или wav) с подключенного USB-накопителя по нажатию на GPIO-кнопку.

### FlashPlay5Buttons

Модификация скрипта FlashPlay. Запускает музыкальный файл (только mp3), соответствующий одной из 5 GPIO-кнопок с подключенного USB-накопителя.

###Дополнительно:

Для корректной улучшения звука на Raspberry необходимо дописать строчку "audio_pwm_mode=2" в "/boot/config.txt", а также установить громкость командой "amixer set PCM -- 95%".



Также прилагается bash-скрипт, позволяющий зарегистрировать Python-скрипт в качестве сервиса (демона), а также скрипт для установки дополнительных библиотек

Ссылки на инструкции по настройке демона:

[Демонизация скрипта на Python](https://thingsmatic.com/2016/06/18/daemonize-that-python-script/)

[Запуск скрипта Python в фоновом процессе](http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/)
