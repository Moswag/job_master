l = [1, 3, 7, 5]
sum = 0
for element in l:
    for x in l:
        if x == element:
            continue
        else:
            sum += x
    print(sum)
