from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from pytube import YouTube
from tkinter.messagebox import showinfo, showerror
import threading



# функция для загрузки видео
def download_video():

    # оператор try для исключения загрузки видеокода
    try:
        # получение url видео из записи
        video_link = url_entry.get()
        # получение разрешения видео из Combobox
        resolution = video_resolution.get()
        # проверка, пуста ли запись и combobox
        if resolution == '' and video_link == '':
            # отображение сообщения об ошибке, когда combobox пуст
            showerror(title='Error', message='Пожалуйста, введите URL видео и разрешение!!!')
        # проверка пустоты разрешения
        elif resolution == '':
            # отображение сообщения об ошибке, когда combobox пуст
            showerror(title='Error', message='Пожалуйста, выберите разрешение видео!!!')
        # проверка, является ли значение comboxbox значением None
        elif resolution == 'None':
            # отображение сообщения об ошибке, когда значение combobox равно None
            showerror(title='Error', message='Нет - это неправильное разрешение видео!!\n'\
                    'Пожалуйста, выберите правильное разрешение видео')
        # в противном случае давайте загрузим видео
        else:
            #  этот оператор try будет запущен, если разрешение для видео существует
            try:   
                # эта функция будет отслеживать прогресс загрузки видео
                def on_progress(stream, bytes_remaining):
                    # общий размер видео
                    total_size = stream.filesize
                    # эта функция получит размер видео
                    def get_formatted_size(total_size, factor=1024, suffix='B'):
                        # петляя по подразделениям
                        for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                            if total_size < factor:
                                return f"{total_size:.2f}{unit}{suffix}"
                            total_size /= factor
                        # возвращение размера отформатированного видео
                        return f"{total_size:.2f}Y{suffix}"



                    # получение размера отформатированного видео, вызывая функцию
                    formatted_size = get_formatted_size(total_size)
                    # размер, загруженный после запуска
                    bytes_downloaded = total_size - bytes_remaining
                    # процент загрузки после запуска
                    percentage_completed = round(bytes_downloaded / total_size * 100)
                    # обновление значения индикатора прогресса
                    progress_bar['value'] = percentage_completed
                    # обновление пустой метки значением процента
                    progress_label.config(text=str(percentage_completed) + '%, File size:' + formatted_size)
                    # обновление главного окна приложения
                    window.update()
                
                # создание объекта YouTube и передача функции on_progress
                video = YouTube(video_link, on_progress_callback=on_progress)
                # загрузка фактического видео
                video.streams.filter(res=resolution).first().download('C:\\download_youtube\download')
                # всплывающее окно для вывода сообщения об успешной загрузке видео
                showinfo(title='Download Complete', message='Видео успешно сохранено.')
                # переустановка индикатора выполнения и метки выполнения
                progress_label.config(text='')
                progress_bar['value'] = 0
            # except будет выполняться, если разрешение недоступно или недействительно
            except:
                showerror(title='Download Error', message='Не удалось загрузить видео для данного разрешения')
                # переустановка индикатора выполнения и метки выполнения
                progress_label.config(text='')
                progress_bar['value'] = 0
        
    # оператор except для отлова ошибок, URLConnectError, RegMatchError
    except:
        # всплывающее окно для отображения сообщения об ошибке
        showerror(title='Download Error', message='Произошла ошибка при попытке ' \
                    'Установки видео\nНиже приведены возможные варианты ' \
                    'были причинами:\n* Недопустимая ссылка\n* Отсутствие подключения к Интернету\n'\
                     'Убедитесь, что у вас стабильное интернет-соединение и ссылка на видео действительна')
        # переустановка индикатора выполнения и метки выполнения
        progress_label.config(text='')
        progress_bar['value'] = 0



# функция поиска разрешений видео
def searchResolution():
    # получение url видео из записи
    video_link = url_entry.get()
    # проверка пустой ли ссылки на видео
    if video_link == '':
        showerror(title='Error', message='Предоставьте ссылку на видео, пожалуйста!')
    # если ссылка на видео не пуста разрешение поиска
    else:
        try:
            # создание объекта YouTube
            video = YouTube(video_link)
            # пустой список, в котором будут храниться все видео разрешения
            resolutions = []
            # циклическое прохождение видеопотоков
            for i in video.streams.filter(file_extension='mp4'):
                # добавление разрешений видео в список разрешений
                resolutions.append(i.resolution)
            # добавление разрешений в combobox
            video_resolution['values'] = resolutions
            # после завершения поиска уведомить пользователя
            showinfo(title='Search Complete', message='Проверьте в Combobox доступные разрешения видео.')
        # перехватывать любые ошибки, если они возникают
        except:
            # уведомлять пользователя о возникновении ошибок
            showerror(title='Error', message='При поиске разрешения видео произошла ошибка!\n'\
                'Ниже приведены возможные причины\n* Нестабильное интернет-соединение\n* Недопустимая ссылка')





# функция для запуска функции SearchResolution в качестве потока
def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()
    
    
# функция для запуска функции download_video в качестве потока
def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()

# функция для запуска подсказки пользователю
def information():
    messagebox.showinfo('Подсказка', 'Ссылка это адресс на видеоролик, находится в поисковой строке')



# создает окно с помощью функции Tk()
window = Tk()

# создает заголовок для окна
window.title('Установка видео с YouTube')
# размеры и положение окна
window.geometry('500x250')
# делает окно не изменяемым по размеру
window.resizable(height=FALSE, width=FALSE)

# создает холст для размещения всех виджетов
canvas = Canvas(window, width=500, height=250)
canvas.pack()

##Стили для виджетов

# стиль для заголовка
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('Times New Roman', 20))

# стиль для записи
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 200))

# стиль для кнопки
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

##

# создание этикетки ттк
url_label = ttk.Label(window, text='Вставьте сылку на видео:', style='TLabel')
# создание записи в ттк
url_entry = ttk.Entry(window, width=76, style='TEntry')

# добавление метки на холст
canvas.create_window(165, 50, window=url_label)
# добавление записи на холст
canvas.create_window(250, 80, window=url_entry)

# создание ярлыка разрешения
resolution_label = Label(window, text='Разрешение:')
# добавление метки на холст
canvas.create_window(260, 120, window=resolution_label)


# создание combobox для хранения разрешений видео
video_resolution = ttk.Combobox(window, width=10)
# добавление комбобокса на холст
canvas.create_window(350, 120, window=video_resolution)


# создание кнопки для поиска резолюций
search_resolution = ttk.Button(window, text='Проверить разрешения', command=searchThread)
# добавление кнопки на холст
canvas.create_window(115, 120, window=search_resolution)


# создание пустой метки для отображения прогресса загрузки
progress_label = Label(window, text='')
# добавление метки на холст
canvas.create_window(240, 160, window=progress_label)

# создание индикатора выполнения для отображения прогресса
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=450, mode='determinate')
# добавление индикатора выполнения на холст
canvas.create_window(250, 160, window=progress_bar)

# создание кнопки
download_button = ttk.Button(window, text='Установка видео', style='TButton', command=downloadThread)
# добавление кнопки на холст
canvas.create_window(240, 200, window=download_button)

# создание кнопки
info_button = ttk.Button(window, text='Подсказка', style='TButton', command=information)
# добавление кнопки на холст
canvas.create_window(400, 50, window=info_button)

# запускает окно бесконечно
window.mainloop()