#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Client

c = Client.Client_Class()
print(c.get_ans("http://www.ariel.ac.il/" , "דיזיין"))
print(c.get_ans("http://www.ariel.ac.il/" , "מידע אישי"))
print(c.get_ans("http://www.ariel.ac.il/" , "מינהלה"))