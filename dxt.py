import pyautogui as p
import time

p.PAUSE = 2.5

def move_mouse():
	p.moveTo(100, 100, duration=0.1)

def choose_a():
	move_mouse()
    a_coo = p.locateOnScreen('A.png')
    p.click(a_coo[0] + 5, a_coo[1] + 5)


def continue_study():
	move_mouse()
    continue_study_coo = p.locateOnScreen('goon.png')
    if continue_study_coo:
        p.click(continue_study_coo[0], continue_study_coo[1])


while 1 > 0:
    print('运行中')
    move_mouse()
    submit_btn_coordinates = p.locateOnScreen('submit.png')
    if submit_btn_coordinates:  # 有提交按键
        p.click(submit_btn_coordinates[0] + 10, submit_btn_coordinates[1] + 10)
        move_mouse()
        choose_answer_notice_coo = p.locateOnScreen('selectanswer.png')
        if choose_answer_notice_coo:  # 未选择答案，需要选择
            p.press('space')
            choose_a()
        else:
            continue_study()
    else:
        continue_study()
    print('等待10秒')
    for i in range(1, 10):
        print(i)
        time.sleep(1)
