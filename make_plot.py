# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 21:27:57 2018

@author: user
"""

def make_plot():

    import os
    file_path = '/static/'
    os.chdir('C:\\Users\\user\\Desktop\\hw1\\static')
    from pymongo import MongoClient
    from urllib.parse import quote_plus
    from matplotlib import pyplot as plt
    import numpy as np
    import matplotlib.colors as col
    import matplotlib.cm as cm
    import collections
    
    return_data = dict()
    """ 連接MongoDB """
    uri = "mongodb://%s:%s@%s" % (quote_plus('Mao'), quote_plus('7711'), quote_plus('127.0.0.1'))
    client = MongoClient(uri)
    cllct = client.admin.homicide
    case_count = cllct.find({}).count()
    
#    result = cllct.find({})
#    for data in result:
#        pass
#    data = []
#    for n, i in enumerate(cllct.find({})):
#        data.append(i)    
    """統計圖表"""
    """ 案件是否解決 """
    
    y = cllct.find({'Crime Solved':'Yes'}).count()
    n = case_count - y
    
    plt.clf()
    plt.figure(figsize=(7,7))
    labels = ['Solved', 'Unsolved']
    sizes = [y, n]
    colors = ['yellowgreen', 'red']
    explode = (0,0)
    patches,text1,text2 = plt.pie(sizes,explode=explode,labels=labels,colors=colors, autopct = '%3.2f%%',
                                  shadow = False, startangle =90, pctdistance = 0.6)
    for i in range(2):
        text1[i].set_fontsize(14)
        text2[i].set_fontsize(14)
    plt.axis('equal')
    plt.title('Crime Solved or not')
    plt.savefig("sloved.png", dpi=120)
#   plt.show()

    return_data.update({'Crime Solved or not': [file_path + "sloved.png", '']})

    """ 年齡 """
    
    victim_age = {}
    perpetrator_age = {}
    for data in cllct.find({}):
        if data['Victim Age'] == '998':
            continue
        if int(data['Victim Age']) not in victim_age.keys():
            victim_age.update({int(data['Victim Age']): 0})
        else:
            victim_age[int(data['Victim Age'])] -= 1
        if data['Perpetrator Age'] == ' ':
            continue
        if int(data['Perpetrator Age']) not in perpetrator_age.keys():
            perpetrator_age.update({int(data['Perpetrator Age']): 0})
        else:
            perpetrator_age[int(data['Perpetrator Age'])] += 1
    #perpetrator_age.pop(' ', None)
    #victim_age.pop('0', None)
    perpetrator_age.pop(0, None)
    victim_age = collections.OrderedDict(sorted(victim_age.items()))
    perpetrator_age = collections.OrderedDict(sorted(perpetrator_age.items()))
    
    plt.clf()
    plt.figure(figsize=(10,5))
    plt.bar(victim_age.keys(), victim_age.values(), label = 'Victim', alpha = 0.8)
    plt.bar(perpetrator_age.keys(), perpetrator_age.values(), label = 'Perpetrator', alpha = 0.8)
    plt.legend(loc="upper right")
    plt.xticks(np.arange(0, 101, step=5))
    plt.grid()
    plt.ylabel('Count', fontsize=14)
    plt.xlabel('Age', fontsize=14)
    plt.title('Age of Victim and Perpetrator')
    plt.savefig("age.png", dpi=120, bbox_inches="tight")
    # plt.show()
	
    return_data.update({'Age of Victim and Perpetrator': [file_path + "age.png", '']})

    """ 被害人種族和性別 """
    
    race = ['White', 'Black', 'Asian/Pacific Islander', 'Native American/Alaska Native', 'Unknown']
    n = np.arange(len(race))
    m_func = lambda attr: cllct.find({'Victim Race':attr, 'Victim Sex':'Male'}).count()
    f_func = lambda attr: cllct.find({'Victim Race':attr, 'Victim Sex':'Female'}).count()*(-1)
    m = list(map(m_func, race))
    f = list(map(f_func, race))
    
    plt.clf()
    plt.figure(figsize=(8, 5))
    race = ['White', 'Black', 'Asian /\nPacific Islander', 'Native American /\nAlaska Native', 'Unknown']
    plt.bar(n, m, color = 'LightBlue', label = 'Male', tick_label = race)
    plt.bar(n, f, color = 'Pink', label = 'Female')
    plt.legend(loc="upper right")
    for x, y in zip(n, m):
        plt.text(x, y, y, ha='center', va='bottom')
    for x, y in zip(n, f):
        plt.text(x, y, -y, ha='center', va='top')
    plt.xlabel('Victim Race', fontsize=14)
    plt.ylabel('Victim count', fontsize=14)
    plt.title('Sex and Race of Victim')
    plt.grid()
    plt.savefig("victim_race.png", dpi=120, bbox_inches="tight")
#    plt.show()
	
    return_data.update({'Sex and Race of Victim': [file_path + "victim_race.png", '']})
       
    """ 加害人種族和性別 """
    
    race = ['White', 'Black', 'Asian/Pacific Islander', 'Native American/Alaska Native', 'Unknown']
    n = np.arange(len(race))
    m_func = lambda attr: cllct.find({'Perpetrator Race':attr, 'Perpetrator Sex':'Male'}).count()
    f_func = lambda attr: cllct.find({'Perpetrator Race':attr, 'Perpetrator Sex':'Female'}).count()*(-1)
    m = list(map(m_func, race))
    f = list(map(f_func, race))
    
    plt.clf()
    plt.figure(figsize=(8, 5))
    race = ['White', 'Black', 'Asian /\nPacific Islander', 'Native American /\nAlaska Native', 'Unknown']
    plt.bar(n, m, color = 'LightBlue', label = 'Male', tick_label = race)
    plt.bar(n, f, color = 'Pink', label = 'Female')
    plt.legend(loc="upper right")
    for x, y in zip(n, m):
        plt.text(x, y, y, ha='center', va='bottom')
    for x, y in zip(n, f):
        plt.text(x, y, -y, ha='center', va='top')
    plt.xlabel('Perpetrator Race', fontsize=14)
    plt.ylabel('Perpetrators Count', fontsize=14)
    plt.title('Sex and Race of Perpetrator')
    plt.grid()
    plt.savefig("perpetrator_race.png", dpi=120, bbox_inches="tight")
#    plt.show()
    
    return_data.update({'Sex and Race of Perpetrator': [file_path + "perpetrator_race.png", '']})

    
    """ 被害人和加害人關系 """
    
    relation_type = ['Employee', 'Family', 'Brother', 'Ex-Wife', 'Neighbor', 'Boyfriend', 'Friend', 'Boyfriend/Girlfriend', 'Employer', 'Stepson', 'Girlfriend', 'Stepfather', 'Common-Law Husband', 'Daughter', 'Wife', 'Son', 'Stepdaughter', 'Ex-Husband', 'Husband', 'Father', 'Sister', 'Stepmother', 'Common-Law Wife', 'Unknown', 'Acquaintance', 'Mother', 'Stranger', 'In-Law']
    func = lambda relation: cllct.find({'Relationship':relation}).count()
    count = list(map(func, relation_type))
    mean_values = range(4,32)
    cmap1 = cm.ScalarMappable(col.Normalize(min(mean_values), max(mean_values), cm.hot))
    color_list = cmap1.to_rgba(mean_values)
    
    plt.clf()
    plt.figure(figsize=(8,8))
    y_pos = np.arange(len(count))
    y_pos = [x for x in y_pos]
    plt.yticks(y_pos, relation_type, fontsize=10)
    plt.barh(y_pos, count, align='center', color=color_list, alpha=0.8)
    plt.xscale('log')
    for x, y in zip(range(len(relation_type)), count):
        plt.text(y+10, x, y, ha='left', va='center', fontsize=10)
    plt.xlabel('Count', fontsize=14)
    plt.ylabel('Relationship', fontsize=14)
    plt.title('Relation between Victim and Perpetrator')
    plt.grid()
    plt.savefig("relation.png", dpi=120, bbox_inches="tight")
#    plt.show()
    
    return_data.update({'Relation between Victim and Perpetrator': [file_path + "relation.png", '']})
    
    """ 使用的武器 """
    
    weapon_kind = ['Fall', 'Shotgun', 'Unknown', 'Suffocation', 'Strangulation', 'Explosives', 'Blunt Object', 'Gun', 'Fire', 'Knife', 'Firearm', 'Drugs', 'Rifle', 'Drowning', 'Poison', 'Handgun']
    year = ['2010', '2011', '2012', '2013', '2014']
    mean_values = range(6,22, 1)
    cmap1 = cm.ScalarMappable(col.Normalize(min(mean_values), max(mean_values), cm.hot))
    color_list = cmap1.to_rgba(mean_values)
    n = np.arange(len(year))
    count = []
    for w in weapon_kind:
        temp = []
        for y in year:
            temp.append(cllct.find({'Weapon':w, 'Year':y}).count())
        count.append(temp)
    add_count = []
    for i in np.arange(16):
        temp = count[i]
        for j in np.arange(i+1, len(weapon_kind)):
            temp = np.add(temp, count[j])
        add_count.append(temp)
        # 累加
    plt.clf()
    plt.figure(figsize=(8,5))
    for i in range(len(weapon_kind)):
        if i == 0:
            plt.bar(n, add_count[i], color = color_list[i], label = weapon_kind[i], tick_label = year, alpha=0.8)
        else:
            plt.bar(n, add_count[i], color = color_list[i], label = weapon_kind[i], alpha=0.8)
    plt.legend(loc='center right', borderaxespad=-11)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.grid()
    plt.title('Used Weapon')
    plt.savefig("weapon.png", dpi=120, bbox_inches="tight")
#    plt.show()
    
    return_data.update({'Used Weapon': [file_path + "weapon.png", '']})
    
    """ 發生地區 """
    
    #result = cllct.find({})
    #state = set()
    #for data in result:
    #    state.update({data['State']})
    #state = list(state)
    state = ['Kansas', 'North Dakota', 'Pennsylvania', 'Utah', 'Alaska', 'Missouri', 'Delaware', 'Mississippi', 'California', 'Tennessee', 'Hawaii', 'New Jersey', 'New Hampshire', 'Rhodes Island', 'Vermont', 'Maine', 'West Virginia', 'New York', 'Wisconsin', 'Iowa', 'Texas', 'Arkansas', 'Illinois', 'Maryland', 'Alabama', 'Connecticut', 'Montana', 'Indiana', 'District of Columbia', 'South Dakota', 'Florida', 'South Carolina', 'Arizona', 'Kentucky', 'Louisiana', 'Michigan', 'Minnesota', 'New Mexico', 'North Carolina', 'Virginia', 'Nebraska', 'Nevada', 'Oklahoma', 'Massachusetts', 'Washington', 'Georgia', 'Idaho', 'Ohio', 'Colorado', 'Oregon', 'Wyoming']
    year = ['2010', '2011', '2012', '2013', '2014']
    mean_values = range(4,55, 1)
    cmap1 = cm.ScalarMappable(col.Normalize(min(mean_values), max(mean_values), cm.hot))
    color_list = cmap1.to_rgba(mean_values)
    
    count = []
    for s in state:
        temp = []
        for y in year:
            temp.append(cllct.find({'State':s, 'Year':y}).count())
        count.append(temp)
    add_count = []
    for i in np.arange(len(state)):
        temp = count[i]
        for j in np.arange(i+1, len(state)):
            temp = np.add(temp, count[j])
        add_count.append(temp)
    
    plt.clf()
    plt.figure(figsize=(8,5))
    for i in range(len(state)):
        if i == 0:
            plt.bar(n, add_count[i], color = color_list[i], label = state[i], tick_label = year, alpha=0.8)
        else:
            plt.bar(n, add_count[i], color = color_list[i], label = state[i], alpha=0.8)
    plt.legend(loc='center right', borderaxespad=-40, ncol=3)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.grid()
    plt.title('State')
    plt.savefig("state.png", dpi=120, bbox_inches="tight")
#   plt.show()
    
    return_data.update({'State': [file_path + "state.png", '']})
    
    return return_data