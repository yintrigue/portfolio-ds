"""Provide functions to enable SmartSnake's brains. As as the current version, functions
included in this module are built for convenience rather than reuseability/extensibility. Lots of
shortcuts are there just to quickly make things work.
"""
import numpy as np
import pandas as pd
from snaky import SmartSnaky

def enable_brain_v1(
            snake: SmartSnaky,
            build_training_data: bool = True,
            do_training: bool = False,
            auto_play: bool = True) -> None:
    """Logistic Regression + Simple Vision (i.e. able to see obstacles...)
    """
    # generate data
    if build_training_data:
        snake.simulate(n_game=10000, csv='trainset_random.csv', vision_mode='simple')

    # training
    if do_training:
        snake.train(
                brain_model='logi',
                vision='simple',
                csv='trainset_random.csv',
                epoch=20,
                batch_size=32,
                weights_save_path='./brain_models/brain_v1_lr.h5')

        # testing model
        snake.evaluate(
                brain_model='logi',
                vision='simple',
                model_weights='./brain_models/brain_v1_lr.h5',
                test_csv='trainset_random.csv',
                sig_thd=0.5)

    # predict & replay
    if auto_play:
        snake.autoplay(
                n_move=100,
                brain_model='logi',
                vision = 'simple',
                model_weights='./brain_models/brain_v1_lr.h5',
                output_csv='autoplay.csv',
                replay_fps=5)

def enable_brain_v2(
            snake: SmartSnaky,
            build_training_data: bool = True,
            do_training: bool = True,
            auto_play: bool = True) -> None:
    """Neural Net + Simple Vision (i.e. able to see obstacles...)
    """
    # generate data
    if build_training_data:
        snake.simulate(n_game=10000, csv='trainset_random.csv', vision_mode='simple')

    # training
    if do_training:
        snake.train(
                brain_model='neural_net',
                vision='simple',
                csv='trainset_random.csv',
                epoch=20,
                batch_size=32,
                weights_save_path='./brain_models/brain_v2_nn.h5')

        # testing model
        snake.evaluate(
                brain_model='neural_net',
                vision='simple',
                model_weights='./brain_models/brain_v2_nn.h5',
                test_csv='trainset_random.csv',
                sig_thd=0.5)

    # predict & replay
    if auto_play:
        snake.autoplay(
                n_move=100,
                brain_model='neural_net',
                vision = 'simple',
                model_weights='./brain_models/brain_v2_nn.h5',
                output_csv='autoplay.csv',
                replay_fps=5)

def enable_brain_v3(
            snake: SmartSnaky,
            build_training_data: bool = True,
            do_training: bool = True,
            auto_play: bool = True) -> None:
    """Neural Net + Advanced Vision (i.e. able to see obstacles + apples...)
    """
    # generate data
    if build_training_data:
        snake.simulate(n_game=10000, csv='trainset_random.csv', vision_mode='advanced')

    # training
    if do_training:
        snake.train(
                brain_model='neural_net',
                vision='advanced',
                csv='trainset_random.csv',
                epoch=30,
                batch_size=32,
                weights_save_path='./brain_models/brain_v3_nn.h5')

        # testing model
        snake.evaluate(
                brain_model='neural_net',
                vision='advanced',
                model_weights='./brain_models/brain_v3_nn.h5',
                test_csv='trainset_random.csv',
                sig_thd=0.5)

    # predict & replay
    if auto_play:
        snake.autoplay(
                n_move=1000,
                brain_model='neural_net',
                vision = 'advanced',
                model_weights='./brain_models/brain_v3_nn.h5',
                output_csv='autoplay.csv',
                replay_fps=24)

def enable_brain_v4(
            snake: SmartSnaky,
            build_training_data: bool = True,
            do_training: bool = True,
            auto_play: bool = True) -> None:
    """Neural Net + Expert Vision (i.e. able to see obstacles + apples + closed regions...)
    """
    # build traing data using brain_v3
    if build_training_data:
        build_train_data_using_brain_v3(snake=snake, do_training=True)

    # training
    if do_training:
        snake.train(
                brain_model='neural_net',
                vision='expert',
                csv='train_v3_random_combined.csv',
                epoch=30,
                batch_size=32,
                weights_save_path='./brain_models/brain_v4_nn.h5')

        # testing model
        snake.evaluate(
                brain_model='neural_net',
                vision='expert',
                model_weights='./brain_models/brain_v4_nn.h5',
                test_csv='train_v3_random_combined.csv',
                sig_thd=0.5)

    # predict & replay
    if auto_play:
        snake.autoplay(
                n_move=1000,
                brain_model='neural_net',
                vision = 'expert',
                model_weights='./brain_models/brain_v4_nn.h5',
                output_csv='autoplay.csv',
                replay_fps=24,
                verbose=1)

def build_train_data_using_brain_v3(
                        snake: SmartSnaky,
                        do_training: bool = True) -> None:
    """Generate training data using brain v3. The goal is to produce enough
    examples that cover the closed region scenarios.
    """
    N_GAME_RANDOM = 10000
    N_GAME_V3 = 500
    N_MOVE_V3 = 1000

    # training brain_v3
    if do_training:
        print("Training brain model v3...")
        snake.simulate(n_game=N_GAME_RANDOM, csv='trainset_random.csv', vision_mode='advanced')
        snake.train(
                brain_model='neural_net',
                vision='advanced',
                csv='trainset_random.csv',
                epoch=20,
                batch_size=32,
                weights_save_path='./brain_models/brain_v3_nn.h5')

        # testing model
        snake.evaluate(
                brain_model='neural_net',
                vision='advanced',
                model_weights='./brain_models/brain_v3_nn.h5',
                test_csv='trainset_random.csv',
                sig_thd=0.5)

    # build new training data
    print("Generating training data using brain model v3...")
    snake.autoplay(
            n_game=N_GAME_V3,
            n_move=N_MOVE_V3,
            brain_model='neural_net',
            vision = 'advanced',
            model_weights='./brain_models/brain_v3_nn.h5',
            output_csv='trainset_by_model3.csv',
            replay=False,
            verbose=2)

    # combined v3 & random data
    print("Combining v3 & random data...")
    df1 = pd.read_csv('trainset_random.csv', dtype={
                                            'vision': np.object,
                                            'vision_simple': np.object,
                                            'vision_advanced': np.object,
                                            'vision_expert': np.object,
                                            'vision_new': np.object})
    df2 = pd.read_csv('train_by_v3.csv', dtype={
                                            'vision': np.object,
                                            'vision_simple': np.object,
                                            'vision_advanced': np.object,
                                            'vision_expert': np.object,
                                            'vision_new': np.object})
    df1.loc[:,'game_id'] += 1000000
    df2.loc[:,'game_id'] += 2000000
    df = pd.concat([df1, df2], ignore_index=True)
    df.to_csv('trainset_by_model3_concat_random.csv', index=False)
    print("Traning data for model v4 have been built!")

def replay(
        snake: SmartSnaky,
        game_id: int = 0,
        csv: str = 'train.csv',
        fps = 12,
        show_ending: bool = False) -> None:
    snake.replay(
            game_id=game_id,
            fps=fps,
            csv=csv,
            ending=show_ending,
            print_data=True)
