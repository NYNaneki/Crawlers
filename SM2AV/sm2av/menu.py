from . import smtools
from . import sm2av


# 考虑新增一个输出结果到本地文本文件的功能
def get_input():
    """获取用户输入"""

    while True:
        try:
            print('输入导入SM号的方式：')
            print('1. 从B站视频简介导入（av or bv 号）')
            print('2. 从N站用户投稿导入（输入N站用户ID）')
            print('3. 从本地文件导入（输入文件名）')
            print('4. 从字符串导入（每个关键字之间用,隔开)')
            print('5. 退出程序')

            inp = int(input('请根据序号输入: '))

            if inp == 5:
                input('输入回车退出...')
                exit()
            elif inp < 1 or inp > 5:
                print('无效的输入。')
            else:
                print()
                return inp
        except Exception as error:
            print(f'输入异常: {error}')


async def get_from_desc(session):
    """封装的从B站简介获取sm号方法"""

    inp = input('输入av/bv: ')

    if inp.upper().startswith('AV'):
        inp = inp[2:]

    sm_list = await smtools.get_sm_from_desc(session, inp)

    return sm_list


async def get_from_nico(session):
    """封装的从N站用户ID获取sm号方法

    起始页和终止页是可选项，默认只会获取一页数据，程序不对页数的正确性进行检查"""

    while True:
        inplist = input('输入N站用户ID [起始页] [终止页]: ').split(' ')
        begin = end = 1

        if 1 <= len(inplist) <= 3:
            uid = inplist[0]

            if len(inplist) == 2:
                begin = end = int(inplist[1])
            elif len(inplist) == 3:
                begin = int(inplist[1])
                end = int(inplist[2])

            break
        elif len(inplist) > 3:
            print('无效的输入。')

    sm_list = await smtools.get_sm_from_nico(uid, begin, end)

    return sm_list


async def get_from_file(unused):
    """封装的从文件获取sm号方法
    这里的unused参数纯粹是为了占位置"""

    inp = input('输入文件名: ')

    sm_list = await smtools.get_sm_from_file(inp)

    return sm_list


async def get_from_text(unused):
    """封装的从文本获取sm号方法
    这里的unused参数纯粹是为了占位置"""

    inp = input('输入关键字: ')

    sm_list = await smtools.get_sm_from_text(inp)

    return sm_list


async def run():
    """封装的启动检索方法"""

    switch = {
        1: get_from_desc,
        2: get_from_nico,
        3: get_from_file,
        4: get_from_text
    }

    async with await smtools.get_session() as session:
        while True:
            filename = input('输入输出文件名(可选): ')
            file_obj = None

            if filename:
                try:
                    file_obj = open(filename, 'a', encoding='utf-8')
                except IOError as error:
                    print(f'打开文件失败: {error}')

            print()

            sm_list = await switch[get_input()](session)
            await sm2av.SM2AV(sm_list, session, file_obj).search(coro_num=5)

            if file_obj:
                file_obj.close()
                print(f'结果已输出到: {filename}')

            print('*' * 40)
