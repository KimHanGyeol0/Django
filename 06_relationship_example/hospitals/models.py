from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'

class Patient(models.Model):
    name = models.TextField()
    # 1:N
    # doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    doctors = models.ManyToManyField(Doctor, related_name='patients')
    """
     M:N(방법 2), patient_doctors 중계 모델 만들어짐
     patient1, doctor1 만들고
     patient1.doctors.add(doctor1)으로 추가
     patient1.doctors.all()로 환자 1번과 예약한 모든 의사

     doctor1.patient_set.all() 1번 의사와 예약한 모든 환자
     doctor1.patient_set.add(patient2) 으로 추가
     역참조는 참조가 되어지는, 필드가 없는 모델에서 사용

     doctor1.patient_set.remove(patient2)으로 의사 입장에서 취소
     patient1.doctors.remove(doctor1)으로 환자 입장에서 취소

     그런데 추가데이터(예약 시간, ...)이 있을 경우에는 중계 테이블 필요(manytomany필드에 through='Reservation'으로 연결)
     doctors = models.ManyToManyField(Doctor, related_name='patients')로 참조되는 테이블 이름 변경
     docto1.patients.all()로 사용가능
     """
    
    # 
    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'

# # M:N을 하기 위한 중계 모델(방법 1)
# class Reservation(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.doctor_id}번 의사의 {self.patient_id}번 환자'
#     # doctor1.reservation_set.all() 하면 1번 의사의 모든 예약 조회
#     # patien1.reservation_set.all() 하면 1번 환자의 모든 예약 조회