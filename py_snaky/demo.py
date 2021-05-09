import sys
sys.path.append('./src')
from snaky import Snaky, SmartSnaky
import brains

# play, autoplay, replay
MODE = 'autoplay'
# brains.enable_brain_v1: Logistic Regression + Simple Vision (i.e. able to see obstacles)
# brains.enable_brain_v2: Neural Net + Simple Vision (i.e. able to see obstacles)
# brains.enable_brain_v3: Neural Net + Advanced Vision (i.e. able to see obstacles + apples)
# brains.enable_brain_v4: Neural Net + Expert Vision (i.e. able to see obstacles + apples + closed regions...)
BRAIN_FUNC = brains.enable_brain_v3
DO_TRAINING = False
BUILD_TRAINING_DATA = False

snake = SmartSnaky(
            snake_sprite_sheet_url='assets/skin_grey/sprite.png',
            apple_sprite_url='assets/skin_grey/apple.png',
            font_url='assets/retro_computer.ttf',
            board_color=(250, 250, 250))

if MODE == 'replay':
    # replay a specific historical game
    brains.replay(snake=snake, csv='autoplay.csv', game_id=0, show_ending=False)
elif MODE == 'autoplay':
    # build brain & autoplay using the brain
    BRAIN_FUNC(
        snake=snake,
        build_training_data=BUILD_TRAINING_DATA,
        do_training=DO_TRAINING,
        auto_play=True)
else:
    # play the game manually
    snake.play()
