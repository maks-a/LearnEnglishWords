#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import myle.singleton
import myle.app


def run():
    me = myle.singleton.SingleInstance()
    me
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    myle.app.App()

if __name__ == '__main__':
    run()
