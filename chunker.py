def chunk_recipients(numbers: list[str], chunk_size: int = 100) -> list[list[str]]:
    """
    Takes an arbitrary list of phone numbers (N) and slices it 
    into a list of sub-lists, each containing up to 'chunk_size' numbers.
    """
    return [numbers[i : i + chunk_size] for i in range(0, len(numbers), chunk_size)]


if __name__ == "__main__":
    # Test list with 250 numbers
    dummy_numbers = [f"+2348000000{i:03d}" for i in range(1, 251)]
    
    print(f"Total numbers generated: {len(dummy_numbers)}")
    
    # Chunk into batches of 100
    batches = chunk_recipients(dummy_numbers, chunk_size=100)
    
    print(f"Total batches created: {len(batches)}")
    
    for index, batch in enumerate(batches, start=1):
        print(f"Batch {index}: contains {len(batch)} numbers")