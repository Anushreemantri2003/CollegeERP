from rest_framework import serializers
from .models import COUNTRY, STATE, CITY, CURRENCY, LANGUAGE, DESIGNATION, CATEGORY, UNIVERSITY, INSTITUTE, DEPARTMENT, PROGRAM,BRANCH, YEAR,SEMESTER,ACADEMIC_YEAR,SEMESTER_DURATION

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = COUNTRY
        fields = ['COUNTRY_ID', 'NAME', 'CODE', 'PHONE_CODE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = STATE
        fields = ['STATE_ID', 'COUNTRY', 'NAME', 'CODE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CITY
        fields = ['CITY_ID', 'STATE', 'NAME', 'CODE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CURRENCY
        fields = ['CURRENCY_ID', 'NAME', 'CODE', 'SYMBOL', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LANGUAGE
        fields = ['LANGUAGE_ID', 'NAME', 'CODE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DESIGNATION
        fields = ['DESIGNATION_ID', 'NAME', 'CODE', 'DESCRIPTION', 'PERMISSIONS', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CATEGORY
        fields = ['CATEGORY_ID', 'NAME', 'CODE', 'DESCRIPTION', 'RESERVATION_PERCENTAGE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

    def validate(self, data):
        # Validate code format
        if 'CODE' in data:
            data['CODE'] = data['CODE'].upper()
            if not data['CODE'].isalnum():
                raise serializers.ValidationError({
                    "error": "Invalid format",
                    "message": "Category code must contain only letters and numbers",
                    "field": "CODE"
                })

            # Check for existing code
            code = data['CODE']
            if self.instance is None:  # Only for creation
                if CATEGORY.objects.filter(CODE=code).exists():
                    raise serializers.ValidationError({
                        "error": "Duplicate entry",
                        "message": f"Category with code '{code}' already exists",
                        "field": "CODE"
                    })

        # Validate reservation percentage
        if 'RESERVATION_PERCENTAGE' in data:
            try:
                percentage = float(data['RESERVATION_PERCENTAGE'])
                if not (0 <= percentage <= 100):
                    raise serializers.ValidationError({
                        "error": "Invalid value",
                        "message": "Reservation percentage must be between 0 and 100",
                        "field": "RESERVATION_PERCENTAGE"
                    })
            except (TypeError, ValueError):
                raise serializers.ValidationError({
                    "error": "Invalid format",
                    "message": "Reservation percentage must be a valid number",
                    "field": "RESERVATION_PERCENTAGE"
                })

        return data

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UNIVERSITY
        fields = [
            'UNIVERSITY_ID', 'NAME', 'CODE', 'ADDRESS', 
            'CONTACT_NUMBER', 'EMAIL', 'WEBSITE', 'ESTD_YEAR', 
            'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY'
        ]

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = INSTITUTE
        fields = [
            'INSTITUTE_ID', 'UNIVERSITY', 'NAME', 'CODE',
            'ADDRESS', 'CONTACT_NUMBER', 'EMAIL', 'WEBSITE',
            'ESTD_YEAR', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY'
        ]
                
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACADEMIC_YEAR
        fields = [
            'ACADEMIC_YEAR', 'START_DATE', 'END_DATE',
            'INSTITUTE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY'
        ]

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DEPARTMENT
        fields = ['DEPARTMENT_ID', 'INSTITUTE_CODE', 'NAME', 'CODE', 'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY']

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = PROGRAM
        fields = [
    'PROGRAM_ID', 'INSTITUTE', 'NAME', 'CODE', 
    'DURATION_YEARS', 'LEVEL', 'TYPE', 'DESCRIPTION',
    'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY'
]

class BranchSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    PROGRAM = ProgramSerializer(read_only=True)  # ✅ Use YearSerializer
=======
    PROGRAM_CODE = serializers.CharField(source='PROGRAM.CODE', read_only=True)
    INSTITUTE_CODE = serializers.CharField(source='PROGRAM.INSTITUTE.CODE', read_only=True)
    
>>>>>>> 1405027219c9a09e33f40ef845f6a2c491673eb1
    class Meta:
        model = BRANCH
        fields = [
            'BRANCH_ID', 'PROGRAM', 'NAME', 'CODE',
            'DESCRIPTION', 'IS_ACTIVE', 'CREATED_BY',
            'UPDATED_BY', 'PROGRAM_CODE', 'INSTITUTE_CODE'
        ]
        

class YearSerializer(serializers.ModelSerializer):
    # BRANCH = BranchSerializer(read_only=True)  # ✅ Use BranchSerializer
    class Meta:
        model = YEAR
        fields =  ['YEAR_ID','YEAR','BRANCH']
    
    def validate_BRANCH_ID(self, value):
        if not value:
            raise serializers.ValidationError("Branch ID is required.")
        return value
        
class SemesterSerializer(serializers.ModelSerializer):
    # YEAR = YearSerializer(read_only=True)  # ✅ Use YearSerializer
   
    class Meta:
        model = SEMESTER
<<<<<<< HEAD
        fields = ['SEMESTER_ID','SEMESTER','YEAR']
   
        

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = COURSE
#         fields = ['COURSE_ID','SEMESTER_NAME','NAME',
#         'CODE','CREDITS','THEORY_MARKS','PRACTICAL_MARKS',
#         'IS_ELECTIVE','IS_ACTIVE','SEMESTER_ID'
#         ]
=======
        fields = ['SEMESTER_ID','SEMESTER','YEAR'
        ]
>>>>>>> 1405027219c9a09e33f40ef845f6a2c491673eb1

class SemesterDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEMESTER_DURATION
        fields = [
            'SEMESTER', 'START_DATE', 'END_DATE', 
            'IS_ACTIVE', 'CREATED_BY', 'UPDATED_BY'
        ]