import chess
import chess.pgn
import chess.svg

from pgn_parser import parser, pgn
from PIL import Image as PILImage, ImageFont as PILImageFont, ImageDraw as PILImageDraw
from wand.image import Image as WandImage
from wand.color import Color as WandColor
import numpy

from .ClipBase import ClipBase
class ChessClip(ClipBase):
    """
    Create a chess clip from a pgn file
    """

    def _draw_player_bars(self):
        """

        """

    def __init__(self,
                 chess_move_duration=3,
                 file_path=None,
                 clip_size=(1080, 1920),
                 video_end_time=180,
                 **kwargs):
        """
        Initialize ChessClip object
        :param chess_move_duration: Amount of time in seconds, each move should be displayed for
        :param file_path: Path to a pgn chess file
        :param clip_size: Width and height of the clip. Width of the clip
        """


        if not file_path:
            raise ValueError(f'{type(self).__name__}.init(file_path=None) is invalid. '
                             f'Provide a valid path to a pgn file')


        # Initialize the ClipBase
        super().__init__(clip_height=clip_size[1],
                         clip_pixel_format='rgba',
                         clip_width=clip_size[0],
                         file_path=file_path,
                         video_end_time=video_end_time,
                         **kwargs)

        # Open the pgn file and read its contents
        with open(file_path) as f:
            pgn_file_contents = f.read()

        # Parse the pgn file
        game = parser.parse(pgn_file_contents, actions=pgn.Actions())
        print(game)
        # Create a chess board
        board = chess.Board()

        # Start a list of frames for this clip
        frames = []
        # Iterate through the moves of the game
        for move in game.movetext:
            # Split the move string
            move_number, san_move, move_dict = str(move).split(' ',2)
            board.push_san(san_move)

            # Convert the board to SVG
            board_svg = chess.svg.board(board)

            # Convert the svg to a png to a numpy array
            wi = WandImage(blob=board_svg.encode(),
                           format='svg',
                           width=clip_size[0],
                           height=clip_size[0],
                           background=WandColor('#00000000'))
            wi.save(filename='board.png')

            # Create ndarray of the board
            board_ndarray = numpy.array(PILImage.open('board.png')).astype('uint8')

            # Put the board in the center vertically
            board_margin = int((clip_size[1] - clip_size[0]) / 2)

            # Start a new frame for this move
            move_frame = (numpy.tile((0,0,0,0), clip_size[0]*clip_size[1])
                       .reshape(clip_size[1], clip_size[0], 4)
                       .astype('uint8'))

            # Project the board onto the frame
            move_frame[board_margin:clip_size[1] - board_margin, 0: clip_size[0]] = board_ndarray


            # Create a PIL ImageDraw object
            font_path = 'C:\\Windows\\Fonts\\cour.ttf'
            pil_image = PILImage.fromarray(move_frame)
            pil_font = PILImageFont.truetype(font_path, size=40)
            draw = PILImageDraw.Draw(pil_image)

            # Add the Player name and rating for Black
            text = f"{game.tag_pairs['Black']} ({game.tag_pairs['BlackElo']})"
            draw.text(fill=(255,255,255,255),
                      font=pil_font,
                      xy=(0,370),
                      text=text)


            # Add the Player name and rating for White
            text = f"{game.tag_pairs['White']} ({game.tag_pairs['WhiteElo']})"
            draw.text(fill=(255,255,255,255),
                      font=pil_font,
                      xy=(0,1500),
                      text=text)

            move_frame = numpy.array(pil_image)
            # Create all the necessary frames for this move
            for _ in range(self.fps * chess_move_duration):
                frames.append(move_frame)

        self.set_video_frames(frames)