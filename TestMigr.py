def some_func(arr1, arr2):
    for i in arr1:
        arr2.remove(i)
    sorted_unique_values = list(set(arr2))
    sorted_unique_values.sort(key=max)
    return sorted_unique_values

arr1 = [5, 4, 3, 4534535, 7, 6]
arr2 = [5, 4, 6, 8, 89, 5]

result = some_func(arr1, arr2)
print(result)
