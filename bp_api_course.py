# -*- coding: utf8 -*-

import os
import numpy as np
from flask import Blueprint, render_template, abort, request, jsonify

pages_api_course = Blueprint("pages_api_course", __name__, template_folder="templates")

@pages_api_course.route("/api/course_cvpredict", methods=['GET','POST'])
def api_course_cvpredict():
    if request.method=='GET':
        return render_template('api/course_cvpredict.html')

    no_students = int(request.form.get('no_students'))
    no_courseitems = int(request.form.get('no_courseitems'))
    no_duration = int(request.form.get('no_duration'))
    no_enroll = int(request.form.get('no_enroll'))
    no_exam = int(request.form.get('no_exam'))
    no_learnci_per_day = float(request.form.get('no_learnci_per_day'))
    learnstates,res = stu_simulation(no_students ,no_enroll, no_duration, no_exam, no_courseitems, no_learnci_per_day)
    return jsonify(res)

def stu_simulation(no_students, no_enroll, no_duration, no_exam, no_courseitems, no_learnci_per_day):

    curstuno = 0    
    learnstates = {} 
    res = {}
    vv_perday = [0 for i in range(no_duration)]
    enroll_ratio  = [] 
    utility_uv = [0 for i in range(no_courseitems)]
    utility_pv = [0 for i in range(no_courseitems)]
        
    for t in range(no_duration):
        if curstuno<no_students:
            for i in range(no_enroll):
                learnstates[curstuno] = {'learn_times':no_learnci_per_day,'start_date':t+1,'p_sd':(no_duration-t)*1.0/no_duration}
                curstuno += 1
                if curstuno>=no_students:
                    break
             
        for i in range(curstuno):
            prob = (learnstates[i]['learn_times']/no_courseitems)*(learnstates[i]['p_sd'])*(t*1.0/no_exam)
            apple = np.random.random()
            if apple <= prob:
                learnstates[i]['learn_times'] += no_learnci_per_day
            
        vv_perday[t] = int(sum([learnstates[i]['learn_times'] for i in range(curstuno)]))       
        
    ltimes = [int(learnstates[i]['learn_times']) for i in range(no_students)]
    ltimes_ordered = ltimes[:]
    ltimes_ordered.sort(reverse=True)
    
    for l in ltimes:
        if int(l) <= no_courseitems:
            enroll_ratio.append(l*1.0/no_courseitems)
            for i in range(int(l)):
                utility_pv[i] = utility_pv[i] + 1
                utility_uv[i] =  utility_uv[i] + 1
        else:
            enroll_ratio.append(1)
            for i in range(no_courseitems):
                utility_uv[i] =  utility_uv[i] + 1          
            ln = l / no_courseitems
            for i in range(ln):
                for j in range(no_courseitems):
                    utility_pv[j] = utility_pv[j] + 1
            for i in range(int(l) % no_courseitems):
                utility_pv[i] = utility_pv[i] + 1
               
    utility_ratio = [ p*1.0/no_students for p in utility_pv]
    
    en_mean = round(sum(enroll_ratio)/no_students,4)
    en_median = round(get_median(enroll_ratio),4)
    ut_mean = round(sum(utility_ratio)/no_courseitems,4)
    ut_median = round(get_median(utility_ratio),4)
                                      
    bins = range(0,201,9)    
    histed_ltimes = list(np.histogram(ltimes,bins=bins))
    histed_ltimes[0] = histed_ltimes[0].tolist()
    histed_ltimes[1] = histed_ltimes[1].tolist()
    
    vv_ratio_perday = [v*1.0/(no_courseitems*no_students) for v in vv_perday]
    
    res['vv_origin'] = ltimes
    res['vv_ordered'] = ltimes_ordered
    res['vv_histed'] = histed_ltimes
    res['vv_total'] = int(sum(ltimes))
    res['en_mean'] = en_mean
    res['en_median'] = en_median
    res['ut_mean'] = ut_mean
    res['ut_median'] = ut_median
    res['ut_pv'] = utility_pv
    res['vv_perday'] = vv_perday
    res['vv_ratio_perday'] = vv_ratio_perday    
    
    return learnstates,res

def get_median(data):
    data.sort()
    half = len(data) / 2
    return (data[half] + data[~half]) / 2

    
