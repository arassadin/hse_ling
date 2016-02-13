import os

from corpus import text_unit, corpus

DATA_DIR = os.path.abspath(os.path.join(os.path.curdir, 'data'))
DATA_EXT = '*.txt'


def main():
    corp = corpus()

    # rg_98 = text_unit(dates=[1997, 1998, 1999], sources=['RG'])
    # rg_98.read(DATA_DIR, '98', 'rg' + DATA_EXT)
    # rg_98.get_lemm()
    # corp.add(rg_98)

    # rg_01 = text_unit(dates=[2000, 2001, 2002], sources=['RG'])
    # rg_01.read(DATA_DIR, '01', 'rg' + DATA_EXT)
    # rg_01.get_lemm()
    # corp.add(rg_01)

    # rg_04 = text_unit(dates=[2003, 2004, 2005], sources=['RG'])
    # rg_04.read(DATA_DIR, '04', 'rg' + DATA_EXT)
    # rg_04.get_lemm()
    # corp.add(rg_04)

    # rg_16 = text_unit(dates=[2016], sources=['RG'])
    # rg_16.read(DATA_DIR, '16', 'rg' + DATA_EXT)
    # rg_16.get_lemm()
    # corp.add(rg_16)

    # nv_98 = text_unit(dates=[1997, 1998, 1999], sources=['Novaya'])
    # nv_98.read(DATA_DIR, '98', 'nv' + DATA_EXT)
    # nv_98.get_lemm()
    # corp.add(nv_98)

    # nv_01 = text_unit(dates=[2000, 2001, 2002], sources=['Novaya'])
    # nv_01.read(DATA_DIR, '01', 'nv' + DATA_EXT)
    # nv_01.get_lemm()
    # corp.add(nv_01)

    # nv_04 = text_unit(dates=[2003, 2004, 2005], sources=['Novaya'])
    # nv_04.read(DATA_DIR, '04', 'nv' + DATA_EXT)
    # nv_04.get_lemm()
    # corp.add(nv_04)

    # nv_16 = text_unit(dates=[2016], sources=['Novaya'])
    # nv_16.read(DATA_DIR, '16', 'nv' + DATA_EXT)
    # nv_16.get_lemm()
    # corp.add(nv_16)

    # corp.dump(path='dumps/corp.dump')

    # corp.load('dumps/corp.dump')

    # corp.get_info()

    # lemmas = corp.get_lemm(sources='RG')
    # corp.add_stat(name='RG_lemmas', value=lemmas, descr='RG lemmas')

    # lemmas = corp.get_lemm(sources='Novaya')
    # corp.add_stat(name='Novaya_lemmas', value=lemmas, descr='Novaya lemmas')

    # lemmas = corp.get_lemm(period=[1997, 1999])
    # corp.add_stat(
    #     name='98_lemmas', value=lemmas, descr='Lemmas from 1997 till 1999')

    # lemmas = corp.get_lemm(period=[2000, 2002])
    # corp.add_stat(
    #     name='01_lemmas', value=lemmas, descr='Lemmas from 2000 till 2002')

    # lemmas = corp.get_lemm(period=[2003, 2005])
    # corp.add_stat(
    #     name='04_lemmas', value=lemmas, descr='Lemmas from 2003 till 2005')

    # lemmas = corp.get_lemm(period=[2016, 2016])
    # corp.add_stat(
    #     name='16_lemmas', value=lemmas, descr='Lemmas from 2016')

    # corp.dump('dumps/corp_multy-lemm.dump')

    corp.load('dumps/corp_multy-lemm.dump')

    corp.get_info()

if __name__ == "__main__":
    main()
