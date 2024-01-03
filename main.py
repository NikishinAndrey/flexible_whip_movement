import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, HTMLWriter

# Параметры веревки

# Параметры веревки
length = 0.5  # длина веревки
num_points = 40  # количество точек на веревке
time_steps = 50000  # количество временных шагов
mass_array = np.arange(num_points, 0, -1)
mass_array = mass_array / sum(mass_array)
print(mass_array)
v_ampl = 5
c = 100
M = 1

gravity = False #True
x_border = True
criterion_stop = True #False

const_frame = 400 # количество
frame_count = 400
final_frame_count = num_points * 100*1 + 100*1 * num_points // 4
printEvery = num_points*1 // 4

g = 9.81
tau = np.pi * np.sqrt(sum(mass_array) / c)

# Начальные условия оси Ox
x = np.linspace(0, length, num_points) / length
# Начальные условия оси Oy
y = np.zeros(num_points)  # изначально точки находятся на линии y = 0
y = y / length

# Нулевые начальные условия на скорость вдоль оси Ox
velocity_x = np.zeros(num_points) / length * tau
# Нулевые начальные условия на скорость вдоль оси Oy
velocity_y = np.zeros(num_points) / length * tau


F_x = np.zeros(num_points - 1)
F_y = np.zeros(num_points - 1)
T = np.linspace(0, 50 * tau, time_steps) / tau

dt = T[1] - T[0]
print(f"dt/tau: {dt / tau}")
frequency = 1/(const_frame*4*dt)
print(f'Частота: {frequency}')
x[0] = 0
y[0] = 0
velocity_x[0] = 0
velocity_y[0] = 0

a = 1 / num_points
if gravity:
    coefficient = np.array([(mass_array[i] * g) / (c * length) for i in range(num_points)])
else:
    coefficient = np.array([0] * num_points)

# Создание графика
fig, ax = plt.subplots()
# plt.ylim(-100, 100)
plt.ylim(-10, 10)
# hide x-axis
ax.get_xaxis().set_visible(False)
# hide y-axis
ax.get_yaxis().set_visible(False)

# line, = ax.plot(x, y, marker='o')
line, = ax.plot(x, y, 'o')

# надо в разных циклах искать скорости и перемещения
# Функция обновления графика на каждом временном шаге

velocity_y[0] = v_ampl
flag = -1
frame_count = 400  # итератор по времени


resultsX = np.zeros((final_frame_count, num_points))
resultsY = np.zeros_like(resultsX)
resultsVX = np.zeros_like(resultsX)
resultsVY = np.zeros_like(resultsX)

resultsX[0, :] = x
resultsY[0, :] = y
resultsVX[0, :] = velocity_x
resultsVY[0, :] = velocity_y

for i in range(1, resultsX.shape[0]):
    # deltaX = (np.roll(resultsX[i - 1], -1) - resultsX[i - 1])[:-1]
    # deltaY = (np.roll(resultsY[i - 1], -1) - resultsX[i - 1])[:-1]
    # delta = np.sqrt(deltaX ** 2 + deltaY ** 2)

    x = resultsX[i - 1].copy()
    y = resultsY[i - 1].copy()
    velocity_x = resultsVX[i - 1].copy()
    velocity_y = resultsVY[i - 1].copy()

    delta_x = x[1] - x[0]
    delta_y = y[1] - y[0]
    l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)

    F_x[0] = (l1 - a) * delta_x / l1
    F_y[0] = (l1 - a) * delta_y / l1

    if not criterion_stop:
        if i == frame_count:
            print(i)
            velocity_y[0] = flag * v_ampl
            flag = flag * (-1)
            frame_count += const_frame * 2
    else:
        if i == frame_count and i < const_frame*6:
            print(i)
            velocity_y[0] = flag * v_ampl
            flag = flag * (-1)
            frame_count += const_frame*2

        if i == const_frame*6:
            velocity_y[0] = 0


    for j in range(1, num_points - 1):
        delta_x = x[j + 1] - x[j]
        delta_y = y[j + 1] - y[j]
        l1 = np.sqrt(delta_x ** 2 + delta_y ** 2)

        F_x[j] = (l1 - a) * delta_x / l1
        F_y[j] = (l1 - a) * delta_y / l1

        velocity_x[j] = velocity_x[j] + (F_x[j] - F_x[j - 1]) * dt * (4 * np.pi ** 2)
        velocity_y[j] = velocity_y[j] + (F_y[j] - F_y[j - 1] - coefficient[j]) * dt * (4 * np.pi ** 2)

    velocity_x[num_points - 1] = velocity_x[num_points - 1] + (
        -F_x[num_points - 1 - 1]) * dt * (4 * np.pi ** 2)
    velocity_y[num_points - 1] = velocity_y[num_points - 1] + (
            -F_y[num_points - 1 - 1] - coefficient[num_points - 1]) * dt * (4 * np.pi ** 2)

    for j in range(num_points):
        x[j] = x[j] + velocity_x[j] * dt
        y[j] = y[j] + velocity_y[j] * dt
        if x_border and i <= num_points*100:
            if 1 <= j <= num_points - 1:
                x[j] = max(x[j], x[j - 1])


    x[0] = x[0] + velocity_x[0] * dt
    y[0] = y[0] + velocity_y[0] * dt
    for j in range(1, num_points):
        x[j] = x[j] + velocity_x[j] * dt
        y[j] = y[j] + velocity_y[j] * dt

    resultsX[i] = x
    resultsY[i] = y
    resultsVX[i] = velocity_x
    resultsVY[i] = velocity_y


def update(frame):
    line.set_xdata(resultsX[frame * printEvery])
    line.set_ydata(resultsY[frame * printEvery])
    return line,


# Создание анимации
ani = FuncAnimation(fig, update, frames=resultsX.shape[0] // printEvery - 1, interval=1, blit=True)

#Сохранение анимации в видеофайл GIF
if gravity:
    ani.save(f'ani_m={sum(mass_array):.2f}_c={c}_v_ampl={v_ampl}_points={num_points}_frequency={frequency:.2f}_stop={criterion_stop}.gif', writer="ffmpeg", fps=60)
else:
    ani.save(f'ani_c={c}_v_ampl={v_ampl}_points={num_points}_frequency={frequency:.2f}_stop={criterion_stop}.gif', writer="ffmpeg", fps=60)


# #Сохранение анимации в страницу HTML
# if gravity:
#     ani.save(f'ani_m={sum(mass_array):.2f}_c={c}_v_ampl{v_ampl}_points={num_points}.html', writer=HTMLWriter())
# else:
#     ani.save(f'ani_c={c}_v_ampl{v_ampl}_points={num_points}.html', writer=HTMLWriter())


# Отображение анимации
plt.xlabel('X')
plt.ylabel('Y')
plt.title(f'Движение хлыста, Масса = {sum(mass_array):.2f}, жесткость связей = {c}, количество частиц')
# plt.show()
