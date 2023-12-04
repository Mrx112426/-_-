import random

def quick_select(arr : list[int], k : int) -> int:
    if len(arr) == 1:
        return arr[0]

    pivot = arr[random.randint(0, len(arr)-1)]
    L : list[int] = []
    M: list[int] = []
    R: list[int] = []

    for val in arr:
        if pivot > val:
            L.append(val)

    for val in arr:
        if pivot == val:
            M.append(val)

    for val in arr:
        if pivot < val:
            R.append(val)

    if k <= len(L):
        return quick_select(L,k)
    elif k<= (len(L) + len(M)):
        return pivot
    else:
        return quick_select(R, k - (len(L) + len(M)))


if __name__ == "__main__":
    arr = [10,20,30,40,50,60,70]
    print(f"Array : {arr}")
    k = 7
    kMin = quick_select(arr, k)
    print(f"{k} - th min element is {kMin}")
    k = 2
    kMin = quick_select(arr,k)
    print(f"{k} - th min element is {kMin}")
    k = 1
    kMin = quick_select(arr, k)
    print(f"{k} - th min element is {kMin}")
