from django.db import models
from core.models import AuditModel
from django.utils import timezone
from accounts.models import BRANCH, PROGRAM, INSTITUTE, SEMESTER, YEAR
from academic.models import ACADEMIC_YEAR, EXAMINATION, CURRICULUM

class STUDENT(AuditModel):
    STUDENT_ID = models.AutoField(primary_key=True, db_column='STUDENT_ID')
    ENROLLMENT_NO = models.CharField(max_length=20, unique=True, db_column='ENROLLMENT_NO')
    FIRST_NAME = models.CharField(max_length=50, db_column='FIRST_NAME')
    MIDDLE_NAME = models.CharField(max_length=50, null=True, blank=True, db_column='MIDDLE_NAME')
    LAST_NAME = models.CharField(max_length=50, db_column='LAST_NAME')
    DATE_OF_BIRTH = models.DateField(db_column='DATE_OF_BIRTH')
    GENDER = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        db_column='GENDER'
    )
    EMAIL = models.EmailField(unique=True, db_column='EMAIL')
    PHONE = models.CharField(max_length=15, db_column='PHONE')
    ADDRESS = models.TextField(db_column='ADDRESS')
    CITY = models.CharField(max_length=50, db_column='CITY')
    STATE = models.CharField(max_length=50, db_column='STATE')
    PINCODE = models.CharField(max_length=6, db_column='PINCODE')
    BLOOD_GROUP = models.CharField(max_length=5, db_column='BLOOD_GROUP')
    PHOTO = models.ImageField(upload_to='student_photos/', null=True, blank=True, db_column='PHOTO')
    
    # Academic Details
    BRANCH = models.ForeignKey(BRANCH, on_delete=models.PROTECT, db_column='BRANCH_ID')
    PROGRAM = models.ForeignKey(PROGRAM, on_delete=models.PROTECT, db_column='PROGRAM_ID')
    ACADEMIC_YEAR = models.ForeignKey(ACADEMIC_YEAR, on_delete=models.PROTECT, db_column='ACADEMIC_YEAR_ID')
    CURRENT_SEMESTER = models.IntegerField(db_column='CURRENT_SEMESTER')
    ADMISSION_DATE = models.DateField(db_column='ADMISSION_DATE')
    
    # Status
    IS_ACTIVE = models.BooleanField(default=True, db_column='IS_ACTIVE')

    class Meta:
        db_table = '"STUDENT"."STUDENTS"'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"{self.ENROLLMENT_NO} - {self.FIRST_NAME} {self.LAST_NAME}"

class STUDENT_PARENT(AuditModel):
    PARENT_ID = models.AutoField(primary_key=True, db_column='PARENT_ID')
    STUDENT = models.ForeignKey(STUDENT, on_delete=models.CASCADE, db_column='STUDENT_ID')
    RELATION = models.CharField(
        max_length=10,
        choices=[('FATHER', 'Father'), ('MOTHER', 'Mother'), ('GUARDIAN', 'Guardian')],
        db_column='RELATION'
    )
    FIRST_NAME = models.CharField(max_length=50, db_column='FIRST_NAME')
    MIDDLE_NAME = models.CharField(max_length=50, null=True, blank=True, db_column='MIDDLE_NAME')
    LAST_NAME = models.CharField(max_length=50, db_column='LAST_NAME')
    OCCUPATION = models.CharField(max_length=100, db_column='OCCUPATION')
    EMAIL = models.EmailField(db_column='EMAIL')
    PHONE = models.CharField(max_length=15, db_column='PHONE')
    ANNUAL_INCOME = models.DecimalField(max_digits=12, decimal_places=2, db_column='ANNUAL_INCOME')
    IS_ACTIVE = models.BooleanField(default=True, db_column='IS_ACTIVE')

    class Meta:
        db_table = '"STUDENT"."STUDENT_PARENTS"'
        verbose_name = 'Student Parent'
        verbose_name_plural = 'Student Parents'
        unique_together = ['STUDENT', 'RELATION']

    def __str__(self):
        return f"{self.STUDENT.ENROLLMENT_NO} - {self.RELATION} - {self.FIRST_NAME}"

class STUDENT_ACADEMIC(AuditModel):
    ACADEMIC_ID = models.AutoField(primary_key=True, db_column='ACADEMIC_ID')
    STUDENT = models.ForeignKey(STUDENT, on_delete=models.CASCADE, db_column='STUDENT_ID')
    QUALIFICATION = models.CharField(max_length=50, db_column='QUALIFICATION')  # e.g., "10th", "12th", "BTech"
    BOARD_UNIVERSITY = models.CharField(max_length=100, db_column='BOARD_UNIVERSITY')
    INSTITUTION = models.CharField(max_length=200, db_column='INSTITUTION')
    YEAR_OF_PASSING = models.IntegerField(db_column='YEAR_OF_PASSING')
    PERCENTAGE = models.DecimalField(max_digits=5, decimal_places=2, db_column='PERCENTAGE')
    DIVISION = models.CharField(max_length=20, db_column='DIVISION')  # First, Second, Third
    SUBJECTS = models.JSONField(db_column='SUBJECTS')  # Store subjects as JSON
    DOCUMENTS = models.JSONField(db_column='DOCUMENTS', null=True, blank=True)  # Store document URLs
    IS_VERIFIED = models.BooleanField(default=False, db_column='IS_VERIFIED')

    class Meta:
        db_table = '"STUDENT"."STUDENT_ACADEMICS"'
        verbose_name = 'Student Academic'
        verbose_name_plural = 'Student Academics'
        unique_together = ['STUDENT', 'QUALIFICATION']

    def __str__(self):
        return f"{self.STUDENT.ENROLLMENT_NO} - {self.QUALIFICATION}"

class STUDENT_RESULT(AuditModel):
    RESULT_ID = models.AutoField(primary_key=True, db_column='RESULT_ID')
    STUDENT = models.ForeignKey(STUDENT, on_delete=models.CASCADE, db_column='STUDENT_ID')
    CURRICULUM = models.ForeignKey(CURRICULUM, on_delete=models.PROTECT, db_column='CURRICULUM_ID')
    EXAMINATION = models.ForeignKey(EXAMINATION, on_delete=models.PROTECT, db_column='EXAMINATION_ID')
    MARKS_OBTAINED = models.DecimalField(max_digits=5, decimal_places=2, db_column='MARKS_OBTAINED')
    IS_PASS = models.BooleanField(db_column='IS_PASS')
    GRADE = models.CharField(max_length=2, db_column='GRADE')
    GRADE_POINTS = models.DecimalField(max_digits=10, decimal_places=1, db_column='GRADE_POINTS')
    ATTEMPT_NUMBER = models.IntegerField(default=1, db_column='ATTEMPT_NUMBER')
    REMARKS = models.CharField(max_length=255, null=True, blank=True, db_column='REMARKS')
    IS_VERIFIED = models.BooleanField(default=False, db_column='IS_VERIFIED')

    class Meta:
        db_table = '"STUDENT"."STUDENT_RESULTS"'
        verbose_name = 'Student Result'
        verbose_name_plural = 'Student Results'
        unique_together = ['STUDENT', 'CURRICULUM', 'EXAMINATION', 'ATTEMPT_NUMBER']

    def __str__(self):
        return f"{self.STUDENT.ENROLLMENT_NO} - {self.CURRICULUM.COURSE.CODE} - {self.EXAMINATION.NAME}"

class STUDENT_MASTER(AuditModel):
    RECORD_ID = models.AutoField(primary_key=True, db_column='RECORD_ID')
    STUDENT_ID = models.CharField(max_length=20, unique=True, db_column='STUDENT_ID')
    INSTITUTE = models.CharField(max_length=20, db_column='INSTITUTE_CODE')
    ACADEMIC_YEAR = models.CharField(max_length=10, db_column='ACADEMIC_YEAR')
    BATCH = models.CharField(
        max_length=4,
        db_column='BATCH',
        help_text='Expected graduation/passout year (e.g., 2025)'
    )
    ADMISSION_CATEGORY = models.CharField(max_length=20, db_column='ADMISSION_CATEGORY')
    FORM_NO = models.IntegerField(db_column='FORM_NO')
    VALIDITY = models.DateField(db_column='VALIDITY', default=timezone.now)
    NAME_ON_CERTIFICATE = models.CharField(max_length=100, db_column='NAME_ON_CERTIFICATE', blank=True, default='')
    NAME = models.CharField(max_length=100, db_column='NAME')
    SURNAME = models.CharField(max_length=100, db_column='SURNAME')
    PARENT_NAME = models.CharField(max_length=100, db_column='PARENT_NAME', default='')
    MOTHER_NAME = models.CharField(max_length=100, db_column='MOTHER_NAME', blank=True, default='')
    FATHER_NAME = models.CharField(max_length=100, db_column='FATHER_NAME', default='')
    GENDER = models.CharField(max_length=10, db_column='GENDER', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    DOB = models.DateField(db_column='DOB')
    DOP = models.DateField(db_column='DOP', null=True, blank=True)
    PER_ADDRESS = models.TextField(db_column='PER_ADDRESS', blank=True, default='')
    LOC_ADDRESS = models.TextField(db_column='LOC_ADDRESS', blank=True, default='')
    PER_STATE_ID = models.IntegerField(db_column='PER_STATE_ID', default=1)
    LOC_STATE_ID = models.IntegerField(db_column='LOC_STATE_ID', default=1)
    PER_PHONE_NO = models.CharField(max_length=15, db_column='PER_PHONE_NO', blank=True, default='')
    LOC_PHONE_NO = models.CharField(max_length=15, db_column='LOC_PHONE_NO', blank=True, default='')
    MOB_NO = models.CharField(max_length=15, db_column='MOB_NO')
    EMAIL_ID = models.EmailField(db_column='EMAIL_ID')
    PER_CITY = models.CharField(max_length=50, db_column='PER_CITY', blank=True, default='')
    LOC_CITY = models.CharField(max_length=50, db_column='LOC_CITY', blank=True, default='')
    NATIONALITY = models.CharField(max_length=50, db_column='NATIONALITY', default='INDIAN')
    BLOOD_GR = models.CharField(max_length=5, db_column='BLOOD_GR', default='O+')
    CASTE = models.CharField(max_length=50, db_column='CASTE', default='GENERAL')
    BRANCH_ID = models.ForeignKey(
        'accounts.BRANCH',
        to_field='BRANCH_ID',
        on_delete=models.PROTECT,
        db_column='BRANCH_ID'
    )
    ENROLMENT_NO = models.CharField(max_length=20, db_column='ENROLMENT_NO', blank=True, default='')
    IS_ACTIVE = models.CharField(max_length=8, db_column='IS_ACTIVE', default='YES')
    HANDICAPPED = models.CharField(max_length=10, db_column='HANDICAPPED', default='NO')
    MARK_ID = models.CharField(max_length=20, db_column='MARK_ID', blank=True, default='0')
    ADMISSION_DATE = models.DateField(db_column='ADMISSION_DATE', default=timezone.now)
    QUOTA_ID = models.IntegerField(db_column='QUOTA_ID', default=1)
    
    PER_PIN = models.CharField(max_length=6, db_column='PER_PIN', blank=True, default='')
    LOC_PIN = models.CharField(max_length=6, db_column='LOC_PIN', blank=True, default='')
    YEAR_SEM_ID = models.IntegerField(db_column='YEAR_SEM_ID', default=1)
    DATE_LEAVING = models.DateField(db_column='DATE_LEAVING', null=True, blank=True)
    RELIGION = models.CharField(max_length=50, db_column='RELIGION', blank=True, default='')
    DOB_WORD = models.CharField(max_length=100, db_column='DOB_WORD', blank=True, default='')
    ADMN_ROUND = models.CharField(max_length=10, db_column='ADMN_ROUND', default='1')
    BANK_NAME = models.CharField(max_length=100, db_column='BANK_NAME', blank=True, default='')
    BANK_ACC_NO = models.CharField(max_length=20, db_column='BANK_ACC_NO', blank=True, default='')
    EMERGENCY_NO = models.CharField(max_length=15, db_column='EMERGENCY_NO', blank=True, default='')
    PER_TALUKA = models.CharField(max_length=50, db_column='PER_TALUKA', blank=True, default='')
    PER_DIST = models.CharField(max_length=50, db_column='PER_DIST', blank=True, default='')
    LOC_TALUKA = models.CharField(max_length=50, db_column='LOC_TALUKA', blank=True, default='')
    LOC_DIST = models.CharField(max_length=50, db_column='LOC_DIST', blank=True, default='')
    EDITPERSON = models.CharField(max_length=100, db_column='EDITPERSON', default='SYSTEM')
    ADMN_QUOTA_ID = models.IntegerField(db_column='ADMN_QUOTA_ID', default=0)
    STATUS = models.CharField(max_length=20, db_column='STATUS', default='ACTIVE')
    JOINING_STATUS = models.CharField(max_length=20, db_column='JOINING_STATUS', default='JOINED')
    REGISTRATION_DATE = models.DateField(db_column='REGISTRATION_DATE', default=timezone.now)
    LATERAL_STATUS = models.CharField(max_length=20, db_column='LATERAL_STATUS', default='NO')
    JOINING_STATUS_DATE = models.DateField(db_column='JOINING_STATUS_DATE', default=timezone.now)
    RETENTION_STATUS_DATE = models.DateField(db_column='RETENTION_STATUS_DATE', default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.STUDENT_ID:
            latest_entry = STUDENT_MASTER.objects.filter(
                BATCH=self.BATCH, 
                BRANCH_ID=self.BRANCH_ID
            ).count() + 1
            program_code = self.BRANCH_ID.PROGRAM_id
            self.STUDENT_ID = f"{program_code}{self.BATCH[-2:]}{latest_entry:03d}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = '"STUDENT"."STUDENT_MASTER"'
        verbose_name = 'Student Master'
        verbose_name_plural = 'Student Masters'
        indexes = [
            models.Index(fields=['STUDENT_ID']),
            models.Index(fields=['EMAIL_ID']),
            models.Index(fields=['MOB_NO'])
        ]

    def __str__(self):
        return f"{self.STUDENT_ID} - {self.NAME} {self.SURNAME}"
    

class STUDENT_ROLL_NUMBER_DETAILS(AuditModel):
    RECORD_ID = models.AutoField(primary_key=True, db_column='RECORD_ID')
    INSTITUTE = models.ForeignKey(INSTITUTE, on_delete=models.PROTECT, db_column='INSTITUTE_ID')
    BRANCH = models.ForeignKey(BRANCH, on_delete=models.PROTECT, db_column='BRANCH_ID')
    YEAR = models.ForeignKey(YEAR, on_delete=models.PROTECT, db_column='YEAR_ID')
    STUDENT = models.ForeignKey(STUDENT, on_delete=models.PROTECT, db_column='STUDENT_ID')
    ACADEMIC_YEAR = models.ForeignKey(ACADEMIC_YEAR, on_delete=models.PROTECT, db_column='ACADEMIC_YEAR_ID')
    ROLL_NO = models.CharField(max_length=20, db_column='ROLLNO')  # Fixed max_length
    SEMESTER = models.ForeignKey(SEMESTER, on_delete=models.PROTECT, db_column='SEMESTER_ID')

    class Meta:
        db_table = '"STUDENT"."STUDENT_ROLL_NUMBER_DETAILS"'  # Removed schema to avoid Django issues
        verbose_name = 'Student Roll Number Details'
        verbose_name_plural = 'Student Roll Number Details'

    def __str__(self):
        return f"{self.STUDENT.ENROLLMENT_NO} - {self.ROLL_NO}"
