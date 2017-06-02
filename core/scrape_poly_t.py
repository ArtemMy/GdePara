from apscheduler.schedulers.background import BackgroundScheduler
from core.models import ModelCourse, ModelClassFormat, ModelGroup, ModelTeacher
import urllib.request, json
from django.db import transaction

@transaction.atomic
def get_schedule(teachers, id, gr, courses, class_f):
	with urllib.request.urlopen("http://ruz2.spbstu.ru/api/v1/ruz/scheduler/" + str(id)) as url:
		data = json.loads(url.read().decode())
		for day in data.get("days"):
			for lesson in day.get("lessons"):
				if lesson["teachers"] and lesson["teachers"][0].get("id"):
					if not lesson["teachers"][0].get("id") in teachers:
						teachers[int(lesson["teachers"][0].get("id"))] = ModelTeacher(first_name=lesson["teachers"][0]["first_name"],
							 middle_name=lesson["teachers"][0]["middle_name"],
							 last_name=lesson["teachers"][0]["last_name"],
							 degree=lesson["teachers"][0]["chair"]
						)
					teach = teachers[int(lesson["teachers"][0].get("id"))]
				else:
					teach = None
				print("here")
				course = next((c for c in courses if c.name == lesson["subject"] and c.teacher == teach), None)

				if(not course):
					course = ModelCourse(lesson["subject"], teach)
					courses.add(course)

				class_f.append(ModelClassFormat(day_of_week=day.get("weekday"), \
					time_of_beginning=lesson.get("time_start"), \
					time_of_ending=lesson.get("time_end"), \
					course=course \
					))

				if(lesson.get("typeObj")):
					type_of_class=lesson.get("typeObj").get("name")
				if(day.get("auditories")):
					class_f.buildauditoriuming = day.get("auditories").get("name")
					if(day.get("auditories").get("building")):
						class_f.building = day.get("auditories").get("building").get("name")

@transaction.atomic
def get_tea():
	with urllib.request.urlopen("http://ruz2.spbstu.ru/api/v1/ruz/teachers/") as url:
		data = json.loads(url.read().decode())
		dct = {}
		for tea in data["teachers"]:
			m_t = ModelTeacher(first_name=tea["first_name"],
						 middle_name=tea["middle_name"],
						 last_name=tea["last_name"],
						 degree=tea["chair"]
						 )
			dct[int(tea["id"])] = m_t
	return dct

def get_grs(fac, grs):
	with urllib.request.urlopen("http://ruz2.spbstu.ru/api/v1/ruz/faculties/" + str(fac["id"]) + "/groups/") as url:
		data = json.loads(url.read().decode())
		for gr in data["groups"]:
			m_gr = ModelGroup(number=gr.get("name"),
						 spec=gr.get("spec"),
						 faculty=fac.get("name"),
						 faculty_abbr=fac.get("abbr")
						 )
			grs.append(m_gr)
			yield gr["id"], m_gr

def update_tt():
	ModelCourse.objects.all().delete()
	ModelClassFormat.objects.all().delete()
	ModelGroup.objects.all().delete()
	ModelTeacher.objects.all().delete()

	teachers = get_tea()
	print("{} teachers".format(len(teachers)))
	courses = set()
	class_f = list()
	grs = list()
	with urllib.request.urlopen("http://ruz2.spbstu.ru/api/v1/ruz/faculties/") as url:
		data = json.loads(url.read().decode())
		for fac in data["faculties"][7:8]:
			print("{} out of {} facs".format(data["faculties"].index(fac), len(data["faculties"])))
			print(fac)
			sch_grs = [x for x in get_grs(fac, grs)]
			for id, gr in sch_grs:
				print("{} out of {} grs".format(sch_grs.index((id, gr)), len(sch_grs)))
				get_schedule(teachers, id, gr, courses, class_f)

	ModelTeacher.objects.bulk_create(teachers.values())
	print(len(courses))
	ModelCourse.objects.bulk_create(list(courses))
	print(len(ModelCourse.objects.all()))
	ModelClassFormat.objects.bulk_create(class_f)
	ModelGroup.objects.bulk_create(grs)

def setup():
	sched = BackgroundScheduler()

	@sched.scheduled_job('cron', hour='04', minute='24')
	def sched_update_tt():
		update_tt()
	sched.start()