import os
from cv2 import imread


def ImgInit():
    startIcon = {}
    for filename in os.listdir(r'pic/leftClick/start'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            startIcon[filename] = (imread('pic/leftClick/start/' + filename))
    for filename in os.listdir(r'pic/leftClick/end'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            startIcon[filename] = (imread('pic/leftClick/end/' + filename))
    startIcon['threshold'] = 0.21
    startIcon['name'] = 'start'

    ChooseHeroIcon = {}
    for filename in os.listdir(r'pic/leftClick/heros'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            ChooseHeroIcon[filename] = (
                imread('pic/leftClick/heros/' + filename))
    ChooseHeroIcon['threshold'] = 0.21
    ChooseHeroIcon['name'] = 'ChooseHero'

    rightClickIcon = {}
    for filename in os.listdir(r'pic/rightClick'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            rightClickIcon[filename] = (imread('pic/rightClick/' + filename))
    rightClickIcon['threshold'] = 0.13
    rightClickIcon['name'] = 'rightClick'

    leftClickDelayIcon = {}
    for filename in os.listdir(r'pic/leftClickDelay'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            leftClickDelayIcon[filename] = (
                imread('pic/leftClickDelay/' + filename))
    leftClickDelayIcon['threshold'] = 0.3
    leftClickDelayIcon['name'] = 'leftClickDelay'

    judgeHeroIcon = {}
    for filename in os.listdir(r'pic/judge'):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            judgeHeroIcon[filename] = (imread('pic/judge/' + filename))
    judgeHeroIcon['threshold'] = 0.15
    judgeHeroIcon['name'] = 'judgeHero'

    # 重写为字典，编号有点记不住
    flags = {}
    flags['in_game_flag'] = imread('pic/flags/in_game_flag.png')
    flags['in_game_flag2'] = imread('pic/flags/in_game_flag2.png')
    flags['heroInfoFlag'] = imread('pic/flags/heroInfoFlag.png')
    flags['fighting_flag'] = imread('pic/flags/fighting_flag.png')
    flags['fighting_flag2'] = imread('pic/flags/fighting_flag2.png')
    flags['fighting_flag3'] = imread('pic/flags/fighting_flag3.png')
    flags['fighting_flag4'] = imread('pic/flags/fighting_flag4.png')
    flags['threshold'] = 0.21
    flags['name'] = 'flags'

    return startIcon, ChooseHeroIcon, rightClickIcon, leftClickDelayIcon, judgeHeroIcon, flags
