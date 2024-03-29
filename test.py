
# count 65
# список данных
data = ["Kirill", "Dima", "Anton", "Ivan", "Ilya", "Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya","Kirill", "Dima", "Anton", "Ivan", "Ilya"]
print(len(data))

pageNumber = 1
pageSize = 5

# pNumber 1: 0 - 4
# pNumber 2: 3 - 5
# pNumber 3: 6 - 8
# pNumber 4: 9 - 11
# pNumber 5: 12 - 14
# pNumber 6: 15 - 17
# pNumber 7: 18 - 20

# pNumber 1: 1 - 3
# pNumber 2: 4 - 6
# pNumber 3: 7 - 9
# pNumber 4: 10 - 12
# pNumber 5: 13 - 15
# pNumber 6: 16 - 18
# pNumber 7: 19 - 21

endIndex = pageNumber * pageSize - 1
startIndex = endIndex - (pageSize - 1)

result = data[startIndex:endIndex+1]    # в срезах координата "до" не включается, поэтому + 1
print(result)