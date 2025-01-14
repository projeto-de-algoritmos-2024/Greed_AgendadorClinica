def interval_scheduling(intervals):
    intervals.sort(key=lambda x: x[1])
    
    selected_intervals = []
    last_end_time = float('-inf')
    
    for start, end in intervals:
        if start >= last_end_time:
            selected_intervals.append((start, end))
            last_end_time = end
    
    return selected_intervals

tasks = [(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]
result = interval_scheduling(tasks)
print("Intervalos selecionados:", result)
