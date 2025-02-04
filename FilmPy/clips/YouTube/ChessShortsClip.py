from ..ChessClip import ChessClip
from ...constants import Chess

class ChessShortsClip(ChessClip):
    """
    A Chess Clip with an appropriate size and length to be a YouTube short video
    """

    def __init__(self,
                 chess_board_orientation=Chess.WHITE.value,
                 chess_move_duration=None,
                 chesspy_game=None,
                 file_path=None,
                 clip_size=(1080, 1920),
                 **kwargs):
        """
        Initialize ChessClip object
        :param chess_move_duration: Amount of time in seconds, each move should be displayed for
        :param file_path: Path to a pgn chess file
        :param clip_size: Width and height of the clip. Width of the clip
        """

        # Move duration was not supplied, default to 2 seconds
        if not chess_move_duration:
            chess_move_duration = 2

        # If there are over 180, adjust the move duration
        number_moves = len(chesspy_game.moves)

        if number_moves > 175:
            chess_move_duration = .75
        elif number_moves >= 85:
                chess_move_duration = 1

        # Calculate the video's length, Add a "1 move" padding to the clips duration
        video_end_time = chess_move_duration * (number_moves+1)

        # Initialize the ChessClip
        super().__init__(chess_board_orientation=chess_board_orientation,
                         chess_move_duration=chess_move_duration,
                         chesspy_game=chesspy_game,
                         clip_size=clip_size,
                         file_path=file_path,
                         video_end_time=video_end_time,
                         **kwargs)