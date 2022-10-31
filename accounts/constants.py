PAGE_SIZE = 30

"""
user role type name
"""
USER_ROLE = ((1, "Admin"),(2,"Customer"),(3,"ServiceProvider"))
ADMIN = 1
CUSTOMER = 2
SERVICE_PROVIDER = 3


"""
Service Provider Roles
"""
SERVICE_USER_ROLE = ((1, "Hospital"), (2, "Clinic"), (3, "Saloon"), (4, "Banks"))
HOSPITAL_USER = 1
CLINIC_USER = 2
SALOON_USER = 3
BANK_USER = 4


"""
User Status
"""
USER_STATUS = ((1, "Active"),(2,"Inactive"),(3,"Deleted"))
ACTIVE = 1
INACTIVE = 2
DELETED = 3


"""
USER GENDER
"""
GENDER = ((1, "Male"), (2, "Female"), (3, "Other"))
MALE = 1
FEMALE = 2
OTHER = 3


"""
Page Type
"""
PAGE_TYPE =  ((1,"Terms_And_Condition"),(2,"Privacy_Policy"),(3, "About_Us"))
TERMS_AND_CONDITION = 1
PRIVACY_POLITY  = 2
ABOUT_US  = 3


"""
Login History
"""
LOGIN_STATUS = ((1,'LOGIN_SUCCESS'),(2,'LOGIN_FAILURE'))
LOGIN_SUCCESS = 1
LOGIN_FAILURE = 2


"""
Device Types
"""
DEVICE_TYPE = ((1, 'Aandroid'), (2, 'IOS'))
ANDROID = 1
IOS = 2


"""
Social Login Types
"""
SOCIAL_TYPE = ((1,'Google'), (2, 'Apple'))
GOOGLE_LOGIN = 1
APPLE_LOGIN = 2
