import math as m


def rotate(point_a, point_b, a):
    xa, ya, xb, yb = point_a[0], point_a[1], point_b[0], point_b[1]
    a = a * (m.pi / 180)
    # перенесем вращение в точку А и крутим
    xb = xb - xa
    yb = yb - ya
    xb_r = (xb * m.cos(a)) - (yb * m.sin(a)) + xa
    yb_r = (xb * m.sin(a)) + (yb * m.cos(a)) + ya  # с функции выходит ошибка в миллионных долях
    return [xb_r, yb_r]  # поворот AB вокруг A на угол a, возвращаем положение B


def find_tops(house_A, house_b):
    tops = []
    for i in range(24):
        xa = -m.sin(i * (15 * m.pi / 180)) * (house_b[1] - house_A[1]) + m.cos(i * (15 * m.pi / 180)) * (
                house_b[0] - house_A[0]) + house_A[0]
        ya = m.cos(i * (15 * m.pi / 180)) * (house_b[1] - house_A[1]) + m.sin(i * (15 * m.pi / 180)) * (
                house_b[0] - house_A[0]) + house_A[1]
        for j in range(24):
            xb = -m.sin(j * (15 * m.pi / 180)) * (house_A[1] - house_b[1]) + m.cos(j * (15 * m.pi / 180)) * (
                    house_A[0] - house_b[0]) + house_b[0]
            yb = m.cos(j * (15 * m.pi / 180)) * (house_A[1] - house_b[1]) + m.sin(j * (15 * m.pi / 180)) * (
                    house_A[0] - house_b[0]) + house_b[1]
            if m.isclose(xa, xb, abs_tol=1e-06) == True and m.isclose(ya, yb, abs_tol=1e-06) == True:
                tops.append([xa, ya])
    return tops


def distance(point1, point2):  # точка, которую с которой
    try:
        return m.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    except:
        return 0


def find_round_center(p1, p2, p3):
    a = p2[0] - p1[0]
    b = p2[1] - p1[1]
    c = p3[0] - p1[0]
    d = p3[1] - p1[1]
    e = a * (p1[0] + p2[0]) + b * (p1[1] + p2[1])
    f = c * (p1[0] + p3[0]) + d * (p1[1] + p3[1])
    g = 2 * (a * (p3[1] - p2[1]) - b * (p3[0] - p2[0]))
    Ox = (d * e - b * f) / g
    Oy = (a * f - c * e) / g
    return [round(Ox, 7), round(Oy, 7), distance([Ox, Oy], p1), p1, p2]  # возвращаем координаты центра и радиус


def point_of_intersection(center1_XY_r, center2_XY_r):
    # ищем точки пересечения 2х окружностей - 1\2 и 1\3. таким образом поиск пересечения по 3ей окружносте отпадает за ненадобностью
    x1, y1, r1 = center1_XY_r[0], center1_XY_r[1], center1_XY_r[2]
    x2, y2, r2 = center2_XY_r[0], center2_XY_r[1], center2_XY_r[2]

    d12 = distance([x1, y1], [x2, y2])
    a12 = ((r1 ** 2) - (r2 ** 2) + (d12 ** 2)) / (2 * d12)
    if m.isclose(d12, 0, abs_tol=1e-06) == True and m.isclose(r1, r2, abs_tol=1e-06) == True:
        return m.nan
    elif round(d12, 5) < round(m.fabs(r1 - r2), 5):  # окружность внутри - нет пересечения
        return m.nan
    elif d12 > r1 + r2:  # окружность наружи - нет пересечения
        return m.nan
    else:
        try:
            h12 = m.sqrt((r1 ** 2) - (a12 ** 2))
            p3x = x1 + ((a12 / d12) * (x2 - x1))
            p3y = y1 + ((a12 / d12) * (y2 - y1))
            xi1 = round(p3x + (h12 / d12) * (y2 - y1), 8)
            yi1 = round(p3y - (h12 / d12) * (x2 - x1), 8)
            xi2 = round(p3x - (h12 / d12) * (y2 - y1), 8)
            yi2 = round(p3y + (h12 / d12) * (x2 - x1), 8)
            return [xi1, yi1], [xi2, yi2]
        except:
            h12 = 0
            p3x = x1 + ((a12 / d12) * (x2 - x1))
            p3y = y1 + ((a12 / d12) * (y2 - y1))
            xi1 = round(p3x + (h12 / d12) * (y2 - y1), 8)
            yi1 = round(p3y - (h12 / d12) * (x2 - x1), 8)
            # p3 = np.array(x1,y1) + ((a12 / d12) * (np.array(x2,y2)-np.array(x1,y1))

            return [xi1, yi1]


houses = []
coordinats = input().split(' ')
tops = []
for i in range(5):
    if i % 2 == 0:
        houses.append([float(coordinats[i]), float(coordinats[i + 1])])
# найдем вершины равнобндренных треугольников
for i in range(len(houses)):
    for j in range(len(houses)):
        if i > j:
            tops.append(find_tops(houses[i], houses[j]))  # набор всех вершин для каждой стороны (6 штук)
# опишем окружности по 3м точкам  и найдем координаты центра окружности, и ее радиус.
xyr = []
ans = []
k = 0
for i in range(len(houses)):
    for j in range(len(houses)):
        if j > i:
            for l in range(2):
                xyr.append(find_round_center(houses[i], houses[j], tops[k][l]))
            k = k + 1
for i in range(len(xyr)):
    for j in range(len(xyr)):
        if j > i:
            a = point_of_intersection(xyr[i], xyr[j])
            try:
                for l in range(len(a)):
                    try:
                        ans.append([a[l][0], a[l][1], max(distance([a[l][0], a[l][1]], houses[0]),
                                                          distance([a[l][0], a[l][1]], houses[1]),
                                                          distance([a[l][0], a[l][1]], houses[2]))])
                    except:
                        ans.append([a[l], a[l + 1], max(distance([a[l], a[l + 1]], houses[0]),
                                                        distance([a[l], a[l + 1]], houses[1]),
                                                        distance([a[l], a[l + 1]], houses[2]))])
            except:
                continue
answers = []
for i in range(len(ans)):
    counter = 0
    for j in range(len(ans)):
        if j > i and (m.isclose(ans[i][0], ans[j][0], abs_tol=1e-06) == True) and (
                m.isclose(ans[i][1], ans[j][1], abs_tol=1e-06) == True):
            counter = counter + 1
    if counter > 1:
        flag = False
        if answers != []:
            for g in range(len(answers)):
                if m.isclose(ans[i][0], answers[g][0], abs_tol=1e-06) == True:
                    continue
                else:
                    answers.append(ans[i])
        else:
            answers.append(ans[i])
shortest = m.inf
ans1 = []
for i in range(len(answers)):
    if answers[i][2] < shortest:
        shortest = answers[i][2]
        ans1 = answers[i][:2]
print("{:.6F}".format(ans1[0]), "{:.6F}".format(ans1[1]))
