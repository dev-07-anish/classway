from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Class, Question, Answer, Enroll
from account.models import User

from .forms import ModelFormEditClass, ModelFormJoinClass, ModelFormNewClass, ModelFormAllotMarks, ModelFormAddQuestion, ModelFormAddAnswer


import string
import random
import json


from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def app_home(request):
    if 'logged_in_user' in request.session:
        return render(request, 'temp_app_classway/app_home.html')

    return render(request, 'temp_website/home.html')


def app_fresher(request):
    return render(request, 'temp_app_classway/app_fresher.html')


##############################################################################


##############################################################################


def app_available_class(request):
    user_email = request.session['logged_in_user']

    # fetching user id with the help of user email
    temp = User.objects.filter(email=user_email)
    for i in temp:
        user_id = i.id

    # fetching classes created by this user_id
    obj_user_classes = Class.objects.filter(class_admin=user_id)

    # fetching total user enrolled each classes
    obj_user_enrolls_count = Enroll.objects.all().count()

    # -------------------------

    # test = Enroll.objects.select_related(Class)
    # for i in test:
    #     print(i)

    # -------------------------

    if obj_user_classes:
        return render(request, 'temp_app_classway/app_available_class.html', {
            'created_class': obj_user_classes,
            'enroll_count': obj_user_enrolls_count
        })

    # elif obj_user_classes ==0 and

    else:
        return redirect('/app_classway/app_no_class/')


##############################################################################


##############################################################################


def app_no_class(request):
    return render(request, 'temp_app_classway/app_no_class.html')


def app_class_performance(request):

    if request.method == 'POST':
        shit_data = request.POST.get('getdata', 'None')

        bad_char = ['"']
        for i in bad_char:
            x = shit_data.replace(i, '')

        class_id = int(x)

        print("class_id",class_id)


        obj_stud_list = Enroll.objects.filter(class_id = class_id)

        print(obj_stud_list)

        list_stud_name = []
        list_stud_email = []

        for i in obj_stud_list:
            # print(i.user_id.first_name+" "+i.user_id.last_name)
            list_stud_name.append(i.user_id.first_name+" "+i.user_id.last_name)
            list_stud_email.append(i.user_id.email)


        print(list_stud_name)
        print(list_stud_email)


        # ---------------------------------------

        obj_qns = Question.objects.filter(class_id = class_id)




        print(obj_qns)


        



        # -----------------------------

        # list_qn_id = []
        # list_stud = []
        # list_total_attempt = []
        # for i, j in enumerate(obj_qns):
        #     list_qn_id.append(j.id)
        #     print("---------")

        #     obj_user = Answer.objects.filter(qn_id=list_qn_id[i])

        #     list_stud.append(obj_user)            
        #     print("obj_user",obj_user)

        #     print("len:",obj_user.__len__())

        #     list_total_attempt.append(0)

        #     for k in obj_user:
        #         obj_user_total_ans = Answer.objects.filter(qn_id=list_qn_id[i])
        #         print(obj_user_total_ans)
        #         list_total_attempt[i] += 1


        # # print("list_stud:",list_stud)
        # print("obj_qns:",obj_qns)
        # print("list_total_attempt:",list_total_attempt)

        # ---------------------------------------





        responseData = {
            'page': 'hii response...'
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")


    else:
        return render(request, 'temp_app_classway/app_class_performance.html')




# ***


def app_view_question(request):
    if request.method == 'POST':
        shit_data1 = request.POST.get('getdata1', 'None')
        shit_data2 = request.POST.get('getdata2', 'None')

        print(shit_data1)
        print(shit_data2)
        bad_char = ['"']
        for i in bad_char:
            x = shit_data1.replace(i, '')
        for i in bad_char:
            y = shit_data2.replace(i, '')

        class_idy = int(x)
        qn_idy = int(y)

        print(class_idy)
        print(qn_idy)

        global obj_class
        global obj_qnk
        global obj_stud_list
        global qn_idk

        obj_class = Class.objects.filter(id=class_idy)

        # get all qns from this class
        obj_qnk = Question.objects.filter(id=qn_idy, class_id=class_idy)

        print(obj_qnk)

        qn_idk = obj_qnk[0].id

        print('qn_idk:', qn_idk)

        obj_stud_list = Answer.objects.filter(qn_id=qn_idk)
        print('obj_stud_list:', obj_stud_list)

        for i in obj_stud_list:
            print(i.user_id.first_name)

        responseData = {
            'page': 'hii response...'
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")

    else:
        return render(request, 'temp_app_classway/app_view_question.html', {
            # 'obj_qn':obj_qn,
            'obj_class': obj_class,
            'obj_qnk': obj_qnk,
            'obj_stud_list': obj_stud_list,
            'qn_idk': qn_idk

        })


def app_view_question_student(request):
    if request.method == 'POST':

        obj_form = ModelFormAllotMarks(request.POST)
        global obj_qnq
        global obj_ans
        global obj_stud
        # global msg

        if obj_form.is_valid():
            print('valid form')
            msg = 'form valid'
            print('msg:', msg)

            marks = obj_form.cleaned_data['ans_marks']
            print('marks:', marks)

            print('obj_ans:', obj_ans)
            ans_id = obj_ans[0].id
            print('ans_id:', ans_id)

            allot_marks = Answer.objects.get(id=ans_id)
            if allot_marks.ans_marks is None:
                allot_marks.ans_marks = marks
                allot_marks.save()
                print('marks alloted...')
                msg = 'marks alloted...'
            else:
                print('marks already alloted...')
                msg = 'marks already alloted...'

            responseData = {
                'msg': msg
            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")

        else:
            print('invalid form')
            # msg='form invalid'

            shit_data1 = request.POST.get('getdata1', 'None')
            shit_data2 = request.POST.get('getdata2', 'None')

            print(shit_data1)
            print(shit_data2)
            bad_char = ['"']
            for i in bad_char:
                x = shit_data1.replace(i, '')
            for i in bad_char:
                y = shit_data2.replace(i, '')

            stud_idp = int(x)
            qn_idp = int(y)

            print('stud_idp', stud_idp)
            print('qn_idp', qn_idp)

            obj_stud = User.objects.filter(id=stud_idp)

            obj_qnq = Question.objects.filter(id=qn_idp)

            obj_ans = Answer.objects.filter(user_id=stud_idp, qn_id=qn_idp)

        responseData = {
            'page': 'hii response... from qn_student'
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")

    else:
        obj_form = ModelFormAllotMarks()
        return render(request, 'temp_app_classway/app_view_question_student.html', {
            'obj_form': obj_form,
            'obj_stud': obj_stud,
            'obj_qnq': obj_qnq,
            'obj_ans': obj_ans,
        })


def app_account_page(request):
    return render(request, 'temp_app_classway/app_account_page.html')


def app_status_page(request):
    return render(request, 'temp_app_classway/app_status_page.html')


def app_add_answer_todo(request):
    
    if request.method == 'POST':
        print('post')

        obj_form = ModelFormAddAnswer(request.POST)
        global class_name
        global qn_desc
        global qn_date
        global qn_marks
        global qn_deadline

        global class_idx
        global qn_idx
        global user_idx

        if obj_form.is_valid():
            print('valid')

            obj_qn = Question.objects.filter(id=qn_idx)
            print('obj_qn', obj_qn)

            obj_user = User.objects.filter(id=user_idx)
            print('obj_user', obj_user)

            ans_desc = obj_form.cleaned_data['ans_desc']

            if Answer.objects.filter(qn_id=obj_qn[0], user_id=obj_user[0]).exists():
                msg = 'already answered...'

            else:
                # FK mei obj store hoga
                insert_ans = Answer(
                    qn_id=obj_qn[0], user_id=obj_user[0], ans_desc=ans_desc)
                insert_ans.save()
                print('answer saved...')
                msg = 'answer submitted...'

                return render(request, 'temp_app_classway/app_add_answer_todo.html', {
                    'obj_form': obj_form,
                    'class_name': class_name,
                    'msg': msg,
                    'qn_desc': qn_desc
                })

            # print('desc:',obj_form.cleaned_data['ans_desc'])
            return render(request, 'temp_app_classway/app_add_answer_todo.html', {
                'obj_form': obj_form,
                'class_name': class_name,
                'msg': msg,
                'qn_desc': qn_desc
            })

        else:

            print('invalid form...')

            shit_data1 = request.POST.get('getdata1', 'None')
            shit_data2 = request.POST.get('getdata2', 'None')

            print(shit_data1)
            print(shit_data2)

            bad_char = ['"']

            for i in bad_char:
                x = shit_data1.replace(i, '')

            for i in bad_char:
                y = shit_data2.replace(i, '')

            # global class_idx
            # global qn_idx
            # global user_idx

            class_idx = int(x)
            qn_idx = int(y)

            user_idx = get_user_id(request)

            print('class_id:', class_idx)
            print('qn_id:', qn_idx)
            print('user_id:', user_idx)

            obj_class = Class.objects.filter(id=class_idx)
            # global class_name
            class_name = obj_class[0].class_name
            print('class_name:', class_name)

            obj_qn = Question.objects.filter(id=qn_idx)
            # global qn_desc
            qn_desc = obj_qn[0].qn_desc
            print(qn_desc)


            qn_marks =obj_qn[0].qn_marks 

            qn_date = obj_qn[0].qn_date
            # print(qn_date)

            qn_deadline = obj_qn[0].qn_deadline

            responseData = {
                # 'id': 4,
                # 'name': 'Test Response',
                # 'roles' : ['Admin','User']
                'page': 'hii response...'

            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")

            # obj_form = ModelFormAddAnswer()
            # return render(request, 'temp_app_classway/app_add_answer.html',{'obj_form':obj_form})

    else:
        print('get')
        # return redirect('/app_classway/app_add_answer/')
        obj_form = ModelFormAddAnswer()
        return render(request, 'temp_app_classway/app_add_answer_todo.html', {
            'obj_form': obj_form,
            'class_name': class_name,
            'qn_desc': qn_desc,
            'qn_date':qn_date,
            'qn_deadline':qn_deadline,
            'qn_marks':qn_marks
        })

    # return render(request, 'temp_app_classway/app_add_answer_todo.html')




# --------------------------------------------------------------------------

def app_todo_page(request):
    user_id = get_user_id(request)

    obj_enrolled_classes = Enroll.objects.filter(user_id=user_id)
    print(obj_enrolled_classes)


    user_id = get_user_id(request)
    print("user_id:",user_id)

    list_pendings = []
    # list_

    for i in obj_enrolled_classes:
        obj_qn = Question.objects.filter(class_id = i.class_id.id)
        for j in obj_qn:
            print(j.id)

            check_ans = Answer.objects.filter(qn_id = j.id, user_id=user_id)
            print(check_ans)
            if check_ans:
                print("hii")
            else:
                print(j," is empty")
                list_pendings.append(j)

    print(list_pendings)

    for k in list_pendings:
        print("desc:",k.qn_desc)
        print("id:",k.id)
        print("deadline:",k.qn_deadline)
        print("class_name:",k.class_id.class_name)



            # print(j.qn_desc)
            
        # break;    







    # class_id1 = obj_enrolled_classes[0].class_id.id
    
    # obj_total_qns1 = Question.objects.filter(class_id = class_id1)
    # print(obj_total_qns1)



    # class_id2 = obj_enrolled_classes[1].class_id.id

    # obj_total_qns2 = Question.objects.filter(class_id = class_id2)
    # print(obj_total_qns2)




    return render(request, 'temp_app_classway/app_todo_page.html',{
        'obj_enrolled_classes':obj_enrolled_classes,
        'list_pendings':list_pendings
    })


######################################################################################
######################################################################################
######################################################################################
######################################################################################


######################################################################################
######################################################################################
######################################################################################
######################################################################################


######################################################################################
######################################################################################
######################################################################################
######################################################################################

def generate_unique_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    return str(code)


def get_user_id(request):
    if 'logged_in_user' in request.session:
        user_email = request.session['logged_in_user']
        obj_user = User.objects.filter(email=user_email)
        return obj_user[0].id
    else:
        return '[user is not logged in]'


def filter_data(data):
    bad_char = ['"']
    for i in bad_char:
        x = data.replace(i, '')
    pure_data = int(x)
    return pure_data

######################################################################################
######################################################################################
######################################################################################
######################################################################################


######################################################################################
######################################################################################
######################################################################################
######################################################################################


######################################################################################
######################################################################################
######################################################################################
######################################################################################


def app_class_details(request):
    # global class_id

    if request.method == 'POST':
        print('post')
        user_id = get_user_id(request)

        # got the data but in json type
        shit_data = request.POST.get('getdata', 'None')

        # converting this shit into integer:

        bad_char = ['"']
        for i in bad_char:
            x = shit_data.replace(i, '')

        class_id = int(x)
        print("class_id:", class_id)

        global obj_class
        obj_class = Class.objects.filter(id=class_id)

        global obj_qn
        obj_qn = Question.objects.filter(class_id=class_id)
        # print(obj_qn)

        responseData = {
            'page': 'temp_app_classway/app_class_details'
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")
        # return JsonResponse('hii form views')
        # return render(request, 'temp_app_classway/app_class_details_enrolled.html',{'obj_class':obj_class,'obj_qn':obj_qn})
    else:

        print('get')
        return render(request, 'temp_app_classway/app_class_details.html', {'obj_class': obj_class, 'obj_qn': obj_qn})

    # return render(request, 'temp_app_classway/app_class_details_enrolled.html')


def app_add_question(request):
    if request.method == 'POST':
        print('post')

        global class_id_add_qn

        obj_form = ModelFormAddQuestion(request.POST)

        if obj_form.is_valid():
            print('form valid...')
            print('qn_desc:', obj_form.cleaned_data['qn_desc'])
            print('class_id_add_qn:', class_id_add_qn)
            print('qn deadline:', obj_form.cleaned_data['qn_deadline'])

            obj_class_add_qn = Class.objects.filter(id=class_id_add_qn)
            print('obj_class_add_qn', obj_class_add_qn)

            qn_desc = obj_form.cleaned_data['qn_desc']
            qn_marks = obj_form.cleaned_data['qn_marks']
            qn_deadline = obj_form.cleaned_data['qn_deadline']

            add_qn = Question(qn_marks=qn_marks, qn_desc=qn_desc,
                              qn_deadline=qn_deadline, class_id=obj_class_add_qn[0])
            add_qn.save()
            print('inserted')

            responseData = {
                'response': 'new question added...'
            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")

        else:
            print('form not valid')

            shit_data = request.POST.get('getdata', 'None')

            bad_char = ['"']
            for i in bad_char:
                x = shit_data.replace(i, '')

            class_id_add_qn = int(x)
            print('class_id_qn: ', class_id_add_qn)

            responseData = {
                'response': 'from add qn...'
            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")

    else:
        obj_form = ModelFormAddQuestion()
        print('get')

    return render(request, 'temp_app_classway/app_add_question.html', {'obj_form': obj_form})


# -------------------------------------------------------------------------------------------------------------


# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################
# ##############################################################################################################################


# ####################################################################################################################################


# ####################################################################################################################################

def app_create_class(request):
    if request.method == 'POST':

        form_obj = ModelFormNewClass(request.POST)

        if form_obj.is_valid():
            class_name = form_obj.cleaned_data['class_name']
            class_subject = form_obj.cleaned_data['class_subject']
            print(class_name)
            print(class_subject)

            current_user_email = request.session['logged_in_user']
            print(current_user_email)

            obj_user = User.objects.filter(email=current_user_email)
            present_codes = Class.objects.values_list('class_code', flat=True)
            count_present_code = Class.objects.all().count()

            print("total count:", count_present_code)

            for i in obj_user:
                user_id = i.id

            # creating unique class code
            code = generate_unique_code()

            for i in range(count_present_code):
                if Class.objects.filter(class_code=code):
                    i = 0
                    code = generate_unique_code()

            create_class = Class(class_name=class_name,
                                 class_subject=class_subject, class_code=code, class_admin=user_id)
            create_class.save()

            print('new class created...')
            return redirect('/app_classway/app_available_class/')
    else:
        print('get')
        form_obj = ModelFormNewClass()

    return render(request, 'temp_app_classway/app_create_class.html', {
        'create_class_form': form_obj
    })

# ####################################################################################################################################


def app_class_details_enrolled(request):
    # global class_id

    if request.method == 'POST':
        print('post')
        user_id = get_user_id(request)

        # got the data but in json type
        shit_data = request.POST.get('getdata', 'None')

        # converting this shit into integer:

        bad_char = ['"']
        for i in bad_char:
            x = shit_data.replace(i, '')

        class_id = int(x)
        print("class_id:", class_id)

        global obj_class
        obj_class = Class.objects.filter(id=class_id)

        global obj_qn
        obj_qn = Question.objects.filter(class_id=class_id)
        # print(obj_qn)


        



        responseData = {
            # 'id': 4,
            # 'name': 'Test Response',
            # 'roles' : ['Admin','User']
            'page': 'temp_app_classway/app_class_details_enrolled'

        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")
        # return JsonResponse('hii form views')
        # return render(request, 'temp_app_classway/app_class_details_enrolled.html',{'obj_class':obj_class,'obj_qn':obj_qn})
    else:

        print('get')
        return render(request, 'temp_app_classway/app_class_details_enrolled.html', {
            'obj_class': obj_class,
            'obj_qn': obj_qn
        })

    # return render(request, 'temp_app_classway/app_class_details_enrolled.html')


# ####################################################################################################################################


def app_available_class_enrolled(request):

    user_email = request.session['logged_in_user']

    # getting user id:
    obj_user_id = User.objects.filter(email=user_email)
    user_id = obj_user_id[0].id
    print('user_id: ', user_id)

    # getting all enrolled classes by this user:
    obj_total_enrolled_classes = Enroll.objects.filter(user_id=user_id)

    # -----------------------------------
    # -----------------------------------


    print('------')

    list_count = []
    for p in obj_total_enrolled_classes:
        print(p.class_id)
        temp = Enroll.objects.filter(class_id = p.class_id)
        # print(temp)
        count = 0
        for q in temp:
            print(q)
            count+=1

        list_count.append(count)


    print(list_count)







    # print("total students:",obj_total_enrolled_classes[0].__len__())
    print('------')



    # -----------------------------------
    # -----------------------------------

    print('class admin:',obj_total_enrolled_classes[0].class_id.class_admin)
    x = obj_total_enrolled_classes[0].class_id.class_admin
    
    obj_admin = User.objects.get(id = x)

    print(obj_admin.first_name)







    # getting admin names into a list
    list_admin_name = []

    for i in obj_total_enrolled_classes:
        print(i)
        admin_id =i.class_id.class_admin 
        obj_admin_name = User.objects.get(id = admin_id)
        name = obj_admin_name.first_name+" "+obj_admin_name.last_name
        list_admin_name.append(name)


    
    print(list_admin_name)


    for i in list_admin_name:
        print(i)


    # zipping both the list and the object to access both simultanously:

    mylist_all = zip(obj_total_enrolled_classes,list_admin_name,list_count)
    # loop iterates only one time, don't waste here
    # for i,j in mylist_all:
    #     print(i.class_id.class_name,j)

    # print(mylist_all)


    # for k,p in mylist_all:
    #     print(k.class_id.class_name,p)



    # -----------------------
    # ------------
    # -----------------------------------

    # print('------------------')


    # list_x = [[2,3,4],[1,2,3]]



    # for index, item in enumerate(obj_total_enrolled_classes):
    #     print(index)
    #     print(item.class_id.class_name)
    #     print(list_admin_name[index])



    # for i in range(obj_total_enrolled_classes.__len__()):
    #     print(obj_total_enrolled_classes[i])





    # for i in obj_total_enrolled_classes:
    #     admin_id =i.class_id.class_admin 
    #     print(admin_id)

    #     obj_admin_name = User.objects.get(id = admin_id)
    #     print(obj_admin_name.first_name+' '+obj_admin_name.last_name)


    # print('obj_total_enrolled_classes:',obj_total_enrolled_classes[0].class_id.class_admin)
    
    # temp = obj_total_enrolled_classes[0].class_id.class_admin

    # class_admin = User.objects.get(id = temp)
    # print(class_admin.first_name+' '+class_admin.last_name)



    if mylist_all:
        return render(request, 'temp_app_classway/app_available_class_enrolled.html', {
            'mylist_all': mylist_all,
            'test':'test'
        })
    else:
        return render(request, 'temp_app_classway/app_no_enrolled_class.html')


# ####################################################################################################################################

def app_join_class(request):

    if request.method == 'POST':
        print('post')

        form_obj = ModelFormJoinClass(request.POST)

        if form_obj.is_valid():
            print('form valid')

            user_code = form_obj.cleaned_data['class_code']
            print('user_code:', user_code)

            # getting current user id:
            obj_current_user_id = User.objects.filter(
                email=request.session['logged_in_user'])

            current_user_id = obj_current_user_id[0].id
            print('current_user_id:', current_user_id)

            get_code = Class.objects.filter(class_code=user_code)

            if get_code:
                class_id = get_code[0].id
                class_admin = get_code[0].class_admin

                # print("type class_admin",type(class_admin))
                # print("type current_user_id",type(current_user_id))

                # getting class code
                obj_get_class_id = Class.objects.filter(class_code=user_code)
                class_id = obj_get_class_id[0].id

                print("class id:", class_id)

                # check_class_id_enroll = Enroll.objects.filter(
                # class_id=class_id)

                # check_user_id_enroll = Enroll.objects.filter(
                # user_id=current_user_id)

                if Enroll.objects.filter(user_id=current_user_id, class_id=class_id).exists():
                    print('user exists in this class')
                    msg = 'already enrolled...'
                    return render(request, 'temp_app_classway/app_join_class.html', {
                        'join_class_form': form_obj,
                        'msg': msg
                    })
                else:
                    print('user does not exists in this class')

                    print('current_user_id:', current_user_id)
                    print('class_admin:', class_admin)

                    # here current_user_id was integer therefore needed to convert into string
                    if class_admin == str(current_user_id):
                        print('admin cannot enroll')
                        msg = 'admin cannot enroll...'
                        return render(request, 'temp_app_classway/app_join_class.html', {
                            'join_class_form': form_obj,
                            'msg': msg
                        })

                    else:
                        print('success')
                        enroll_user = Enroll(
                            class_id=get_code[0], user_id=obj_current_user_id[0])  # FK mei obj store hoga
                        enroll_user.save()

                        print('data inserted...')
                        msg = 'class enrolled...'
                        return render(request, 'temp_app_classway/app_join_class.html', {
                            'join_class_form': form_obj,
                            'msg': msg
                        })

            else:
                print('code not found')
                msg = 'invalid code...'
                return render(request, 'temp_app_classway/app_join_class.html', {
                    'join_class_form': form_obj,
                    'msg': msg
                })
    else:
        print('get')
        form_obj = ModelFormJoinClass()

    return render(request, 'temp_app_classway/app_join_class.html', {
        'join_class_form': form_obj
    })

# ####################################################################################################################################


def app_add_answer(request):

    if request.method == 'POST':
        print('post')

        obj_form = ModelFormAddAnswer(request.POST)
        global class_name
        global qn_desc
        global qn_date
        global qn_marks
        global qn_deadline

        global class_idx
        global qn_idx
        global user_idx

        if obj_form.is_valid():
            print('valid')

            obj_qn = Question.objects.filter(id=qn_idx)
            print('obj_qn', obj_qn)

            obj_user = User.objects.filter(id=user_idx)
            print('obj_user', obj_user)

            ans_desc = obj_form.cleaned_data['ans_desc']

            if Answer.objects.filter(qn_id=obj_qn[0], user_id=obj_user[0]).exists():
                msg = 'already answered...'

            else:
                # FK mei obj store hoga
                insert_ans = Answer(
                    qn_id=obj_qn[0], user_id=obj_user[0], ans_desc=ans_desc)
                insert_ans.save()
                print('answer saved...')
                msg = 'answer submitted...'

                return render(request, 'temp_app_classway/app_add_answer.html', {
                    'obj_form': obj_form,
                    'class_name': class_name,
                    'msg': msg,
                    'qn_desc': qn_desc,
                    'qn_marks':qn_marks,
                    'qn_date':qn_date,
                    'qn_deadline':qn_deadline
                })

            # print('desc:',obj_form.cleaned_data['ans_desc'])
            return render(request, 'temp_app_classway/app_add_answer.html', {
                'obj_form': obj_form,
                'class_name': class_name,
                'msg': msg,
                'qn_desc': qn_desc,
                'qn_marks':qn_marks,
                'qn_date':qn_date,
                'qn_deadline':qn_deadline
            })

        else:

            print('invalid form...')

            shit_data1 = request.POST.get('getdata1', 'None')
            shit_data2 = request.POST.get('getdata2', 'None')

            print(shit_data1)
            print(shit_data2)

            bad_char = ['"']

            for i in bad_char:
                x = shit_data1.replace(i, '')

            for i in bad_char:
                y = shit_data2.replace(i, '')

            # global class_idx
            # global qn_idx
            # global user_idx

            class_idx = int(x)
            qn_idx = int(y)

            user_idx = get_user_id(request)

            print('class_id:', class_idx)
            print('qn_id:', qn_idx)
            print('user_id:', user_idx)

            obj_class = Class.objects.filter(id=class_idx)
            # global class_name
            class_name = obj_class[0].class_name
            print('class_name:', class_name)



            obj_qn = Question.objects.filter(id=qn_idx)
            # global qn_desc
            qn_desc = obj_qn[0].qn_desc
            print(qn_desc)

            qn_marks =obj_qn[0].qn_marks 

            qn_date = obj_qn[0].qn_date
            # print(qn_date)

            qn_deadline = obj_qn[0].qn_deadline
            # print(qn_deadline)



            responseData = {
                # 'id': 4,
                # 'name': 'Test Response',
                # 'roles' : ['Admin','User']
                'page': 'hii response...'

            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")

            # obj_form = ModelFormAddAnswer()
            # return render(request, 'temp_app_classway/app_add_answer.html',{'obj_form':obj_form})

    else:
        print('get')
        # return redirect('/app_classway/app_add_answer/')
        obj_form = ModelFormAddAnswer()
        return render(request, 'temp_app_classway/app_add_answer.html', {
            'obj_form': obj_form,
            'class_name': class_name,
            'qn_desc': qn_desc,
            'qn_date':qn_date,
            'qn_deadline':qn_deadline,
            'qn_marks':qn_marks
        })


# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------

def app_delete_class(request):
    if request.method=='POST':
        global class_id

        if 'class_id' not in request.POST:
            print('yes by user')

            del_row = Class.objects.get(id=class_id)
            del_row.delete()

            return render(request, 'temp_app_classway/app_class_details.html')

        else:
            print('1st call')

            shit_data = request.POST.get('class_id', 'None')

            bad_char = ['"']
            for i in bad_char:
                x = shit_data.replace(i, '')

            class_id = int(x)

            obj_del_class = Class.objects.filter(id=class_id)
            class_name = obj_del_class[0].class_name

            responseData = {
                'data': 'response from app_delete_class...',
                'class_name': class_name
            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")


    else:
        responseData = {
            'data': "something's wrong"
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")




def app_exit_class(request):
    if request.method=='POST':
        global class_id

        if 'class_id' not in request.POST:
            print('yes by user')

            stud_id = get_user_id(request)

            print('user_id:',stud_id)

            del_row = Enroll.objects.get(class_id = class_id,user_id=stud_id)
            print(del_row)
            del_row.delete()

            return render(request, 'temp_app_classway/app_class_details.html')

        else:
            print('1st call')

            shit_data = request.POST.get('class_id', 'None')

            bad_char = ['"']
            for i in bad_char:
                x = shit_data.replace(i, '')

            class_id = int(x)

            obj_del_class = Class.objects.filter(id=class_id)
            class_name = obj_del_class[0].class_name

            responseData = {
                'data': 'response from app_delete_class...',
                'class_name': class_name
            }

            return HttpResponse(json.dumps(responseData), content_type="application/json")


    else:
        responseData = {
            'data': "something's wrong"
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")



def app_edit_class(request):
    pass


def app_view_students(request):
    

    if request.method == 'POST':

        global class_id
        global obj_studs
        global subject
        
        shit_data = request.POST.get('getdata', 'None')

        print('shit_data',shit_data)

        bad_char = ['"']
        for i in bad_char:
            x = shit_data.replace(i, '')
        class_id = int(x)
        print(class_id)


        obj_studs = Enroll.objects.filter(class_id = class_id)
        print('obj_studs:',obj_studs)

        for i in obj_studs:
            print(i.user_id.first_name)

        
        obj_class_info = Class.objects.get(id = class_id)
        # print('obj_class_info:',obj_class_info.class_subject)
        subject = obj_class_info.class_subject


        responseData = {
                'data': 'response from app_view_studs...'
                # 'class_name': class_name
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")

    
    
    else:
        return render(request, 'temp_app_classway/app_view_students.html',{
            'obj_studs':obj_studs,
            'subject':subject
        })


def app_remove_student(request):

    if request.method == 'POST':
        print("post")

        shit_data1 = request.POST.get('getdata1', 'None')
        shit_data2 = request.POST.get('getdata2', 'None')

        print(shit_data1)
        print(shit_data2)
        bad_char = ['"']

        for i in bad_char:
            x = shit_data1.replace(i, '')
        
        for i in bad_char:
            y = shit_data2.replace(i, '')

        global class_id

        stud_id = int(x)
        class_id = int(y)

        print('stud_id',stud_id)
        print('class_id',class_id)


        remove_stud = Enroll.objects.get(class_id  = class_id, user_id = stud_id)
        remove_stud.delete()


        global stud_name
        stud_name = remove_stud.user_id.first_name





        responseData = {
                'data': 'response from app_remove_stud...'
                # 'class_name': class_name
        }

        return HttpResponse(json.dumps(responseData), content_type="application/json")


    else:
        print('get')

        obj_studs = Enroll.objects.filter(class_id = class_id)
        # print('obj_studs:',obj_studs)

        return render(request, 'temp_app_classway/app_view_students.html',{
            'obj_studs':obj_studs,
            'subject':subject,
            'stud_name':stud_name
        })






# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////

