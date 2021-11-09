from demo_filler.demo.player import Player


def main():
    player = Player(input_player_num())
    while True:
        player.board.input()
        player.piece.input()
        player.put_piece()


def input_player_num() -> int:
    return int(input().split()[2][1])


if __name__ == "__main__":
    main()
