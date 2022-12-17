# Get data from .txt file
def get_input() -> str:
    with open('input/Day17.txt', 'r') as file:
        # Split lines and write each line to list
        data = file.read()
    return data


def create_piece(piece_type: str, height: int) -> list[tuple]:
    # Initialize list of piece parts
    piece_pos = []
    # Create the piece parts depending on the type
    match piece_type:
        case '-':
            piece_pos.append((2, height))
            piece_pos.append((3, height))
            piece_pos.append((4, height))
            piece_pos.append((5, height))
        case '+':
            piece_pos.append((3, height))
            piece_pos.append((2, height + 1))
            piece_pos.append((3, height + 1))
            piece_pos.append((4, height + 1))
            piece_pos.append((3, height + 2))
        case 'J':
            piece_pos.append((2, height))
            piece_pos.append((3, height))
            piece_pos.append((4, height))
            piece_pos.append((4, height + 1))
            piece_pos.append((4, height + 2))
        case 'I':
            piece_pos.append((2, height))
            piece_pos.append((2, height + 1))
            piece_pos.append((2, height + 2))
            piece_pos.append((2, height + 3))
        case 'o':
            piece_pos.append((2, height))
            piece_pos.append((3, height))
            piece_pos.append((2, height + 1))
            piece_pos.append((3, height + 1))

    return piece_pos


# Solves part 1
def part_one(jets: str, turns: int) -> int:
    shape_order = ['-', '+', 'J', 'I', 'o']
    # Initialize variables
    height = 0
    # Initialize floor
    pieces = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}
    # Loop through turns
    for i in range(turns):
        # Create new piece
        new_piece = create_piece(shape_order[i % 5], height + 4)
        candidate_move = new_piece.copy()
        # While the piece is not blocked
        while True:
            # Get the next jets push
            push = jets[0]
            # Move the operation to the back
            jets = jets[1:] + jets[0]
            # Push the piece with the jets
            # Check if the piece can be pushed
            if push == '<':
                # Check if the piece doesn't hit the left wall
                width = min(new_piece, key=lambda item: item[0])[0]
                if width > 0:
                    candidate_move = [(x - 1, y) for x, y in new_piece]
            elif push == '>':
                # Check if the piece doesn't hit the right wall
                width = max(new_piece, key=lambda item: item[0])[0]
                if width < 6:
                    candidate_move = [(x + 1, y) for x, y in new_piece]
            # Check if any piece would be blocked, if not, update
            if not bool(set(candidate_move) & pieces):
                new_piece = candidate_move.copy()

            # Move the piece one down
            candidate_move = [(x, y - 1) for x, y in new_piece]
            # Check if any piece would be blocked
            if bool(set(candidate_move) & pieces):
                # Correct position and add to pieces
                pieces.update(new_piece)
                # Update height
                height = max(pieces, key=lambda item: item[1])[1]
                break
            # Otherwise update new piece position
            else:
                new_piece = candidate_move.copy()
    return height


# Solves part 2
def part_two(jets: str, turns: int) -> int:
    shape_order = ['-', '+', 'J', 'I', 'o']
    # Initialize variables
    height = 0
    shape_count = 0
    jet_count = 0
    # Initialize floor
    pieces = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}
    # Initialize repeater to check repeated patterns
    repeater = {}
    # Loop through all turns
    while turns > 0:
        # Create new piece
        new_piece = create_piece(shape_order[shape_count % 5], height + 4)
        candidate_move = new_piece.copy()
        # While the piece is not blocked
        while True:
            # Get the next jet push, here we need to use indices due to the repeater
            push = jets[jet_count % len(jets)]
            # Check if the piece can be pushed
            if push == '<':
                # Check if the piece doesn't hit the left wall
                width = min(new_piece, key=lambda item: item[0])[0]
                if width > 0:
                    candidate_move = [(x - 1, y) for x, y in new_piece]
            elif push == '>':
                # Check if the piece doesn't hit the right wall
                width = max(new_piece, key=lambda item: item[0])[0]
                if width < 6:
                    candidate_move = [(x + 1, y) for x, y in new_piece]
            # Check if any piece would be blocked, if not, update
            if not bool(set(candidate_move) & pieces):
                new_piece = candidate_move.copy()

            # Move the piece one down
            candidate_move = [(x, y - 1) for x, y in new_piece]
            # Check if any piece would be blocked
            if bool(set(candidate_move) & pieces):
                # Correct position and add to pieces
                pieces.update(set(new_piece))
                # Update height
                height = max(pieces, key=lambda item: item[1])[1]
                # Increase jet count
                jet_count += 1
                # Break the loop and continue with next piece
                break
            # Otherwise update new piece position
            else:
                new_piece = candidate_move.copy()
                # Increase jet count
                jet_count += 1

        # Reduce number of turns
        turns -= 1

        # Performance optimization: Find repeated patterns and reduce needed operations
        # Get height levels
        height_levels = [0, 0, 0, 0, 0, 0, 0]
        for piece in pieces:
            x, y = piece
            if y > height_levels[x]:
                height_levels[x] = y
        # Subtract current height from list to get the relative shape
        height_levels = [y - height for y in height_levels]

        # Check if the repeater already contains this shape count, jet count, and height shape
        if (shape_count % 5, jet_count % len(jets), tuple(height_levels)) in repeater:
            # If yes, get the previous values
            turns_old, height_old = repeater[(shape_count % 5, jet_count % len(jets), tuple(height_levels))]
            # Update height of pieces
            new_pieces = set()
            for piece in pieces:
                x, y = piece
                y += (height - height_old) * (turns // (turns_old - turns))
                new_pieces.add((x, y))
            pieces = new_pieces
            # Update height and time
            height = height + (height - height_old) * (turns // (turns_old - turns))
            turns = turns % (turns_old - turns)
        # Otherwise, add shape count, jet count, and height shape as new key to repeater
        else:
            repeater[(shape_count % 5, jet_count % len(jets), tuple(height_levels))] = turns, height
        # Increase shape count
        shape_count += 1
    return height


def main():
    print('The tower will be this tall after 2022 rocks have stopped falling:', part_one(get_input(), 2022))
    print('The tower will be this tall after 1 trillion rocks:', part_two(get_input(), 1_000_000_000_000))


if __name__ == '__main__':
    main()
