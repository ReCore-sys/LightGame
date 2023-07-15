def convert_size(amount: int) -> str:
    sizes = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while amount > 1024:
        amount /= 1024
        i += 1
    return f"{round(amount, 2)} {sizes[i]}"