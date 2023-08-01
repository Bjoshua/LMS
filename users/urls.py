from django.urls import path
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from . import adminview, studentview, staffview
from Schoolapp import views as webview
from chat import views as chatview

urlpatterns = [
    path('login/', user_views.student_login, name='login'),
    path('register_prospective_user/', webview.Register, name='register'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    path('login_user/',user_views.Login_user, name="login_user"),
    path('logout/', user_views.logout_user, name="logout"),

    
    #chat_views
    path('group_chat_middleware', user_views.group_chat_middleware, name='group_chat_middleware'),
    path('room/<room_id>/', chatview.display_room, name="room"),
    path('delete_message/<room_id>/<message_id>/', chatview.delete_message, name="delete_message"),
    path('delete_message_personal/<receiver_pk>/<message_id>/', chatview.delete_message_personal, name="delete_message_personal"),
    path('edit_message/<room_id>/<message_id>/', chatview.edit_message, name="edit_message"),
    path('edit_message_personal/<receiver_pk>/<message_id>/', chatview.edit_message_personal, name="edit_message_personal"),


    path('personal_chat/<receiver_pk>/', chatview.Sendpersonalmessage, name="personal_message"),
    path('chhose_chat/', chatview.Chatroom, name="display_room"),
    # path('send_message/<room_id>/', chatview.send_message, name="send_message"),
    

    # admin Views
    path('admin_home/', adminview.admin_home, name="admin_home"),
    path('admin_profile/', adminview.admin_profile, name="admin_profile"),
    path('admin_profile_update/', adminview.admin_profile_update, name="admin_profile_update"),
    path("admin_assignment_view/", adminview.admin_assignment_view, name="admin_assignment_view"),
    path("admin_test_view/", adminview.admin_test_view, name="admin_test_view"),
    path("admin_examination_view/", adminview.admin_examination_view, name="admin_exam_view"),
    path("admin_lecture_view/", adminview.admin_lecture_view, name="admin_lecture_view"),
    path("admin_edit_lecture/<int:lecture_id>,", adminview.edit_lecture, name="admin_edit_lecture"),
    path("admin_staff_edit_profile/<int:user_id>", adminview.admin_staff_edit_profile, name="admin_staff_edit_profile"),
    path("delete_staff/<staff_id>/", adminview.delete_staff, name="delete_staff"),
    # path("add_staff/", adminview.add_staff, name="add_staff"),
    path("session/", adminview.sessions, name="session"),
    path("edit_session/<session_id>/", adminview.edit_session, name="edit_session"),
    path("delete_session/<session_id>/", adminview.delete_session, name="delete_session"),
    path("manage_stud/", adminview.manage_stud, name="manage_stud"),
    path("admin_student_edit_profile/<int:user_id>", adminview.admin_student_edit_profile, name="admin_student_edit_profile"),
    path("delete_student/<student_id>/", adminview.delete_student, name="delete_student"),
    path("createcbt/", staffview.create_cbt, name="create_cbt"),
    path("set_cbt/<cbt_id>/", staffview.set_cbt, name="set_cbt"),
    path("take_cbt/<cbt_id>/", studentview.take_cbt, name="take_cbt"),
    path("allcbts/", studentview.allcbts, name="allcbts"),
    path("view_score/<cbtr_id>/", studentview.view_score, name="view_score"),
    path("bulk_email/", adminview.bulk_email, name="bulk_email"),


    #Subject
    path("manage_sub/", adminview.manage_sub, name="manage_sub"),
    path("edit_sub/<subject_id>/", adminview.edit_sub, name="edit_sub"),
    path("delete_sub/<subject_id>/", adminview.delete_sub, name="delete_sub"),
    path("manage_class/", adminview.manage_class, name="manage_class"),
    path("delete_class/<class_id>/", adminview.delete_class, name="delete_class"),
    path("manage_staff/", adminview.manage_staff, name="manage_staff"),
    path("admin_prospective_view/", adminview.manage_prospective, name="admin_prospective_view"),
    path("student_leave_view/", adminview.student_leave_view, name="student_leave_view"),
    path('student_leave_approve/<leave_id>/', adminview.student_leave_approve, name="student_leave_approve"),
    path('student_leave_reject/<leave_id>/', adminview.student_leave_reject, name="student_leave_reject"),
    path("staff_leave_view/", adminview.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', adminview.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', adminview.staff_leave_reject, name="staff_leave_reject"),
    path('student_feedback_message_reply/<feedback_id>/', adminview.student_feedback_message_reply, name="student_feedback_message_reply"),
    path('student_feedback_view/', adminview.student_feedback_view, name="student_feedback_view"),
    path('staff_feedback_message_reply/<feedback_id>/', adminview.staff_feedback_message_reply, name="staff_feedback_message_reply"),
    path('staff_feedback_view/', adminview.staff_feedback_view, name="staff_feedback_view"),
    path("admin_delete_lecture/<int:lecture_id>/", adminview.admin_delete_lecture, name="admin_delete_lecture"),
    path("admin_edit_event/<int:event_id>/", adminview.edit_event, name="edit_event"),
    path("admin_delete_event/<int:event_id>/", adminview.delete_event, name="delete_event"),
    path("admin_edit_class/<int:class_id>/", adminview.edit_class, name="admin_edit_class"),
    path("admin_change_user_password/<int:user_id>/", adminview.passwordchange, name="passwordchange"),
    path("add_events/", adminview.Events, name="add_events"),
    path("manage_events/", adminview.manage_events, name="manage_events"),


    #staffviews
    path("room_access/<staff_id>/", staffview.room_access, name="room_access"),
    path("staff_exam_view/", staffview.staff_exam_view, name="staff_exam_view"),
    path("staff_manage_stud/", staffview.staff_manage_stud, name="staff_manage_stud"),
    path("delete_lecture/<int:lecture_id>/", staffview.delete_lecture, name="delete_lecture"),
    path('staff_leave/', staffview.staff_leave, name="staff_leave"),
    path('staff_feedback/', staffview.staff_feedback, name="staff_feedback"),
    path('staff_home/', staffview.staff_home, name="staff_home"),
    path('staff_manage_class', staffview.staff_manage_class, name='staff_manage_class'),
    path("staff_add_assignment/", staffview.staff_add_assignment, name="staff_add_assignment"),    
    path("staff_add_test/", staffview.staff_add_test, name="staff_add_test"),    
    path("staff_add_exam/", staffview.staff_add_exam, name="staff_add_exam"),    
    path("staff_add_lectures/", staffview.staff_add_lectures, name="staff_add_lectures"),    
    path("staff_assignment_view/", staffview.staff_assignment_view, name="staff_assignment_view"),    
    path("staff_marked_assignment_view/", staffview.staff_marked_assignment_view, name="staff_marked_assignment_view"),    
    path("staff_marked_test_view/", staffview.staff_marked_test_view, name="staff_marked_test_view"),    
    path("staff_marked_examination_view/", staffview.staff_marked_examination_view, name="staff_marked_examination_view"),    
    path('staff_lecture_view/', staffview.staff_lecture_view, name='staff_lecture_view'),
    path('staff_edit_lecture/<int:lecture_id>', staffview.edit_lecture, name='staff_edit_lecture'),
    path("staff_test_view/", staffview.staff_test_view, name="staff_test_view"),
    path("staff_update_profile/", staffview.staff_update_profile, name="staff_update_profile"),
    

    # studentviews
    path('student_home_profile/', studentview.student_home_profile, name="student_home"),
    path('student_result/', studentview.student_result, name="student_result"),
    path('student_leave/', studentview.student_leave, name="stud_leave"),
    path('student_feedback/', studentview.student_feedback, name="stud_feedback"),
    path('student_assignment/', studentview.student_assignment, name='student_assignment'),
    path('student_test/', studentview.student_test, name='student_test'),
    path('student_lecture/', studentview.student_lecture, name='student_lecture'),
    path('student_examination/', studentview.student_examination, name='student_examination'),
    path("student_update_profile/", studentview.student_update_profile, name="student_update_profile"),
    path("assignment_views/", studentview.assignment_view, name="assignment_view"),
    path("test_views/", studentview.test_view, name="test_view"),
    path("exam_views/", studentview.exam_view, name="exam_view"),
    path("subject_views/", studentview.subjects, name="subjects"),

    path("profile_page/<user_id>/", adminview.profile_page, name="profile_page"),
]