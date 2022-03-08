# for i, correct_code in enumerate(correct_codes):
    # for input in inputs:
    #     input.clear()

    # print(i)
    # #print(f'loop {full_loops}')
    # innerHTML = unescape(correct_code.get_attribute('innerHTML')).split()

    # correct_answers = [ans for ans in innerHTML if ans not in empty_ans]

    # print(correct_answers)
    # print()

    # if len(correct_answers) == len(inputs):
    #     if not full_loops < len(correct_answers):
    #         for i, correct_ans in enumerate(correct_answers):
    #             for ans in empty_ans:
    #                 if ans in correct_ans:
    #                     correct_answers[i] = correct_ans[
    #                                             correct_ans.index(ans)+len(ans):
    #                                         ]
    #                     print(correct_answers[i])
    #     for input, ans in zip(inputs, correct_answers):
    #             input.send_keys(ans)

    # elif len(inputs) == 1:
    #     ans = ' '.join(correct_answers)
    #     input.send_keys(ans)

    # time.sleep(0.5)
    # driver.find_element(By.ID, os.getenv('submit_ans')).click()
    # driver.find_element(By.ID, os.getenv('submit_ans')).click()

    # if driver.current_url != exercise_url:
    #     full_loops = 0
    #     break
    
    # full_loops += 1