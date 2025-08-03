import time
from multiprocessing import Pool, cpu_count

def get_dvisiors(n):
    divisors = []
    for i in range(1, n+1):
        if n % i == 0:
            divisors.append(i)
    return divisors

def factorize(*numbers):
    result = []
    for number in numbers:
        result.append(get_dvisiors(number))
    return result

def factorize_parallel(*numbers):
    num_cores = cpu_count()
    with Pool(num_cores) as pool:
        result = pool.map(get_dvisiors, numbers)
    return result

if __name__ == "__main__":
    test_numbers = (128, 255, 99999, 10651060)

    print(f"--- Запуск синхронної версії ---")
    start_time_sync = time.time()
    a, b, c, d = factorize(*test_numbers)
    end_time_sync = time.time()
    duration_sync = end_time_sync - start_time_sync

    print(f"Результати синхронної версії:")
    print(f"128: {a}")
    print(f"255: {b}")
    print(f"99999: {c}")
    print(f"10651060: {d}")
    print(f"Час виконання синхронної версії: {duration_sync:.4f} секунд")
    print("-" * 40)

    print(f"--- Запуск паралельної версії ---")
    start_time_parallel = time.time()
    parallel_results = factorize_parallel(*test_numbers)
    end_time_parallel = time.time()
    duration_parallel = end_time_parallel - start_time_parallel
    if parallel_results and len(parallel_results) == len(test_numbers):
        a_p, b_p, c_p, d_p = parallel_results
        print(f"Використано ядер процесора: {cpu_count()}")
        print(f"Результати паралельної версії:")
        print(f"128: {a_p}")
        print(f"255: {b_p}")
        print(f"99999: {c_p}")
        print(f"10651060: {d_p}")
        print(f"Час виконання паралельної версії: {duration_parallel:.4f} секунд")
        print("-" * 40)

    print("--- Запуск тестів для перевірки коректності ---")
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("Тести пройдено успішно!")