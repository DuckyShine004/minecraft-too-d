import pygame

from src.block.block_type import BlockType
from src.block.block_path import BlockPath

from src.utils.vector import Position
from src.utils.rounding import round_to_nearest_multiple

from typing import Dict, List, Tuple

from src.constants import BLOCK_SIZE, CHUNK_SIZE


class BlockManager:
    """
    The BlockManager class automates block related processes with the help of essential
    functions.

    Attributes:
    __blocks - a dictionary that keeps a track on all block positions which have been rendered before.
    __rects - a list that stores the block hitboxes for the loaded chunks.
    __txtrs - a list that stores the block textures for the loaded chunks.
    """

    def __init__(self) -> None:
        self.__blocks = dict()
        self.__rects = []
        self.__txtrs = []

    @staticmethod
    def get_offset_block_position(block_rect, camera_offset):
        offset_block_x = block_rect.x - camera_offset.x
        offset_block_y = block_rect.y - camera_offset.y

        return (offset_block_x, offset_block_y)

    @staticmethod
    def get_local_block_position(block_rect):
        local_block_x = block_rect.x // BLOCK_SIZE
        local_block_y = block_rect.y // BLOCK_SIZE

        return (local_block_x, local_block_y)

    @staticmethod
    def get_chunk_position(local_block_position):
        chunk_x = round_to_nearest_multiple(
            local_block_position[0], CHUNK_SIZE)
        chunk_y = round_to_nearest_multiple(
            local_block_position[1], CHUNK_SIZE)

        return (chunk_x, chunk_y)

    def get_block_rect(self, block_position: Tuple[int, int]) -> pygame.Rect:
        """
        Create a block hitbox for the given block position.

        Return the block hitbox for the given block position.

        Keywords:
        block_position - the passed position value of the given block's position.
        """

        global_block_x = block_position[0] * BLOCK_SIZE
        global_block_y = block_position[1] * BLOCK_SIZE

        global_block_position = (global_block_x, global_block_y)

        block_rect = pygame.Rect(
            *global_block_position, BLOCK_SIZE, BLOCK_SIZE)

        block_rect.topleft = global_block_position

        return block_rect

    def get_block_txtr(self, block_type: BlockType) -> pygame.Surface:
        """
        Create a block texture for the given block type.

        Return the block texture for the given block type.

        Keywords:
        block_type - the type of block we want to create a texture for.
        """

        block_path = BlockPath[block_type.name].value

        block_imge = pygame.image.load(block_path).convert()
        block_txtr = pygame.transform.scale(
            block_imge, (BLOCK_SIZE, BLOCK_SIZE))

        return block_txtr

    def get_block_rect_list(self) -> List[pygame.Rect]:
        """
        Get a list of all block hitboxes for the current loaded chunk position.

        Return all block hitboxes for the current loaded chunk positions.
        """

        return self.__rects

    def remove_block(self, block_position):
        del self.__blocks[block_position]

    def add_block(self, block_position, block_type):
        block_rect = self.get_block_rect(block_position)
        block_txtr = self.get_block_txtr(block_type)

        self.__blocks[block_position] = [block_txtr, block_rect]

    def update(self, block_data: Dict[Tuple[int, int], BlockType]) -> None:
        """
        Update

        Keywords:
        block_data -
        """

        for block_position, block_type in block_data.items():
            if block_type != BlockType.AIR:
                self.__txtrs.append(self.__blocks[block_position][0])
                self.__rects.append(self.__blocks[block_position][1])

    def display(self, screen: pygame.Surface, camera_offset: Position) -> None:
        """
        Display all block game objects to the screen.

        Keywords:
        screen - the surface that our game objects will be displayed onto.
        camera_offset - the camera offset ensures that the screen is automatically
        centered upon every player movement.
        """

        for block_rect, block_txtr in zip(self.__rects, self.__txtrs):
            offset_x = block_rect.x - camera_offset.x
            offset_y = block_rect.y - camera_offset.y

            screen.blit(block_txtr, (offset_x, offset_y))

        self.__rects.clear()
        self.__txtrs.clear()
