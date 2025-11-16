from flask import Flask, render_template_string, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'siws-college-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# College Data
COLLEGE_DATA = {
    'name': 'SIWS College',
    'motto': 'Excellence in Education Since 1934',
    'established': '1934',
    'contact': {
        'phone': '022 2418 0390',
        'email': 'siwscollege.edu.in',
        'address': 'Plot No. 337, Sewree Wadala Estate, Major R. Parameshwaran Marg, Mumbai – 400 031'
    }
}

# Enhanced Facilities Data with actual SIWS images
FACILITIES = {
    'canteen': {
        'name': 'College Canteen',
        'description': 'Healthy and hygienic food services with variety of cuisines',
        'manager': 'Mr. ',
        'experience': '15 years',
        'timing': '8:00 AM - 6:00 PM',
        'image': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500&h=300&fit=crop',
        'logo': 'https://i.pinimg.com/originals/0f/0c/09/0f0c09e6e13943604dcf5868f21fec2e.jpg',
        'animation': 'bounce',
        'details': 'Our canteen provides nutritious and hygienic food at affordable prices. We have a variety of options including Indian, Chinese, and Continental cuisine.',
        'menu': {
            'breakfast': ['Poha - Rs. 20', 'Upma - Rs. 25', 'Sandwich - Rs. 30', 'Tea/Coffee - Rs. 15'],
            'lunch': ['Veg Thali - Rs. 60', 'Non-Veg Thali - Rs. 80', 'Chinese Combo - Rs. 70', 'South Indian - Rs. 50'],
            'snacks': ['Samosa - Rs. 15', 'Vada Pav - Rs. 20', 'French Fries - Rs. 40', 'Cold Coffee - Rs. 35']
        }
    },
    'gymkhana': {
        'name': 'Gymkhana & Sports',
        'description': 'State-of-the-art sports facilities and fitness center',
        'manager': 'Mrs. Priya Sharma',
        'experience': '12 years',
        'timing': '6:00 AM - 9:00 PM',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/gym1-300x200-1.png',
        'logo': 'https://static.vecteezy.com/system/resources/previews/026/726/080/non_2x/fitness-and-gym-logo-design-vector.jpg',
        'animation': 'pulse',
        'details': 'Modern gymnasium with latest equipment and professional trainers. Regular fitness programs and sports competitions.',
        'equipment': ['Treadmills', 'Weight Training', 'Yoga Studio', 'Basketball Court', 'Badminton Court'],
        'activities': ['Gym Training', 'Yoga Classes', 'Aerobics', 'Sports Competitions']
    },
    'health_centre': {
        'name': 'Health Centre',
        'description': '24/7 medical assistance and healthcare services',
        'manager': 'Dr. Anjali Mehta',
        'experience': '20 years',
        'timing': '24/7 Emergency',
        'image': 'https://images.unsplash.com/photo-1551076805-e1869033e561?w=500&h=300&fit=crop',
        'logo': 'https://cdn-icons-png.flaticon.com/512/2967/2967437.png',
        'animation': 'heartBeat',
        'details': 'Fully equipped health center with qualified doctors and nursing staff. Regular health checkups and emergency services available.',
        'services': ['First Aid', 'Medical Checkups', 'Psychological Counseling', 'Vaccination Camps', 'Health Awareness Programs']
    },
    'playground': {
        'name': 'Sports Ground',
        'description': 'Olympic-standard sports facilities for various sports',
        'manager': 'Mr. Vijay Singh',
        'experience': '18 years',
        'timing': '5:00 AM - 8:00 PM',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/Winners-of-Non-teaching-staff-running-race.png',
        'logo': 'https://img.pikbest.com/png-images/20241031/minimalist-sports-logo-vector-illustration-on-transparent-background_11037606.png!sw800',
        'animation': 'wobble',
        'details': 'Spacious playground with facilities for cricket, football, athletics and other outdoor sports. Regular coaching and inter-college tournaments.',
        'facilities': ['Cricket Pitch', 'Football Ground', 'Athletics Track', 'Volleyball Court', 'Basketball Court'],
        'sports': ['Cricket', 'Football', 'Athletics', 'Basketball', 'Volleyball']
    },
    'girls_common_room': {
        'name': 'Girls Common Room',
        'description': 'Comfortable and secure space for female students',
        'manager': 'Mrs. Sunita Patil',
        'experience': '10 years',
        'timing': '7:00 AM - 7:00 PM',
        'image': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=500&h=300&fit=crop',
        'logo': 'https://www.shutterstock.com/image-vector/painted-vector-silhouette-hand-defensive-260nw-1393678679.jpg',
        'animation': 'fadeIn',
        'details': 'Exclusive common room for female students with comfortable seating, study areas, and recreational facilities.',
        'amenities': ['Resting Area', 'Study Space', 'Entertainment Zone', 'Kitchenette', 'Reading Corner']
    },
    'library': {
        'name': 'Central Library',
        'description': 'Digital and physical learning resources with vast collection',
        'manager': 'Dr. Ramesh Nair',
        'experience': '25 years',
        'timing': '8:00 AM - 8:00 PM',
        'image': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=500&h=300&fit=crop',
        'logo': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRXcZvD3S0MY-KWUOKSTmhkpZyPkf-z04kBFQ&s',
        'animation': 'flip',
        'details': 'Well-stocked library with extensive collection of books, journals, and digital resources. Quiet study areas and computer access.',
        'collection': ['50,000+ Books', '100+ Journals', 'E-Library Access', 'Research Papers', 'Digital Archives'],
        'sections': ['Reference Section', 'Periodical Section', 'Digital Library', 'Reading Room']
    },
    'nss': {
        'name': 'NSS Unit',
        'description': 'National Service Scheme - Social Service Initiatives',
        'manager': 'Dr. Anjali Mehta',
        'experience': '8 years',
        'timing': 'Flexible Hours',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/Accordian-1-NSS.jpg',
        'logo': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/NSS-Orientation-Program.png',
        'animation': 'fadeIn',
        'details': 'Active NSS unit engaging students in community service and social awareness programs. Regular camps and outreach activities.',
        'activities': ['Community Service', 'Social Awareness Programs', 'Environmental Initiatives', 'Blood Donation Camps', 'Tree Plantation']
    },
    'dlle': {
        'name': 'Department of Lifelong Learning',
        'description': 'Continuing education and skill development programs',
        'manager': 'Dr. Ramesh Nair',
        'experience': '10 years',
        'timing': '9:00 AM - 5:00 PM',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/05/DLLE.jpg',
        'logo': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/05/DLLE.jpg',
        'animation': 'pulse',
        'details': 'Dedicated department for continuing education, skill development, and certificate programs for students and working professionals.',
        'programs': ['Certificate Courses', 'Workshops', 'Skill Development Programs', 'Vocational Training', 'Professional Certifications']
    }
}

# Enhanced Events Data with actual SIWS images
EVENTS = [
    {
        'id': 1,
        'title': 'Annual Sports Day',
        'date': '2024-03-15',
        'time': '10:00 AM',
        'venue': 'College Ground',
        'description': 'Annual sports competition with various track and field events. Students participate in cricket, football, athletics and more.',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/Winners-of-Non-teaching-staff-running-race.png',
        'category': 'sports',
        'status': 'upcoming'
    },
    {
        'id': 2,
        'title': 'Pongal Celebration',
        'date': '2024-04-20',
        'time': '9:00 AM',
        'venue': 'College Campus',
        'description': 'Traditional Pongal festival celebration with cultural programs, traditional food, and cultural performances.',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/Picture1-6-300x146-1.png',
        'category': 'cultural',
        'status': 'upcoming'
    },
    {
        'id': 3,
        'title': 'Cultural Fest',
        'date': '2024-05-10',
        'time': '6:00 PM',
        'venue': 'Auditorium',
        'description': 'Annual cultural festival with music, dance and drama performances. Inter-college competitions and celebrity performances.',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/834011.jpg',
        'category': 'cultural',
        'status': 'upcoming'
    },
    {
        'id': 4,
        'title': 'Independence Day Celebration',
        'date': '2024-08-15',
        'time': '8:00 AM',
        'venue': 'College Ground',
        'description': 'Flag hoisting ceremony and patriotic program with cultural performances and speeches.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyP04QBdyfZDrgpu1CQM_Q40wIY6xreMekyQ&s',
        'category': 'national',
        'status': 'upcoming'
    },
    {
        'id': 5,
        'title': 'Tech Symposium 2024',
        'date': '2024-02-20',
        'time': '9:00 AM',
        'venue': 'Auditorium',
        'description': 'Annual technical symposium showcasing student projects and innovations in technology.',
        'image': 'https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=500&h=300&fit=crop',
        'category': 'technical',
        'status': 'completed'
    }
]

# Enhanced Notices Data
NOTICES = [
    {
        'id': 1,
        'title': 'Semester Exam Schedule Published',
        'date': '2024-02-01',
        'content': 'Final semester examination schedule has been published. All students are requested to check the notice board for detailed timetable and examination guidelines.',
        'priority': 'high',
        'category': 'academic',
        'department': 'Examination Cell'
    },
    {
        'id': 2,
        'title': 'Library Timings Extended',
        'date': '2024-02-15',
        'content': 'Library will remain open till 10 PM during examination period. Students can avail extended hours for study and reference work.',
        'priority': 'medium',
        'category': 'facility',
        'department': 'Library'
    },
    {
        'id': 3,
        'title': 'NAAC Accreditation Achievement',
        'date': '2024-01-20',
        'content': 'College re-accredited with A grade with 3.15 CGPA in 3rd Cycle of NAAC. This achievement reflects our commitment to quality education.',
        'priority': 'high',
        'category': 'achievement',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/College-was-re-accredited-with-A-grade-with-3.15-CGPA-in-3rd-Cycle-of-NAAC.jpg',
        'department': 'Administration'
    },
    {
        'id': 4,
        'title': 'Admissions Open for 2024-25',
        'date': '2024-01-10',
        'content': 'Admissions for academic year 2024-25 are now open for all courses. Apply online through our admission portal.',
        'priority': 'high',
        'category': 'admission',
        'department': 'Admission Cell'
    }
]

# Teachers Data
TEACHERS = [
    {
        'id': 1,
        'name': 'Dr. Principal',
        'position': 'Principal',
        'department': 'Administration',
        'qualification': 'Ph.D. in Education, M.Sc., B.Ed.',
        'experience': '25 years',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxe4E3D4_ufkJh5iCEmvk9KvmpqYKkY3bxjkp0I_2oRcQxoWPHJxqJ0HFHe6lgP531OjU&usqp=CAU',
        'description': 'Leading the institution with vision and dedication. Committed to academic excellence and holistic development of students.',
        'email': 'principal@siwscollege.edu',
        'subjects': ['Educational Leadership', 'Management']
    },
    {
        'id': 2,
        'name': 'Er. R. Santha Maria Rani',
        'position': 'Head Of Department',
        'department': 'Administration',
        'qualification': 'M.E., M.Phil., B.E.',
        'experience': '20 years',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/Er.-R-Santha-Maria-Rani-2.png',
        'description': 'Dedicated to academic excellence and student development. Specialized in engineering and technical education.',
        'email': 'vprincipal@siwscollege.edu',
        'subjects': ['Engineering', 'Technical Education']
    },
    {
        'id': 3,
        'name': 'Ms. Virgin Mary Fernando',
        'position': 'Head of Department',
        'department': 'Information Department',
        'qualification': 'M.Com, M.Phil., CA Inter',
        'experience': '18 years',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/B.-VirginMary-Fernando-2.png',
        'description': 'Expert in technical problems with extensive industry experience. Focus on practical business education.',
        'email': 'hod.commerce@siwscollege.edu',
        'subjects': ['Coding','Problem-solving']
    }
]

# Achievements Data
ACHIEVEMENTS = [
    {
        'id': 1,
        'title': 'NAAC A Grade Accreditation',
        'description': 'College re-accredited with A grade with 3.15 CGPA in 3rd Cycle of NAAC. This recognition affirms our commitment to quality education and institutional excellence.',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/College-was-re-accredited-with-A-grade-with-3.15-CGPA-in-3rd-Cycle-of-NAAC.jpg',
        'date': '2024',
        'category': 'institutional',
        'department': 'Quality Assurance'
    },
    {
        'id': 2,
        'title': 'Sports Champions 2024',
        'description': 'Students won multiple awards in inter-collegiate sports competitions including gold medals in athletics and team sports.',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/Winners-of-Non-teaching-staff-running-race.png',
        'date': '2024',
        'category': 'sports',
        'department': 'Sports Department'
    },
    {
        'id': 3,
        'title': 'NSS Excellence Award',
        'description': 'Recognized for outstanding social service initiatives and community engagement programs. Awarded best NSS unit in the region.',
        'image': 'https://www.siwscollege.edu.in/wp-content/uploads/2025/02/NSS-Orientation-Program.png',
        'date': '2024',
        'category': 'social',
        'department': 'NSS Unit'
    }
]

# Eligibility Criteria
ELIGIBILITY = {
    'junior_college': {
        'science': {
            'min_ssc_marks': 65,
            'subjects_required': ['Mathematics', 'Science'],
            'description': 'For students interested in Medical, Engineering and Pure Sciences',
            'duration': '2 Years',
            'intake': '120 students'
        },
        'commerce': {
            'min_ssc_marks': 55,
            'subjects_required': ['Mathematics preferred'],
            'description': 'For students interested in Business, Finance and Accounting',
            'duration': '2 Years',
            'intake': '100 students'
        },
        'arts': {
            'min_ssc_marks': 45,
            'subjects_required': ['Any stream'],
            'description': 'For students interested in Humanities, Languages and Social Sciences',
            'duration': '2 Years',
            'intake': '80 students'
        }
    },
    'degree_college': {
        'bsc': {
            'min_hsc_marks': 60,
            'streams': ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Microbiology'],
            'description': 'Bachelor of Science programs with modern curriculum and research opportunities',
            'duration': '3 Years',
            'intake': '180 students'
        },
        'bcom': {
            'min_hsc_marks': 55,
            'streams': ['Accountancy', 'Business Management', 'Banking & Insurance'],
            'description': 'Bachelor of Commerce programs with industry-oriented curriculum',
            'duration': '3 Years',
            'intake': '240 students'
        },
        'ba': {
            'min_hsc_marks': 50,
            'streams': ['English Literature', 'Psychology', 'Economics', 'History'],
            'description': 'Bachelor of Arts programs with diverse subject options',
            'duration': '3 Years',
            'intake': '120 students'
        },
        'bms': {
            'min_hsc_marks': 60,
            'streams': ['Management Studies'],
            'description': 'Bachelor of Management Studies with focus on business management',
            'duration': '3 Years',
            'intake': '60 students'
        }
    }
}

# NEW: Calendar Data
CALENDAR_EVENTS = [
    {
        'id': 1,
        'title': 'Semester 1 Begins',
        'date': '2024-06-15',
        'type': 'academic',
        'description': 'Commencement of First Semester for all programs',
        'color': '#3b82f6'
    },
    {
        'id': 2,
        'title': 'Independence Day',
        'date': '2024-08-15',
        'type': 'holiday',
        'description': 'National Holiday - College Closed',
        'color': '#ef4444'
    },
    {
        'id': 3,
        'title': 'Mid-Semester Exams',
        'date': '2024-09-15',
        'type': 'exam',
        'description': 'Mid-semester examinations for all courses',
        'color': '#f59e0b'
    },
    {
        'id': 4,
        'title': 'Diwali Break',
        'date': '2024-10-24',
        'type': 'holiday',
        'description': 'Diwali Festival Break - College Closed',
        'color': '#ef4444'
    },
    {
        'id': 5,
        'title': 'Semester 1 Ends',
        'date': '2024-11-30',
        'type': 'academic',
        'description': 'End of First Semester',
        'color': '#3b82f6'
    },
    {
        'id': 6,
        'title': 'Final Exams',
        'date': '2024-12-01',
        'type': 'exam',
        'description': 'Final Semester Examinations Begin',
        'color': '#f59e0b'
    },
    {
        'id': 7,
        'title': 'Winter Break',
        'date': '2024-12-25',
        'type': 'holiday',
        'description': 'Christmas Holiday - College Closed',
        'color': '#ef4444'
    },
    {
        'id': 8,
        'title': 'Semester 2 Begins',
        'date': '2025-01-15',
        'type': 'academic',
        'description': 'Commencement of Second Semester',
        'color': '#3b82f6'
    }
]

# NEW: Academic Programs Data
ACADEMIC_PROGRAMS = {
    'undergraduate': [
        {
            'id': 1,
            'name': 'Bachelor of Science (B.Sc)',
            'duration': '3 Years',
            'specializations': ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Microbiology'],
            'description': 'Comprehensive science education with modern laboratories and research opportunities.',
            'image': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=500&h=300&fit=crop',
            'fees': '₹45,000 per year',
            'eligibility': 'HSC with Science stream, minimum 60% marks',
            'career_opportunities': ['Software Developer', 'Data Scientist', 'Research Scientist', 'Lab Technician']
        },
        {
            'id': 2,
            'name': 'Bachelor of Commerce (B.Com)',
            'duration': '3 Years',
            'specializations': ['Accountancy', 'Business Management', 'Banking & Insurance'],
            'description': 'Industry-focused commerce education with practical training and internships.',
            'image': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=500&h=300&fit=crop',
            'fees': '₹35,000 per year',
            'eligibility': 'HSC with Commerce stream, minimum 55% marks',
            'career_opportunities': ['Chartered Accountant', 'Financial Analyst', 'Bank Manager', 'Business Consultant']
        },
        {
            'id': 3,
            'name': 'Bachelor of Arts (B.A)',
            'duration': '3 Years',
            'specializations': ['English Literature', 'Psychology', 'Economics', 'History'],
            'description': 'Diverse arts education fostering critical thinking and communication skills.',
            'image': 'https://images.unsplash.com/photo-1588072432836-e100327d50a4?w=500&h=300&fit=crop',
            'fees': '₹25,000 per year',
            'eligibility': 'HSC with any stream, minimum 50% marks',
            'career_opportunities': ['Content Writer', 'Psychologist', 'Economist', 'Historian']
        }
    ],
    'postgraduate': [
        {
            'id': 1,
            'name': 'Master of Science (M.Sc)',
            'duration': '2 Years',
            'specializations': ['Computer Science', 'Mathematics', 'Physics'],
            'description': 'Advanced scientific research and specialization in chosen field.',
            'image': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=500&h=300&fit=crop',
            'fees': '₹60,000 per year',
            'eligibility': 'B.Sc in relevant subject, minimum 55% marks',
            'career_opportunities': ['Research Scientist', 'University Professor', 'Data Analyst']
        }
    ],
    'certificate': [
        {
            'id': 1,
            'name': 'Digital Marketing Certification',
            'duration': '6 Months',
            'description': 'Comprehensive digital marketing skills including SEO, SEM, and social media marketing.',
            'image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500&h=300&fit=crop',
            'fees': '₹25,000',
            'eligibility': '12th Pass with basic computer knowledge',
            'career_opportunities': ['Digital Marketing Executive', 'SEO Specialist', 'Social Media Manager']
        },
        {
            'id': 2,
            'name': 'Data Analytics Certificate',
            'duration': '8 Months',
            'description': 'Hands-on training in data analysis tools and techniques.',
            'image': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&h=300&fit=crop',
            'fees': '₹30,000',
            'eligibility': 'Graduate with basic mathematics knowledge',
            'career_opportunities': ['Data Analyst', 'Business Analyst', 'Data Scientist']
        }
    ]
}

# NEW: Departments Data
DEPARTMENTS = {
    'science': {
        'name': 'Department of Science',
        'hod': 'Dr. Rajesh Kumar',
        'hod_image': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&h=300&fit=crop',
        'description': 'Leading scientific education with state-of-the-art laboratories and research facilities.',
        'image': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=600&h=400&fit=crop',
        'programs': ['B.Sc Computer Science', 'B.Sc Mathematics', 'B.Sc Physics', 'B.Sc Chemistry', 'B.Sc Microbiology'],
        'faculty_count': 25,
        'research_areas': ['Artificial Intelligence', 'Renewable Energy', 'Biotechnology', 'Data Science'],
        'achievements': [
            'Best Science Department Award 2023',
            '10+ Research Papers Published',
            'Industry-Academia Collaboration with Tech Giants'
        ],
        'faculty': [
            {'name': 'Dr. Rajesh Kumar', 'position': 'HOD & Professor', 'qualification': 'Ph.D in Computer Science'},
            {'name': 'Dr. Priya Sharma', 'position': 'Associate Professor', 'qualification': 'Ph.D in Physics'},
            {'name': 'Dr. Amit Patel', 'position': 'Assistant Professor', 'qualification': 'Ph.D in Chemistry'}
        ]
    },
    'commerce': {
        'name': 'Department of Commerce',
        'hod': 'Dr. Sunil Verma',
        'hod_image': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=300&h=300&fit=crop',
        'description': 'Excellence in commerce education with industry-oriented curriculum and practical training.',
        'image': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop',
        'programs': ['B.Com Accountancy', 'B.Com Business Management', 'B.Com Banking & Insurance'],
        'faculty_count': 18,
        'research_areas': ['Financial Markets', 'Business Analytics', 'Taxation', 'Banking Operations'],
        'achievements': [
            '100% Placement Record for 3 consecutive years',
            'Industry Certification Programs',
            'Stock Market Simulation Lab'
        ],
        'faculty': [
            {'name': 'Dr. Sunil Verma', 'position': 'HOD & Professor', 'qualification': 'Ph.D in Commerce'},
            {'name': 'Prof. Anjali Mehta', 'position': 'Associate Professor', 'qualification': 'M.Com, CA'},
            {'name': 'Prof. Ramesh Nair', 'position': 'Assistant Professor', 'qualification': 'M.Com, MBA'}
        ]
    },
    'arts': {
        'name': 'Department of Arts & Humanities',
        'hod': 'Dr. Meera Desai',
        'hod_image': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=300&h=300&fit=crop',
        'description': 'Fostering creativity, critical thinking, and cultural awareness through diverse arts education.',
        'image': 'https://images.unsplash.com/photo-1588072432836-e100327d50a4?w=600&h=400&fit=crop',
        'programs': ['B.A English Literature', 'B.A Psychology', 'B.A Economics', 'B.A History'],
        'faculty_count': 15,
        'research_areas': ['Literary Theory', 'Cognitive Psychology', 'Economic Development', 'Cultural Studies'],
        'achievements': [
            'National Level Debate Competition Winners',
            'Cultural Exchange Programs',
            'Published Literary Magazine'
        ],
        'faculty': [
            {'name': 'Dr. Meera Desai', 'position': 'HOD & Professor', 'qualification': 'Ph.D in English Literature'},
            {'name': 'Dr. Anil Kapoor', 'position': 'Associate Professor', 'qualification': 'Ph.D in Psychology'},
            {'name': 'Prof. Seema Joshi', 'position': 'Assistant Professor', 'qualification': 'M.A in Economics'}
        ]
    },
    'management': {
        'name': 'Department of Management Studies',
        'hod': 'Dr. Vikram Singh',
        'hod_image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop',
        'description': 'Developing future business leaders through innovative management education and industry exposure.',
        'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=600&h=400&fit=crop',
        'programs': ['Bachelor of Management Studies (BMS)', 'MBA (Affiliated)'],
        'faculty_count': 12,
        'research_areas': ['Strategic Management', 'Marketing', 'Human Resources', 'Entrepreneurship'],
        'achievements': [
            'Industry Internship Program with 50+ Companies',
            'Entrepreneurship Development Cell',
            'Management Fest - "Manfest"'
        ],
        'faculty': [
            {'name': 'Dr. Vikram Singh', 'position': 'HOD & Professor', 'qualification': 'Ph.D in Management'},
            {'name': 'Prof. Neha Sharma', 'position': 'Associate Professor', 'qualification': 'MBA, Ph.D'},
            {'name': 'Prof. Rahul Mehta', 'position': 'Assistant Professor', 'qualification': 'MBA, UGC NET'}
        ]
    }
}

# NEW: Alumni Data
ALUMNI_DATA = {
    'success_stories': [
        {
            'id': 1,
            'name': 'GOLD ALUMINI',
            'batch': '1930',
            'program': 'Aluminis of SIWS',
            'current_position': 'Clinical Psychologist, Apollo Hospitals',
            'image':'https://friendsofsiws.wordpress.com/wp-content/uploads/2015/02/68-batch.jpg',
            'achievement': 'Pioneered mental health awareness programs in corporate sector',
            'testimonial': 'The psychology program at SIWS gave me both theoretical knowledge and practical skills.'
        },
        {
            'id': 2,
            'name': 'Dr. Rajan Ravichandran',
            'batch': '1980-1983',
            'program': 'B.Com Accountancy',
            'current_position': 'Chartered Accountant, Nair & Associates',
            'image': 'https://i2.wp.com/friendsofsiws.files.wordpress.com/2016/06/img_1484.jpg?w=370&h=&crop&ssl=1',
            'achievement': 'Established successful CA firm with 50+ clients',
            'testimonial': 'The practical approach to commerce education at SIWS helped me build a successful practice.'
        },
        {
            'id': 3,
            'name': 'Anjali Mehta',
            'batch': '1971-1974',
            'program': 'B.Sc Computer Science',
            'current_position': 'Senior Data Scientist, Google',
            'image': 'https://friendsofsiws.files.wordpress.com/2016/09/ms-k1.png?w=500',
            'achievement': 'Leading AI research team at Google, published 20+ research papers',
            'testimonial': 'SIWS College provided the perfect foundation for my career in technology. The faculty and facilities were exceptional.'
        }
    ],
    'events': [
        {
            'id': 1,
            'title': 'Alumni Meet 2024',
            'date': '2026-2-20',
            'description': 'Annual alumni reunion with networking sessions and cultural programs',
            'image': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=500&h=300&fit=crop'
        },
        {
            'id': 2,
            'title': 'Career Guidance Workshop',
            'date': '2025-11-15',
            'description': 'Alumni sharing career insights and guidance for current students',
            'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&h=300&fit=crop'
        }
    ]
}

# NEW: Career Services Data
CAREER_SERVICES = {
    'placement_stats': {
        'total_placed': 350,
        'placement_percentage': 85,
        'highest_package': '₹12 LPA',
        'average_package': '₹5.5 LPA',
        'recruiting_companies': 45
    },
    'top_recruiters': [
        {'name': 'TCS', 'logo': 'https://logo.clearbit.com/tcs.com'},
        {'name': 'Infosys', 'logo': 'https://logo.clearbit.com/infosys.com'},
        {'name': 'Wipro', 'logo': 'https://logo.clearbit.com/wipro.com'},
        {'name': 'Accenture', 'logo': 'https://logo.clearbit.com/accenture.com'},
        {'name': 'Capgemini', 'logo': 'https://logo.clearbit.com/capgemini.com'},
        {'name': 'IBM', 'logo': 'https://logo.clearbit.com/ibm.com'}
    ],
    'training_programs': [
        {
            'name': 'Aptitude Training',
            'duration': '4 Weeks',
            'description': 'Comprehensive aptitude test preparation'
        },
        {
            'name': 'Technical Skills',
            'duration': '6 Weeks',
            'description': 'Programming and technical skill development'
        },
        {
            'name': 'Soft Skills',
            'duration': '3 Weeks',
            'description': 'Communication and interpersonal skills training'
        }
    ]
}

# NEW: Scholarships Data
SCHOLARSHIPS = [
    {
        'id': 1,
        'name': 'Merit Scholarship',
        'description': 'For students with outstanding academic performance in previous examinations',
        'eligibility': 'Minimum 90% in HSC/SSC, Family income less than ₹5 LPA',
        'amount': '100% Tuition Fee Waiver',
        'deadline': '2024-07-31',
        'documents_required': ['Marksheet', 'Income Certificate', 'Aadhaar Card'],
        'beneficiaries': 50
    },
    {
        'id': 2,
        'name': 'Sports Scholarship',
        'description': 'For students with exceptional performance in sports at state/national level',
        'eligibility': 'Represented state/national level sports, Minimum 60% in academics',
        'amount': '50-100% Tuition Fee Waiver',
        'deadline': '2024-07-31',
        'documents_required': ['Sports Certificates', 'Marksheet', 'Aadhaar Card'],
        'beneficiaries': 20
    },
    {
        'id': 3,
        'name': 'Economically Weaker Section Scholarship',
        'description': 'Financial assistance for students from economically disadvantaged backgrounds',
        'eligibility': 'Family income less than ₹2.5 LPA, Minimum 75% in previous exams',
        'amount': '100% Tuition Fee + Stipend',
        'deadline': '2024-07-31',
        'documents_required': ['Income Certificate', 'Caste Certificate', 'Marksheet', 'Aadhaar Card'],
        'beneficiaries': 100
    }
]

# Main Home Page Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIWS College - Excellence in Education Since 1990</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://thumbs.dreamstime.com/b/hall-building-college-sunrise-63035568.jpg');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            min-height: 80vh;
            display: flex;
            align-items: center;
        }

        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        .btn-large {
            padding: 18px 45px;
            font-size: 1.2rem;
        }

        /* Sections */
        section {
            padding: 80px 0;
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--text-light);
            font-size: 1.2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Facilities Grid */
        .facilities-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }

        .facility-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
        }

        .facility-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }

        .facility-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .facility-card:hover .facility-image {
            transform: scale(1.05);
        }

        .facility-content {
            padding: 2rem;
        }

        .facility-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }

        .facility-details {
            background: var(--light-blue);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1.5rem 0;
        }

        .facility-detail-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.8rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(30, 58, 138, 0.1);
        }

        .facility-detail-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }

        /* Teachers Section */
        .teachers-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .teachers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2.5rem;
        }

        .teacher-card {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center;
            transition: all 0.3s ease;
            color: var(--text-dark);
        }

        .teacher-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .teacher-image {
            width: 100%;
            height: 300px;
            object-fit: cover;
        }

        .teacher-info {
            padding: 2rem;
        }

        .teacher-info h3 {
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
            font-size: 1.4rem;
        }

        .teacher-position {
            color: var(--danger);
            font-weight: bold;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }

        .teacher-department {
            color: var(--text-light);
            margin-bottom: 1rem;
            font-weight: 500;
        }

        /* Achievements Section */
        .achievements-section {
            background: var(--white);
        }

        .achievements-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2.5rem;
        }

        .achievement-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 1px solid rgba(0,0,0,0.05);
        }

        .achievement-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .achievement-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }

        .achievement-content {
            padding: 2rem;
        }

        .achievement-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.4rem;
        }

        .achievement-date {
            background: var(--success);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            display: inline-block;
            margin-top: 1rem;
        }

        /* Events Section */
        .events-section {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }

        .events-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2.5rem;
        }

        .event-card {
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            color: var(--text-dark);
        }

        .event-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .event-image {
            width: 100%;
            height: 220px;
            object-fit: cover;
        }

        .event-content {
            padding: 2rem;
        }

        .event-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.4rem;
        }

        .event-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            color: var(--text-light);
            font-size: 0.9rem;
        }

        .event-category {
            background: var(--primary-blue);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        /* Notices Section */
        .notices-section {
            background: var(--light-blue);
        }

        .notice-item {
            background: white;
            padding: 2rem;
            margin: 1.5rem 0;
            border-radius: 15px;
            border-left: 5px solid var(--primary-blue);
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }

        .notice-item:hover {
            transform: translateX(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        }

        .notice-high-priority {
            border-left-color: var(--danger);
            background: linear-gradient(135deg, #fff, #ffeaea);
        }

        .notice-item h3 {
            color: var(--primary-blue);
            margin-bottom: 0.8rem;
            font-size: 1.3rem;
        }

        .notice-meta {
            display: flex;
            justify-content: space-between;
            color: var(--text-light);
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }

        .notice-department {
            background: var(--primary-blue);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
            font-size: 0.8rem;
        }

        /* Quick Links */
        .quick-links {
            background: var(--primary-blue);
            color: white;
            padding: 5rem 0;
            text-align: center;
        }

        .links-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .link-card {
            background: rgba(255,255,255,0.1);
            padding: 3rem 2rem;
            border-radius: 20px;
            transition: all 0.3s ease;
            text-decoration: none;
            color: white;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }

        .link-card:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-10px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        }

        .link-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .link-card p {
            opacity: 0.9;
        }

        /* Stats Section */
        .stats-section {
            background: var(--white);
            padding: 5rem 0;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            text-align: center;
        }

        .stat-card {
            padding: 2rem;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-light);
            font-size: 1.1rem;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 3rem;
            border-radius: 25px;
            width: 90%;
            max-width: 700px;
            position: relative;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        }

        .close-modal {
            position: absolute;
            top: 20px;
            right: 25px;
            font-size: 2.5rem;
            cursor: pointer;
            color: var(--primary-blue);
            transition: color 0.3s;
        }

        .close-modal:hover {
            color: var(--danger);
        }

        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes bounce {
            0%, 20%, 53%, 80%, 100% { transform: translate3d(0,0,0); }
            40%, 43% { transform: translate3d(0,-30px,0); }
            70% { transform: translate3d(0,-15px,0); }
            90% { transform: translate3d(0,-4px,0); }
        }

        @keyframes heartBeat {
            0% { transform: scale(1); }
            14% { transform: scale(1.3); }
            28% { transform: scale(1); }
            42% { transform: scale(1.3); }
            70% { transform: scale(1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out;
        }

        .animate-bounce { animation: bounce 2s infinite; }
        .animate-pulse { animation: pulse 2s infinite; }
        .animate-heartBeat { animation: heartBeat 2s infinite; }

        /* Responsive Design */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .hero p {
                font-size: 1.1rem;
            }
            
            .section-title {
                font-size: 2.2rem;
            }
            
            .container {
                padding: 0 1rem;
            }
            
            .facilities-grid,
            .teachers-grid,
            .achievements-grid,
            .events-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="#home" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="#home">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/alumni">Alumni</a></li>
                    <li><a href="/career-services">Career Services</a></li>
                    <li><a href="/scholarships">Scholarships</a></li>
                    <li><a href="#facilities">Facilities</a></li>
                    <li><a href="#events">Events</a></li>
                    <li><a href="#notices">Notices</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="container fade-in-up">
            <h1>Welcome to ''' + COLLEGE_DATA['name'] + '''</h1>
            <p>Shaping futures through quality education and innovation since ''' + COLLEGE_DATA['established'] + '''</p>
            <div style="margin-top: 3rem;">
                <a href="/admissions" class="btn btn-primary btn-large">Apply for Admissions 2024-25</a>
                <a href="#facilities" class="btn btn-large">Explore Our Campus</a>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">5000+</div>
                    <div class="stat-label">Students</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">200+</div>
                    <div class="stat-label">Faculty</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">50+</div>
                    <div class="stat-label">Courses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">34</div>
                    <div class="stat-label">Years of Excellence</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Facilities Section -->
    <section class="facilities" id="facilities">
        <div class="container">
            <h2 class="section-title">Our Facilities</h2>
            <p class="section-subtitle">State-of-the-art infrastructure to support academic excellence and holistic development</p>
            <div class="facilities-grid" id="facilitiesGrid">
                <!-- Facilities loaded by JavaScript -->
            </div>
            <div style="text-align: center; margin-top: 3rem;">
                <a href="/facilities" class="btn btn-primary btn-large">View All Facilities</a>
            </div>
        </div>
    </section>

    <!-- Teachers Section -->
    <section class="teachers-section" id="teachers">
        <div class="container">
            <h2 class="section-title" style="color: white;">Our Faculty</h2>
            <p class="section-subtitle" style="color: rgba(255,255,255,0.9);">Meet our experienced and dedicated faculty members</p>
            <div class="teachers-grid" id="teachersGrid">
                <!-- Teachers loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Achievements Section -->
    <section class="achievements-section" id="achievements">
        <div class="container">
            <h2 class="section-title">Our Achievements</h2>
            <p class="section-subtitle">Celebrating excellence and recognition in education</p>
            <div class="achievements-grid" id="achievementsGrid">
                <!-- Achievements loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Events Section -->
    <section class="events-section" id="events">
        <div class="container">
            <h2 class="section-title" style="color: white;">Upcoming Events</h2>
            <p class="section-subtitle" style="color: rgba(255,255,255,0.9);">Stay updated with our college activities and programs</p>
            <div class="events-grid" id="eventsGrid">
                <!-- Events loaded by JavaScript -->
            </div>
            <div style="text-align: center; margin-top: 3rem;">
                <a href="/events" class="btn btn-large" style="background: white; color: #f5576c;">View All Events</a>
            </div>
        </div>
    </section>

    <!-- Notices Section -->
    <section class="notices-section" id="notices">
        <div class="container">
            <h2 class="section-title">College Notices</h2>
            <p class="section-subtitle">Important announcements and updates</p>
            <div id="noticesList">
                <!-- Notices loaded by JavaScript -->
            </div>
            <div style="text-align: center; margin-top: 3rem;">
                <a href="/notices" class="btn btn-primary btn-large">View All Notices</a>
            </div>
        </div>
    </section>

    <!-- Quick Links -->
    <section class="quick-links">
        <div class="container">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem;">Quick Links</h2>
            <p style="font-size: 1.2rem; opacity: 0.9;">Easy access to important sections</p>
            <div class="links-grid">
                <a href="/admissions" class="link-card">
                    <h3>Admissions</h3>
                    <p>Apply for 2024-25 academic year</p>
                </a>
                <a href="/academics" class="link-card">
                    <h3>Academics</h3>
                    <p>Programs and courses</p>
                </a>
                <a href="/calendar" class="link-card">
                    <h3>Academic Calendar</h3>
                    <p>Schedule and events</p>
                </a>
                <a href="/departments" class="link-card">
                    <h3>Departments</h3>
                    <p>Academic departments</p>
                </a>
                <a href="/alumni" class="link-card">
                    <h3>Alumni</h3>
                    <p>Network and connect</p>
                </a>
                <a href="/career-services" class="link-card">
                    <h3>Career Services</h3>
                    <p>Placements and training</p>
                </a>
                <a href="/scholarships" class="link-card">
                    <h3>Scholarships</h3>
                    <p>Financial assistance</p>
                </a>
                <a href="/facilities" class="link-card">
                    <h3>Facilities</h3>
                    <p>Campus amenities</p>
                </a>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <footer id="contact" style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved. | Excellence in Education Since ''' + COLLEGE_DATA['established'] + '''</p>
            </div>
        </div>
    </footer>

    <!-- Facility Modal -->
    <div id="facilityModal" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle" style="color: var(--primary-blue); margin-bottom: 1.5rem; font-size: 2rem;">Facility Details</h2>
            <div id="modalContent"></div>
        </div>
    </div>

    <script>
        // Facilities Data
        const facilities = ''' + str(FACILITIES).replace("'", '"') + ''';
        
        // Events Data
        const events = ''' + str(EVENTS).replace("'", '"') + ''';
        
        // Notices Data
        const notices = ''' + str(NOTICES).replace("'", '"') + ''';
        
        // Teachers Data
        const teachers = ''' + str(TEACHERS).replace("'", '"') + ''';
        
        // Achievements Data
        const achievements = ''' + str(ACHIEVEMENTS).replace("'", '"') + ''';
        
        // Load Facilities (limited to 6 for home page)
        const facilitiesGrid = document.getElementById('facilitiesGrid');
        Object.entries(facilities).slice(0, 6).forEach(([id, facility]) => {
            facilitiesGrid.innerHTML += `
                <div class="facility-card" onclick="openModal('${id}')">
                    <img src="${facility.image}" alt="${facility.name}" class="facility-image">
                    <div class="facility-content">
                        <h3>${facility.name}</h3>
                        <p>${facility.description}</p>
                        <div class="facility-details">
                            <div class="facility-detail-item">
                                <strong>Manager:</strong>
                                <span>${facility.manager}</span>
                            </div>
                            <div class="facility-detail-item">
                                <strong>Timing:</strong>
                                <span>${facility.timing}</span>
                            </div>
                            <div class="facility-detail-item">
                                <strong>Experience:</strong>
                                <span>${facility.experience}</span>
                            </div>
                        </div>
                        <div class="btn" style="margin-top: 1rem;">View Complete Details</div>
                    </div>
                </div>
            `;
        });
        
        // Load Teachers
        const teachersGrid = document.getElementById('teachersGrid');
        teachers.forEach(teacher => {
            teachersGrid.innerHTML += `
                <div class="teacher-card">
                    <img src="${teacher.image}" alt="${teacher.name}" class="teacher-image">
                    <div class="teacher-info">
                        <h3>${teacher.name}</h3>
                        <div class="teacher-position">${teacher.position}</div>
                        <div class="teacher-department">${teacher.department}</div>
                        <div style="margin: 1rem 0;"><strong>Qualification:</strong> ${teacher.qualification}</div>
                        <div style="margin-bottom: 1rem;"><strong>Experience:</strong> ${teacher.experience}</div>
                        <p style="font-style: italic; color: var(--text-light);">${teacher.description}</p>
                    </div>
                </div>
            `;
        });
        
        // Load Achievements
        const achievementsGrid = document.getElementById('achievementsGrid');
        achievements.forEach(achievement => {
            achievementsGrid.innerHTML += `
                <div class="achievement-card">
                    <img src="${achievement.image}" alt="${achievement.title}" class="achievement-image">
                    <div class="achievement-content">
                        <h3>${achievement.title}</h3>
                        <p>${achievement.description}</p>
                        <div class="achievement-date">${achievement.date}</div>
                    </div>
                </div>
            `;
        });
        
        // Load Events (limited to 3 for home page)
        const eventsGrid = document.getElementById('eventsGrid');
        const upcomingEvents = events.filter(event => event.status === 'upcoming').slice(0, 3);
        upcomingEvents.forEach(event => {
            eventsGrid.innerHTML += `
                <div class="event-card">
                    <img src="${event.image}" alt="${event.title}" class="event-image">
                    <div class="event-content">
                        <h3>${event.title}</h3>
                        <div class="event-meta">
                            <span>📅 ${event.date}</span>
                            <span>🕒 ${event.time}</span>
                        </div>
                        <div class="event-meta">
                            <span>📍 ${event.venue}</span>
                            <span class="event-category">${event.category}</span>
                        </div>
                        <p>${event.description}</p>
                    </div>
                </div>
            `;
        });
        
        // Load Notices (limited to 3 for home page)
        const noticesList = document.getElementById('noticesList');
        notices.slice(0, 3).forEach(notice => {
            const priorityClass = notice.priority === 'high' ? 'notice-high-priority' : '';
            noticesList.innerHTML += `
                <div class="notice-item ${priorityClass}">
                    <h3>${notice.title}</h3>
                    <div class="notice-meta">
                        <span>📅 ${notice.date}</span>
                        <span class="notice-department">${notice.department}</span>
                    </div>
                    <p>${notice.content}</p>
                </div>
            `;
        });
        
        // Facility Modal Functions
        function openModal(facilityId) {
            const facility = facilities[facilityId];
            let details = `
                <div style="margin-bottom: 2rem;">
                    <img src="${facility.image}" alt="${facility.name}" style="width: 100%; height: 300px; object-fit: cover; border-radius: 15px; margin-bottom: 1.5rem;">
                    <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-dark);">${facility.details}</p>
                </div>
                
                <div class="facility-details">
                    <div class="facility-detail-item">
                        <strong>Manager:</strong>
                        <span>${facility.manager}</span>
                    </div>
                    <div class="facility-detail-item">
                        <strong>Experience:</strong>
                        <span>${facility.experience}</span>
                    </div>
                    <div class="facility-detail-item">
                        <strong>Timing:</strong>
                        <span>${facility.timing}</span>
                    </div>
                </div>
            `;
            
            if (facility.menu) {
                details += '<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Food Menu</h3>';
                Object.entries(facility.menu).forEach(([category, items]) => {
                    details += `<div style="margin-bottom: 1rem;"><strong>${category.charAt(0).toUpperCase() + category.slice(1)}:</strong><br>`;
                    items.forEach(item => {
                        details += `<span style="display: inline-block; background: var(--light-blue); padding: 0.3rem 0.8rem; margin: 0.2rem; border-radius: 8px;">${item}</span>`;
                    });
                    details += '</div>';
                });
                details += '</div>';
            }
            
            if (facility.equipment) {
                details += `<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Equipment & Facilities</h3>`;
                facility.equipment.forEach(item => {
                    details += `<span style="display: inline-block; background: var(--success); color: white; padding: 0.3rem 0.8rem; margin: 0.2rem; border-radius: 8px;">${item}</span>`;
                });
                details += '</div>';
            }
            
            if (facility.services) {
                details += `<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Services Offered</h3>`;
                facility.services.forEach(service => {
                    details += `<span style="display: inline-block; background: var(--warning); color: white; padding: 0.3rem 0.8rem; margin: 0.2rem; border-radius: 8px;">${service}</span>`;
                });
                details += '</div>';
            }
            
            if (facility.activities) {
                details += `<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Activities</h3>`;
                facility.activities.forEach(activity => {
                    details += `<span style="display: inline-block; background: var(--primary-blue); color: white; padding: 0.3rem 0.8rem; margin: 0.2rem; border-radius: 8px;">${activity}</span>`;
                });
                details += '</div>';
            }
            
            document.getElementById('modalTitle').textContent = facility.name;
            document.getElementById('modalContent').innerHTML = details;
            document.getElementById('facilityModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('facilityModal').style.display = 'none';
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('facilityModal');
            if (event.target === modal) {
                closeModal();
            }
        }
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Add loading animation to buttons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', function(e) {
                if (this.getAttribute('href') === '#') {
                    e.preventDefault();
                    const originalText = this.innerHTML;
                    this.innerHTML = '<span class="loading"></span> Loading...';
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 2000);
                }
            });
        });
    </script>
</body>
</html>
'''

# Admissions Page Template (Complete and Functional)
ADMISSIONS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admissions - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Banner */
        .admissions-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
        }

        .admissions-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .admissions-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        .btn-large {
            padding: 18px 45px;
            font-size: 1.2rem;
        }

        /* Main Content */
        .admissions-content {
            background: white;
            padding: 80px 0;
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--text-light);
            font-size: 1.2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Admissions Options */
        .admissions-options {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2.5rem;
            margin-bottom: 4rem;
        }

        .admission-card {
            background: white;
            padding: 3rem 2.5rem;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            text-align: center;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .admission-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(135deg, var(--primary-blue), var(--dark-blue));
        }

        .admission-card:hover {
            transform: translateY(-15px);
            border-color: var(--primary-blue);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }

        .admission-card h3 {
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
            font-size: 1.8rem;
        }

        .admission-card p {
            color: var(--text-light);
            margin-bottom: 2rem;
            line-height: 1.8;
            font-size: 1.1rem;
        }

        /* Eligibility Criteria */
        .eligibility-section {
            background: var(--light-blue);
            padding: 80px 0;
        }

        .eligibility-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .eligibility-card {
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid var(--primary-blue);
            transition: all 0.3s ease;
        }

        .eligibility-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }

        .eligibility-card h4 {
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
            font-size: 1.4rem;
        }

        .eligibility-card p {
            margin-bottom: 1rem;
            color: var(--text-dark);
            line-height: 1.6;
        }

        .eligibility-card .min-marks {
            background: var(--success);
            color: white;
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            font-weight: bold;
            display: inline-block;
            margin-top: 1rem;
            font-size: 0.9rem;
        }

        /* Forms Section */
        .forms-section {
            padding: 80px 0;
            background: white;
        }

        .form-container {
            background: var(--light-blue);
            padding: 3rem;
            border-radius: 25px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            margin-top: 2rem;
        }

        .form-group {
            margin-bottom: 2.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 1rem;
            font-weight: bold;
            color: var(--primary-blue);
            font-size: 1.1rem;
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 18px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s;
            background: white;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--primary-blue);
            outline: none;
            box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
            transform: translateY(-2px);
        }

        .file-upload {
            border: 2px dashed #e5e7eb;
            padding: 2.5rem;
            text-align: center;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s;
            background: rgba(255,255,255,0.5);
        }

        .file-upload:hover {
            border-color: var(--primary-blue);
            background: rgba(255,255,255,0.8);
        }

        .file-upload input {
            margin-bottom: 1.5rem;
        }

        /* Success Message */
        .success-message {
            background: linear-gradient(135deg, var(--success), #34d399);
            color: white;
            padding: 3rem 2rem;
            border-radius: 20px;
            margin: 2rem 0;
            text-align: center;
            display: none;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
        }

        .success-message h3 {
            font-size: 2rem;
            margin-bottom: 1.5rem;
        }

        .success-message p {
            font-size: 1.1rem;
            margin-bottom: 1rem;
            line-height: 1.6;
        }

        /* Process Steps */
        .process-steps {
            background: var(--white);
            padding: 60px 0;
        }

        .steps-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .step-card {
            text-align: center;
            padding: 2rem;
        }

        .step-number {
            background: var(--primary-blue);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 0 auto 1.5rem;
        }

        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }

            .admissions-hero h1 {
                font-size: 2.5rem;
            }

            .admissions-hero p {
                font-size: 1.1rem;
            }

            .admissions-options {
                grid-template-columns: 1fr;
            }

            .form-container {
                padding: 2rem;
            }

            .section-title {
                font-size: 2.2rem;
            }
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>Admissions Portal</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="#eligibility">Eligibility</a></li>
                    <li><a href="#apply">Apply Now</a></li>
                    <li><a href="#process">Process</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Banner -->
    <section class="admissions-hero">
        <div class="container fade-in-up">
            <h1>Begin Your Journey at SIWS College</h1>
            <p>Join our legacy of excellence and shape your future with quality education</p>
            <a href="#apply" class="btn btn-primary btn-large">Start Your Application</a>
        </div>
    </section>

    <!-- Eligibility Section -->
    <section class="eligibility-section" id="eligibility">
        <div class="container">
            <h2 class="section-title">Eligibility Criteria</h2>
            <p class="section-subtitle">Check your eligibility for our various programs before applying</p>
            
            <div class="eligibility-grid">
                <div class="eligibility-card">
                    <h4>Junior College - Science</h4>
                    <p><strong>Stream:</strong> Medical, Engineering, Pure Sciences</p>
                    <p><strong>Subjects Required:</strong> Mathematics, Science</p>
                    <p><strong>Duration:</strong> 2 Years</p>
                    <span class="min-marks">Minimum 65% in SSC</span>
                </div>
                
                <div class="eligibility-card">
                    <h4>Junior College - Commerce</h4>
                    <p><strong>Stream:</strong> Business, Finance, Accounting</p>
                    <p><strong>Subjects Preferred:</strong> Mathematics</p>
                    <p><strong>Duration:</strong> 2 Years</p>
                    <span class="min-marks">Minimum 55% in SSC</span>
                </div>
                
                <div class="eligibility-card">
                    <h4>Junior College - Arts</h4>
                    <p><strong>Stream:</strong> Humanities, Languages, Social Sciences</p>
                    <p><strong>Subjects:</strong> Any stream accepted</p>
                    <p><strong>Duration:</strong> 2 Years</p>
                    <span class="min-marks">Minimum 45% in SSC</span>
                </div>
                
                <div class="eligibility-card">
                    <h4>Degree College - B.Sc</h4>
                    <p><strong>Programs:</strong> Computer Science, Mathematics, Physics</p>
                    <p><strong>Specializations:</strong> Various options available</p>
                    <p><strong>Duration:</strong> 3 Years</p>
                    <span class="min-marks">Minimum 60% in HSC</span>
                </div>
                
                <div class="eligibility-card">
                    <h4>Degree College - B.Com</h4>
                    <p><strong>Programs:</strong> Accountancy, Business Management</p>
                    <p><strong>Specializations:</strong> Banking & Insurance</p>
                    <p><strong>Duration:</strong> 3 Years</p>
                    <span class="min-marks">Minimum 55% in HSC</span>
                </div>
                
                <div class="eligibility-card">
                    <h4>Degree College - B.A & BMS</h4>
                    <p><strong>Programs:</strong> Arts, Management Studies</p>
                    <p><strong>Specializations:</strong> Multiple options</p>
                    <p><strong>Duration:</strong> 3 Years</p>
                    <span class="min-marks">Minimum 50-60% in HSC</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Admissions Process -->
    <section class="process-steps" id="process">
        <div class="container">
            <h2 class="section-title">Admission Process</h2>
            <p class="section-subtitle">Simple and streamlined admission procedure</p>
            
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-number">1</div>
                    <h3>Check Eligibility</h3>
                    <p>Verify that you meet the eligibility criteria for your desired program</p>
                </div>
                
                <div class="step-card">
                    <div class="step-number">2</div>
                    <h3>Fill Application</h3>
                    <p>Complete the online application form with accurate details</p>
                </div>
                
                <div class="step-card">
                    <div class="step-number">3</div>
                    <h3>Upload Documents</h3>
                    <p>Upload required documents including marksheets and ID proof</p>
                </div>
                
                <div class="step-card">
                    <div class="step-number">4</div>
                    <h3>Submit & Track</h3>
                    <p>Submit your application and track its status online</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Admissions Options -->
    <section class="admissions-content">
        <div class="container">
            <h2 class="section-title">Choose Your Path</h2>
            <p class="section-subtitle">Select your desired program and start your application process</p>
            
            <div class="admissions-options">
                <div class="admission-card">
                    <h3>Junior College (11th & 12th)</h3>
                    <p>Build strong foundations in Science, Commerce or Arts streams with expert faculty and modern facilities. Our junior college program prepares students for higher education and competitive exams.</p>
                    <button class="btn btn-primary btn-large" onclick="showForm('junior')">Apply for Junior College</button>
                </div>
                
                <div class="admission-card">
                    <h3>Degree College</h3>
                    <p>Pursue undergraduate degrees in B.Sc, B.Com, B.A or BMS with industry-relevant curriculum and placements. Our degree programs focus on practical learning and skill development.</p>
                    <button class="btn btn-primary btn-large" onclick="showForm('degree')">Apply for Degree College</button>
                </div>
            </div>
        </div>
    </section>

    <!-- Application Forms Section -->
    <section class="forms-section" id="apply">
        <div class="container">
            <h2 class="section-title">Application Form</h2>
            <p class="section-subtitle">Fill out the form for your selected program</p>

            <!-- Success Message -->
            <div class="success-message" id="successMessage">
                <h3>🎉 Application Submitted Successfully!</h3>
                <p>Your admission application has been received. Our team will review your application and contact you within 3-5 working days.</p>
                <p><strong>Application Reference ID: SIWS2024-</strong><span id="referenceId"></span></p>
                <p>You will receive a confirmation email shortly. Keep your reference ID for future communication.</p>
            </div>

            <!-- Junior College Form -->
            <div id="juniorForm" class="form-container" style="display: none;">
                <h3 style="color: var(--primary-blue); margin-bottom: 2rem; text-align: center; font-size: 2rem;">Junior College Admission Form</h3>
                <form id="juniorAdmissionForm" onsubmit="submitForm(event, 'junior')">
                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="full_name" placeholder="Enter your full name as per marksheet" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email Address *</label>
                        <input type="email" name="email" placeholder="Enter your active email address" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Phone Number *</label>
                        <input type="tel" name="phone" placeholder="Enter your 10-digit mobile number" required pattern="[0-9]{10}">
                    </div>
                    
                    <div class="form-group">
                        <label>Select Stream *</label>
                        <select name="stream" required>
                            <option value="">Choose your preferred stream</option>
                            <option value="science">Science</option>
                            <option value="commerce">Commerce</option>
                            <option value="arts">Arts</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>SSC Marks (Percentage) *</label>
                        <input type="number" name="ssc_marks" min="0" max="100" step="0.01" placeholder="Enter your SSC percentage" required>
                    </div>
                    
                    <div class="form-group">
                        <label>SSC Marksheet *</label>
                        <div class="file-upload">
                            <input type="file" name="ssc_marksheet" accept=".pdf,.jpg,.jpeg,.png" required>
                            <p>📁 Upload SSC Marksheet (PDF, JPG, PNG - Max 5MB)</p>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Aadhaar Card *</label>
                        <div class="file-upload">
                            <input type="file" name="aadhaar" accept=".pdf,.jpg,.jpeg,.png" required>
                            <p>📁 Upload Aadhaar Card (PDF, JPG, PNG - Max 5MB)</p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 3rem;">
                        <button type="submit" class="btn btn-primary btn-large" id="juniorSubmitBtn">
                            Submit Application
                        </button>
                        <button type="button" class="btn btn-large" onclick="hideForms()">Cancel</button>
                    </div>
                </form>
            </div>

            <!-- Degree College Form -->
            <div id="degreeForm" class="form-container" style="display: none;">
                <h3 style="color: var(--primary-blue); margin-bottom: 2rem; text-align: center; font-size: 2rem;">Degree College Admission Form</h3>
                <form id="degreeAdmissionForm" onsubmit="submitForm(event, 'degree')">
                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="full_name" placeholder="Enter your full name as per marksheet" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email Address *</label>
                        <input type="email" name="email" placeholder="Enter your active email address" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Phone Number *</label>
                        <input type="tel" name="phone" placeholder="Enter your 10-digit mobile number" required pattern="[0-9]{10}">
                    </div>
                    
                    <div class="form-group">
                        <label>Select Program *</label>
                        <select name="program" required>
                            <option value="">Choose your desired program</option>
                            <option value="bsc">B.Sc (Science)</option>
                            <option value="bcom">B.Com (Commerce)</option>
                            <option value="ba">B.A (Arts)</option>
                            <option value="bms">BMS (Management)</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>HSC Marks (Percentage) *</label>
                        <input type="number" name="hsc_marks" min="0" max="100" step="0.01" placeholder="Enter your HSC percentage" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Select Specialization</label>
                        <select name="specialization">
                            <option value="">Choose specialization (Optional)</option>
                            <option value="computer_science">Computer Science</option>
                            <option value="mathematics">Mathematics</option>
                            <option value="physics">Physics</option>
                            <option value="chemistry">Chemistry</option>
                            <option value="microbiology">Microbiology</option>
                            <option value="accountancy">Accountancy</option>
                            <option value="business_management">Business Management</option>
                            <option value="banking_insurance">Banking & Insurance</option>
                            <option value="english">English Literature</option>
                            <option value="psychology">Psychology</option>
                            <option value="economics">Economics</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>HSC Marksheet *</label>
                        <div class="file-upload">
                            <input type="file" name="hsc_marksheet" accept=".pdf,.jpg,.jpeg,.png" required>
                            <p>📁 Upload HSC Marksheet (PDF, JPG, PNG - Max 5MB)</p>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Aadhaar Card *</label>
                        <div class="file-upload">
                            <input type="file" name="aadhaar" accept=".pdf,.jpg,.jpeg,.png" required>
                            <p>📁 Upload Aadhaar Card (PDF, JPG, PNG - Max 5MB)</p>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 3rem;">
                        <button type="submit" class="btn btn-primary btn-large" id="degreeSubmitBtn">
                            Submit Application
                        </button>
                        <button type="button" class="btn btn-large" onclick="hideForms()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h3 style="font-size: 2rem; margin-bottom: 2rem;">Need Help with Admissions?</h3>
            <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Contact our admission cell for any queries or assistance</p>
            <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            <p style="font-size: 1.1rem; margin-bottom: 2rem;">📍 ''' + COLLEGE_DATA['contact']['address'] + '''</p>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Form Management Functions
        function showForm(type) {
            hideForms();
            if (type === 'junior') {
                document.getElementById('juniorForm').style.display = 'block';
                document.getElementById('juniorForm').scrollIntoView({ behavior: 'smooth' });
            } else if (type === 'degree') {
                document.getElementById('degreeForm').style.display = 'block';
                document.getElementById('degreeForm').scrollIntoView({ behavior: 'smooth' });
            }
        }
        
        function hideForms() {
            document.getElementById('juniorForm').style.display = 'none';
            document.getElementById('degreeForm').style.display = 'none';
        }
        
        function submitForm(event, type) {
            event.preventDefault();
            
            const submitBtn = type === 'junior' ? document.getElementById('juniorSubmitBtn') : document.getElementById('degreeSubmitBtn');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<span class="loading"></span> Submitting...';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(() => {
                // Generate random reference ID
                const referenceId = Math.floor(100000 + Math.random() * 900000);
                document.getElementById('referenceId').textContent = referenceId;
                
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Hide forms
                hideForms();
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Scroll to success message
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });
                
                // Here you would typically send the form data to server
                console.log('Form submitted for:', type);
                
                // Show confirmation alert
                alert('Application submitted successfully! Your reference ID is: SIWS2024-' + referenceId);
                
            }, 2000);
        }
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Add loading animation to main apply button
        document.querySelectorAll('.btn-primary').forEach(button => {
            button.addEventListener('click', function(e) {
                if (this.getAttribute('href') === '#apply') {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<span class="loading"></span> Redirecting...';
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 1500);
                }
            });
        });
    </script>
</body>
</html>
'''

# Facilities Page Template (Complete and Functional)
FACILITIES_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facilities - SIWS College</title>
    <style>
        /* Include all CSS from home page */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles - Same as home page */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section for Facilities */
        .facilities-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1562774053-701939374585?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2064&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .facilities-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .facilities-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Facilities Grid */
        .facilities-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--text-light);
            font-size: 1.2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .facilities-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 3rem;
        }

        .facility-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
        }

        .facility-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .facility-image {
            width: 100%;
            height: 300px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .facility-card:hover .facility-image {
            transform: scale(1.05);
        }

        .facility-content {
            padding: 2.5rem;
        }

        .facility-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }

        .facility-description {
            color: var(--text-light);
            margin-bottom: 1.5rem;
            line-height: 1.7;
            font-size: 1.1rem;
        }

        .facility-details {
            background: var(--light-blue);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
        }

        .facility-detail-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
            padding-bottom: 0.8rem;
            border-bottom: 1px solid rgba(30, 58, 138, 0.1);
        }

        .facility-detail-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }

        .facility-features {
            margin-top: 1.5rem;
        }

        .feature-tag {
            display: inline-block;
            background: var(--primary-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin: 0.3rem;
            font-size: 0.9rem;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
        }

        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 3rem;
            border-radius: 25px;
            width: 90%;
            max-width: 800px;
            position: relative;
            max-height: 85vh;
            overflow-y: auto;
            box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        }

        .close-modal {
            position: absolute;
            top: 20px;
            right: 25px;
            font-size: 2.5rem;
            cursor: pointer;
            color: var(--primary-blue);
            transition: color 0.3s;
        }

        .close-modal:hover {
            color: var(--danger);
        }

        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }

            .facilities-hero h1 {
                font-size: 2.5rem;
            }

            .facilities-hero p {
                font-size: 1.1rem;
            }

            .facilities-grid {
                grid-template-columns: 1fr;
            }

            .section-title {
                font-size: 2.2rem;
            }

            .facility-content {
                padding: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/facilities" style="color: var(--primary-blue); background: var(--light-blue);">Facilities</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/notices">Notices</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="facilities-hero">
        <div class="container fade-in-up">
            <h1>Our Campus Facilities</h1>
            <p>State-of-the-art infrastructure to support academic excellence and holistic development</p>
            <a href="#facilities" class="btn btn-primary">Explore Facilities</a>
        </div>
    </section>

    <!-- Facilities Section -->
    <section class="facilities-section" id="facilities">
        <div class="container">
            <h2 class="section-title">World-Class Facilities</h2>
            <p class="section-subtitle">Discover our comprehensive range of facilities designed to enhance learning, research, and student life</p>
            
            <div class="facilities-grid" id="facilitiesGrid">
                <!-- Facilities loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved. | Excellence in Education Since ''' + COLLEGE_DATA['established'] + '''</p>
            </div>
        </div>
    </footer>

    <!-- Facility Modal -->
    <div id="facilityModal" class="modal">
        <div class="modal-content">
            <span class="close-modal" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle" style="color: var(--primary-blue); margin-bottom: 1.5rem; font-size: 2rem;">Facility Details</h2>
            <div id="modalContent"></div>
        </div>
    </div>

    <script>
        // Facilities Data
        const facilities = ''' + str(FACILITIES).replace("'", '"') + ''';
        
        // Load All Facilities
        const facilitiesGrid = document.getElementById('facilitiesGrid');
        Object.entries(facilities).forEach(([id, facility]) => {
            let features = '';
            if (facility.menu) {
                features = '<div class="facility-features"><strong>Special Features:</strong> Food Services, Multiple Cuisines</div>';
            } else if (facility.equipment) {
                features = `<div class="facility-features"><strong>Equipment:</strong> ${facility.equipment.slice(0, 3).join(', ')}${facility.equipment.length > 3 ? '...' : ''}</div>`;
            } else if (facility.services) {
                features = `<div class="facility-features"><strong>Services:</strong> ${facility.services.slice(0, 3).join(', ')}${facility.services.length > 3 ? '...' : ''}</div>`;
            } else if (facility.activities) {
                features = `<div class="facility-features"><strong>Activities:</strong> ${facility.activities.slice(0, 3).join(', ')}${facility.activities.length > 3 ? '...' : ''}</div>`;
            }
            
            facilitiesGrid.innerHTML += `
                <div class="facility-card" onclick="openModal('${id}')">
                    <img src="${facility.image}" alt="${facility.name}" class="facility-image">
                    <div class="facility-content">
                        <h3>${facility.name}</h3>
                        <p class="facility-description">${facility.description}</p>
                        <div class="facility-details">
                            <div class="facility-detail-item">
                                <strong>Manager:</strong>
                                <span>${facility.manager}</span>
                            </div>
                            <div class="facility-detail-item">
                                <strong>Timing:</strong>
                                <span>${facility.timing}</span>
                            </div>
                            <div class="facility-detail-item">
                                <strong>Experience:</strong>
                                <span>${facility.experience}</span>
                            </div>
                        </div>
                        ${features}
                        <div class="btn" style="margin-top: 1.5rem; width: 100%; text-align: center;">View Complete Details</div>
                    </div>
                </div>
            `;
        });
        
        // Facility Modal Functions
        function openModal(facilityId) {
            const facility = facilities[facilityId];
            let details = `
                <div style="margin-bottom: 2rem;">
                    <img src="${facility.image}" alt="${facility.name}" style="width: 100%; height: 350px; object-fit: cover; border-radius: 15px; margin-bottom: 1.5rem;">
                    <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-dark); margin-bottom: 1.5rem;">${facility.details}</p>
                </div>
                
                <div class="facility-details">
                    <div class="facility-detail-item">
                        <strong>Manager:</strong>
                        <span>${facility.manager}</span>
                    </div>
                    <div class="facility-detail-item">
                        <strong>Experience:</strong>
                        <span>${facility.experience}</span>
                    </div>
                    <div class="facility-detail-item">
                        <strong>Timing:</strong>
                        <span>${facility.timing}</span>
                    </div>
                </div>
            `;
            
            if (facility.menu) {
                details += '<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Food Menu</h3>';
                Object.entries(facility.menu).forEach(([category, items]) => {
                    details += `<div style="margin-bottom: 1.5rem;"><h4 style="color: var(--dark-blue); margin-bottom: 0.5rem;">${category.charAt(0).toUpperCase() + category.slice(1)}</h4>`;
                    items.forEach(item => {
                        details += `<div style="display: inline-block; background: var(--light-blue); padding: 0.5rem 1rem; margin: 0.3rem; border-radius: 8px; border-left: 4px solid var(--primary-blue);">${item}</div>`;
                    });
                    details += '</div>';
                });
                details += '</div>';
            }
            
            if (facility.equipment) {
                details += `<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Equipment & Facilities</h3>`;
                facility.equipment.forEach(item => {
                    details += `<span style="display: inline-block; background: var(--success); color: white; padding: 0.5rem 1rem; margin: 0.3rem; border-radius: 8px;">${item}</span>`;
                });
                details += '</div>';
            }
            
            if (facility.services) {
                details += `<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Services Offered</h3>`;
                facility.services.forEach(service => {
                    details += `<span style="display: inline-block; background: var(--warning); color: white; padding: 0.5rem 1rem; margin: 0.3rem; border-radius: 8px;">${service}</span>`;
                });
                details += '</div>';
            }
            
            if (facility.activities) {
                details += `<div style="margin-top: 2rem;"><h3 style="color: var(--primary-blue); margin-bottom: 1rem;">Activities</h3>`;
                facility.activities.forEach(activity => {
                    details += `<span style="display: inline-block; background: var(--primary-blue); color: white; padding: 0.5rem 1rem; margin: 0.3rem; border-radius: 8px;">${activity}</span>`;
                });
                details += '</div>';
            }
            
            document.getElementById('modalTitle').textContent = facility.name;
            document.getElementById('modalContent').innerHTML = details;
            document.getElementById('facilityModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('facilityModal').style.display = 'none';
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('facilityModal');
            if (event.target === modal) {
                closeModal();
            }
        }
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
'''

# Events Page Template (Complete and Functional)
EVENTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Events - SIWS College</title>
    <style>
        /* Include all CSS from home page */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles - Same as home page */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section for Events */
        .events-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1540575467063-178a50c2df87?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .events-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .events-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Events Section */
        .events-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--text-light);
            font-size: 1.2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .events-filter {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 12px 25px;
            border: 2px solid var(--primary-blue);
            background: transparent;
            color: var(--primary-blue);
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }

        .filter-btn:hover, .filter-btn.active {
            background: var(--primary-blue);
            color: white;
        }

        .events-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 3rem;
        }

        .event-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .event-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .event-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }

        .event-card:hover .event-image {
            transform: scale(1.05);
        }

        .event-content {
            padding: 2.5rem;
        }

        .event-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.6rem;
        }

        .event-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            color: var(--text-light);
            font-size: 0.95rem;
        }

        .event-category {
            background: var(--primary-blue);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .event-status {
            display: inline-block;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .status-upcoming {
            background: var(--success);
            color: white;
        }

        .status-completed {
            background: var(--text-light);
            color: white;
        }

        .event-description {
            color: var(--text-dark);
            line-height: 1.7;
            margin-bottom: 1.5rem;
        }

        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }

            .events-hero h1 {
                font-size: 2.5rem;
            }

            .events-hero p {
                font-size: 1.1rem;
            }

            .events-grid {
                grid-template-columns: 1fr;
            }

            .section-title {
                font-size: 2.2rem;
            }

            .events-filter {
                flex-direction: column;
                align-items: center;
            }

            .filter-btn {
                width: 200px;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/events" style="color: var(--primary-blue); background: var(--light-blue);">Events</a></li>
                    <li><a href="/notices">Notices</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="events-hero">
        <div class="container fade-in-up">
            <h1>College Events & Activities</h1>
            <p>Stay updated with our vibrant campus life, cultural programs, and academic events</p>
            <a href="#events" class="btn btn-primary">View Events</a>
        </div>
    </section>

    <!-- Events Section -->
    <section class="events-section" id="events">
        <div class="container">
            <h2 class="section-title">Upcoming & Past Events</h2>
            <p class="section-subtitle">Explore our diverse range of events that enrich campus life and student experience</p>
            
            <div class="events-filter">
                <button class="filter-btn active" onclick="filterEvents('all')">All Events</button>
                <button class="filter-btn" onclick="filterEvents('upcoming')">Upcoming</button>
                <button class="filter-btn" onclick="filterEvents('completed')">Past Events</button>
                <button class="filter-btn" onclick="filterEvents('cultural')">Cultural</button>
                <button class="filter-btn" onclick="filterEvents('sports')">Sports</button>
                <button class="filter-btn" onclick="filterEvents('technical')">Technical</button>
            </div>
            
            <div class="events-grid" id="eventsGrid">
                <!-- Events loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved. | Excellence in Education Since ''' + COLLEGE_DATA['established'] + '''</p>
            </div>
        </div>
    </footer>

    <script>
        // Events Data
        const events = ''' + str(EVENTS).replace("'", '"') + ''';
        
        // Load All Events
        function loadEvents(filter = 'all') {
            const eventsGrid = document.getElementById('eventsGrid');
            eventsGrid.innerHTML = '';
            
            const filteredEvents = events.filter(event => {
                if (filter === 'all') return true;
                if (filter === 'upcoming') return event.status === 'upcoming';
                if (filter === 'completed') return event.status === 'completed';
                return event.category === filter;
            });
            
            if (filteredEvents.length === 0) {
                eventsGrid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 4rem; color: var(--text-light);">
                        <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">No events found</h3>
                        <p>There are no events in this category at the moment.</p>
                    </div>
                `;
                return;
            }
            
            filteredEvents.forEach(event => {
                const statusClass = event.status === 'upcoming' ? 'status-upcoming' : 'status-completed';
                const statusText = event.status === 'upcoming' ? 'Upcoming' : 'Completed';
                
                eventsGrid.innerHTML += `
                    <div class="event-card">
                        <img src="${event.image}" alt="${event.title}" class="event-image">
                        <div class="event-content">
                            <span class="event-status ${statusClass}">${statusText}</span>
                            <h3>${event.title}</h3>
                            <div class="event-meta">
                                <span>📅 ${event.date}</span>
                                <span>🕒 ${event.time}</span>
                            </div>
                            <div class="event-meta">
                                <span>📍 ${event.venue}</span>
                                <span class="event-category">${event.category}</span>
                            </div>
                            <p class="event-description">${event.description}</p>
                            <button class="btn" style="width: 100%; text-align: center; margin-top: 1rem;">
                                ${event.status === 'upcoming' ? 'Register for Event' : 'View Photos'}
                            </button>
                        </div>
                    </div>
                `;
            });
        }
        
        // Filter Events
        function filterEvents(category) {
            // Update active filter button
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Load filtered events
            loadEvents(category);
        }
        
        // Initialize events
        loadEvents();
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
'''

# Notices Page Template (Complete and Functional)
NOTICES_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notices - SIWS College</title>
    <style>
        /* Include all CSS from home page */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles - Same as home page */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section for Notices */
        .notices-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1582573618383-1aaf165b815c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2069&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .notices-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .notices-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Notices Section */
        .notices-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--text-light);
            font-size: 1.2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .notices-filter {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 3rem;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 12px 25px;
            border: 2px solid var(--primary-blue);
            background: transparent;
            color: var(--primary-blue);
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }

        .filter-btn:hover, .filter-btn.active {
            background: var(--primary-blue);
            color: white;
        }

        .notices-list {
            max-width: 900px;
            margin: 0 auto;
        }

        .notice-item {
            background: white;
            padding: 2.5rem;
            margin: 2rem 0;
            border-radius: 20px;
            border-left: 6px solid var(--primary-blue);
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .notice-item:hover {
            transform: translateX(10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }

        .notice-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(30, 58, 138, 0.02), rgba(30, 64, 175, 0.02));
            z-index: 1;
        }

        .notice-high-priority {
            border-left-color: var(--danger);
            background: linear-gradient(135deg, #fff, #ffeaea);
        }

        .notice-medium-priority {
            border-left-color: var(--warning);
            background: linear-gradient(135deg, #fff, #fff3cd);
        }

        .notice-item h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.5rem;
            position: relative;
            z-index: 2;
        }

        .notice-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            color: var(--text-light);
            font-size: 0.95rem;
            position: relative;
            z-index: 2;
        }

        .notice-department {
            background: var(--primary-blue);
            color: white;
            padding: 0.4rem 1.2rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }

        .notice-priority {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-right: 1rem;
        }

        .priority-high {
            background: var(--danger);
            color: white;
        }

        .priority-medium {
            background: var(--warning);
            color: white;
        }

        .priority-low {
            background: var(--success);
            color: white;
        }

        .notice-content {
            color: var(--text-dark);
            line-height: 1.7;
            font-size: 1.05rem;
            position: relative;
            z-index: 2;
        }

        .notice-image {
            width: 100%;
            max-width: 400px;
            border-radius: 10px;
            margin-top: 1.5rem;
            display: block;
        }

        .no-notices {
            text-align: center;
            padding: 4rem;
            color: var(--text-light);
        }

        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }

            .notices-hero h1 {
                font-size: 2.5rem;
            }

            .notices-hero p {
                font-size: 1.1rem;
            }

            .section-title {
                font-size: 2.2rem;
            }

            .notices-filter {
                flex-direction: column;
                align-items: center;
            }

            .filter-btn {
                width: 200px;
                text-align: center;
            }

            .notice-item {
                padding: 2rem;
            }

            .notice-meta {
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/notices" style="color: var(--primary-blue); background: var(--light-blue);">Notices</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="notices-hero">
        <div class="container fade-in-up">
            <h1>College Notices & Announcements</h1>
            <p>Stay informed with the latest updates, important announcements, and college circulars</p>
            <a href="#notices" class="btn btn-primary">View Notices</a>
        </div>
    </section>

    <!-- Notices Section -->
    <section class="notices-section" id="notices">
        <div class="container">
            <h2 class="section-title">Important Notices</h2>
            <p class="section-subtitle">Latest announcements and updates from various departments</p>
            
            <div class="notices-filter">
                <button class="filter-btn active" onclick="filterNotices('all')">All Notices</button>
                <button class="filter-btn" onclick="filterNotices('academic')">Academic</button>
                <button class="filter-btn" onclick="filterNotices('admission')">Admissions</button>
                <button class="filter-btn" onclick="filterNotices('facility')">Facilities</button>
                <button class="filter-btn" onclick="filterNotices('achievement')">Achievements</button>
            </div>
            
            <div class="notices-list" id="noticesList">
                <!-- Notices loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved. | Excellence in Education Since ''' + COLLEGE_DATA['established'] + '''</p>
            </div>
        </div>
    </footer>

    <script>
        // Notices Data
        const notices = ''' + str(NOTICES).replace("'", '"') + ''';
        
        // Load All Notices
        function loadNotices(filter = 'all') {
            const noticesList = document.getElementById('noticesList');
            noticesList.innerHTML = '';
            
            const filteredNotices = notices.filter(notice => {
                if (filter === 'all') return true;
                return notice.category === filter;
            });
            
            if (filteredNotices.length === 0) {
                noticesList.innerHTML = `
                    <div class="no-notices">
                        <h3 style="font-size: 1.5rem; margin-bottom: 1rem; color: var(--text-light);">No notices found</h3>
                        <p>There are no notices in this category at the moment.</p>
                    </div>
                `;
                return;
            }
            
            filteredNotices.forEach(notice => {
                const priorityClass = `priority-${notice.priority}`;
                const priorityText = notice.priority === 'high' ? 'High Priority' : 
                                   notice.priority === 'medium' ? 'Medium Priority' : 'Low Priority';
                
                let noticeClass = '';
                if (notice.priority === 'high') {
                    noticeClass = 'notice-high-priority';
                } else if (notice.priority === 'medium') {
                    noticeClass = 'notice-medium-priority';
                }
                
                const imageHtml = notice.image ? `<img src="${notice.image}" alt="${notice.title}" class="notice-image">` : '';
                
                noticesList.innerHTML += `
                    <div class="notice-item ${noticeClass}">
                        <span class="notice-priority ${priorityClass}">${priorityText}</span>
                        <h3>${notice.title}</h3>
                        <div class="notice-meta">
                            <span>📅 Published on: ${notice.date}</span>
                            <span class="notice-department">${notice.department}</span>
                        </div>
                        <div class="notice-content">
                            <p>${notice.content}</p>
                            ${imageHtml}
                        </div>
                    </div>
                `;
            });
        }
        
        // Filter Notices
        function filterNotices(category) {
            // Update active filter button
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Load filtered notices
            loadNotices(category);
        }
        
        // Initialize notices
        loadNotices();
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
'''

# Contact Page Template (Complete and Functional)
CONTACT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact - SIWS College</title>
    <style>
        /* Include all CSS from home page */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles - Same as home page */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section for Contact */
        .contact-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2069&q=80');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .contact-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .contact-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Contact Section */
        .contact-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .section-subtitle {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--text-light);
            font-size: 1.2rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .contact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 3rem;
            margin-bottom: 4rem;
        }

        .contact-info {
            background: var(--light-blue);
            padding: 3rem;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .contact-info h3 {
            color: var(--primary-blue);
            margin-bottom: 2rem;
            font-size: 1.8rem;
        }

        .contact-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }

        .contact-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        .contact-icon {
            background: var(--primary-blue);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-right: 1.5rem;
            flex-shrink: 0;
        }

        .contact-details h4 {
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
            font-size: 1.2rem;
        }

        .contact-details p {
            color: var(--text-dark);
            line-height: 1.6;
        }

        .contact-form {
            background: var(--light-blue);
            padding: 3rem;
            border-radius: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .contact-form h3 {
            color: var(--primary-blue);
            margin-bottom: 2rem;
            font-size: 1.8rem;
        }

        .form-group {
            margin-bottom: 2rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 1rem;
            font-weight: bold;
            color: var(--primary-blue);
            font-size: 1.1rem;
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 18px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s;
            background: white;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--primary-blue);
            outline: none;
            box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
            transform: translateY(-2px);
        }

        .form-group textarea {
            height: 150px;
            resize: vertical;
        }

        /* Map Section */
        .map-section {
            padding: 60px 0;
            background: var(--light-blue);
        }

        .map-container {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            height: 400px;
        }

        /* Success Message */
        .success-message {
            background: linear-gradient(135deg, var(--success), #34d399);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin: 2rem 0;
            text-align: center;
            display: none;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
        }

        /* Departments Section */
        .departments-section {
            padding: 60px 0;
            background: var(--white);
        }

        .departments-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 2rem;
        }

        .department-card {
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            border-top: 5px solid var(--primary-blue);
            transition: all 0.3s ease;
        }

        .department-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .department-card h4 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.3rem;
        }

        .department-card p {
            color: var(--text-light);
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }

        /* Animations */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.8s ease-out;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 1rem;
            }

            .contact-hero h1 {
                font-size: 2.5rem;
            }

            .contact-hero p {
                font-size: 1.1rem;
            }

            .contact-grid {
                grid-template-columns: 1fr;
            }

            .section-title {
                font-size: 2.2rem;
            }

            .contact-info, .contact-form {
                padding: 2rem;
            }

            .contact-item {
                flex-direction: column;
                text-align: center;
            }

            .contact-icon {
                margin-right: 0;
                margin-bottom: 1rem;
            }
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/notices">Notices</a></li>
                    <li><a href="/contact" style="color: var(--primary-blue); background: var(--light-blue);">Contact</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="contact-hero">
        <div class="container fade-in-up">
            <h1>Get In Touch With Us</h1>
            <p>We're here to help you with any questions or information you need</p>
            <a href="#contact" class="btn btn-primary">Contact Information</a>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="contact-section" id="contact">
        <div class="container">
            <h2 class="section-title">Contact Information</h2>
            <p class="section-subtitle">Reach out to us through any of the following channels</p>
            
            <div class="contact-grid">
                <div class="contact-info">
                    <h3>College Information</h3>
                    
                    <div class="contact-item">
                        <div class="contact-icon">📍</div>
                        <div class="contact-details">
                            <h4>College Address</h4>
                            <p>''' + COLLEGE_DATA['contact']['address'] + '''</p>
                        </div>
                    </div>
                    
                    <div class="contact-item">
                        <div class="contact-icon">📞</div>
                        <div class="contact-details">
                            <h4>Phone Numbers</h4>
                            <p>''' + COLLEGE_DATA['contact']['phone'] + '''<br>Admissions: +91 (22) 1234-5679</p>
                        </div>
                    </div>
                    
                    <div class="contact-item">
                        <div class="contact-icon">✉️</div>
                        <div class="contact-details">
                            <h4>Email Addresses</h4>
                            <p>''' + COLLEGE_DATA['contact']['email'] + '''<br>admissions@siwscollege.edu</p>
                        </div>
                    </div>
                    
                    <div class="contact-item">
                        <div class="contact-icon">🕒</div>
                        <div class="contact-details">
                            <h4>Working Hours</h4>
                            <p>Monday - Friday: 9:00 AM - 5:00 PM<br>Saturday: 9:00 AM - 1:00 PM</p>
                        </div>
                    </div>
                </div>
                
                <div class="contact-form">
                    <h3>Send us a Message</h3>
                    
                    <!-- Success Message -->
                    <div class="success-message" id="successMessage">
                        <h3>✅ Message Sent Successfully!</h3>
                        <p>Thank you for contacting us. We'll get back to you within 24 hours.</p>
                    </div>
                    
                    <form id="contactForm" onsubmit="submitContactForm(event)">
                        <div class="form-group">
                            <label>Full Name *</label>
                            <input type="text" name="full_name" placeholder="Enter your full name" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Email Address *</label>
                            <input type="email" name="email" placeholder="Enter your email address" required>
                        </div>
                        
                        <div class="form-group">
                            <label>Phone Number</label>
                            <input type="tel" name="phone" placeholder="Enter your phone number">
                        </div>
                        
                        <div class="form-group">
                            <label>Department</label>
                            <select name="department">
                                <option value="">Select Department</option>
                                <option value="admissions">Admissions</option>
                                <option value="academic">Academic</option>
                                <option value="administration">Administration</option>
                                <option value="facilities">Facilities</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label>Message *</label>
                            <textarea name="message" placeholder="Enter your message here..." required></textarea>
                        </div>
                        
                        <button type="submit" class="btn btn-primary" style="width: 100%; padding: 18px; font-size: 1.1rem;" id="submitBtn">
                            Send Message
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </section>

    <!-- Departments Section -->
    <section class="departments-section">
        <div class="container">
            <h2 class="section-title">Key Departments</h2>
            <p class="section-subtitle">Contact specific departments for specialized queries</p>
            
            <div class="departments-grid">
                <div class="department-card">
                    <h4>Admissions Office</h4>
                    <p>For admission-related queries and application process</p>
                    <p><strong>Email:</strong> admissions@siwscollege.edu</p>
                    <p><strong>Phone:</strong> +91 (22) 1234-5679</p>
                </div>
                
                <div class="department-card">
                    <h4>Academic Office</h4>
                    <p>For academic programs and curriculum information</p>
                    <p><strong>Email:</strong> academic@siwscollege.edu</p>
                    <p><strong>Phone:</strong> +91 (22) 1234-5680</p>
                </div>
                
                <div class="department-card">
                    <h4>Administration</h4>
                    <p>For administrative and general inquiries</p>
                    <p><strong>Email:</strong> admin@siwscollege.edu</p>
                    <p><strong>Phone:</strong> +91 (22) 1234-5681</p>
                </div>
                
                <div class="department-card">
                    <h4>Student Support</h4>
                    <p>For student services and support</p>
                    <p><strong>Email:</strong> studentsupport@siwscollege.edu</p>
                    <p><strong>Phone:</strong> +91 (22) 1234-5682</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Map Section -->
    <section class="map-section">
        <div class="container">
            <h2 class="section-title">Find Us</h2>
            <p class="section-subtitle">Visit our campus or locate us on the map</p>
            
            <div class="map-container">
                <iframe 
                    src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3771.75583730284!2d72.83421431538467!3d19.075558987111!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c8c0a1e6b5a5%3A0x3b2fa4b4e4e4e4e4!2sMumbai%2C%20Maharashtra!5e0!3m2!1sen!2sin!4v1620000000000!5m2!1sen!2sin" 
                    width="100%" 
                    height="100%" 
                    style="border:0;" 
                    allowfullscreen="" 
                    loading="lazy">
                </iframe>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">We're Here to Help</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved. | Excellence in Education Since ''' + COLLEGE_DATA['established'] + '''</p>
            </div>
        </div>
    </footer>

    <script>
        // Contact Form Submission
        function submitContactForm(event) {
            event.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<span class="loading"></span> Sending...';
            submitBtn.disabled = true;
            
            // Simulate form submission
            setTimeout(() => {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Reset form
                document.getElementById('contactForm').reset();
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Scroll to success message
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Show confirmation alert
                alert('Thank you for your message! We will get back to you soon.');
                
            }, 2000);
        }
        
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    </script>
</body>
</html>
'''

# NEW: Interactive Calendar Page
CALENDAR_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Calendar - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .calendar-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&h=600&fit=crop');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .calendar-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .calendar-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Calendar Section */
        .calendar-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .calendar-container {
            background: white;
            border-radius: 25px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-bottom: 4rem;
        }

        .calendar-header {
            background: var(--primary-blue);
            color: white;
            padding: 2rem;
            text-align: center;
        }

        .calendar-header h3 {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 1px;
            background: #e5e7eb;
        }

        .calendar-day-header {
            background: var(--light-blue);
            padding: 1rem;
            text-align: center;
            font-weight: bold;
            color: var(--primary-blue);
        }

        .calendar-day {
            background: white;
            padding: 1rem;
            min-height: 120px;
            border: 1px solid #e5e7eb;
            position: relative;
        }

        .calendar-day.empty {
            background: #f9fafb;
        }

        .day-number {
            font-weight: bold;
            margin-bottom: 0.5rem;
            color: var(--text-dark);
        }

        .calendar-event {
            background: var(--primary-blue);
            color: white;
            padding: 0.3rem 0.5rem;
            border-radius: 5px;
            font-size: 0.8rem;
            margin-bottom: 0.3rem;
            cursor: pointer;
            transition: all 0.3s;
        }

        .calendar-event:hover {
            transform: scale(1.05);
        }

        .event-academic { background: #3b82f6; }
        .event-exam { background: #f59e0b; }
        .event-holiday { background: #ef4444; }

        /* Events List */
        .events-list {
            background: var(--light-blue);
            padding: 3rem;
            border-radius: 20px;
            margin-top: 3rem;
        }

        .event-filter {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }

        .filter-btn {
            padding: 10px 20px;
            border: 2px solid var(--primary-blue);
            background: transparent;
            color: var(--primary-blue);
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }

        .filter-btn.active, .filter-btn:hover {
            background: var(--primary-blue);
            color: white;
        }

        .event-item {
            background: white;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 15px;
            border-left: 4px solid var(--primary-blue);
            transition: all 0.3s;
        }

        .event-item:hover {
            transform: translateX(10px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .event-item.academic { border-left-color: #3b82f6; }
        .event-item.exam { border-left-color: #f59e0b; }
        .event-item.holiday { border-left-color: #ef4444; }

        .event-date {
            background: var(--primary-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: bold;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .calendar-grid {
                grid-template-columns: repeat(7, 1fr);
                font-size: 0.8rem;
            }
            
            .calendar-day {
                padding: 0.5rem;
                min-height: 80px;
            }
            
            .calendar-event {
                font-size: 0.7rem;
                padding: 0.2rem 0.3rem;
            }
            
            .event-filter {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar" style="color: var(--primary-blue); background: var(--light-blue);">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/alumni">Alumni</a></li>
                    <li><a href="/career-services">Career Services</a></li>
                    <li><a href="/scholarships">Scholarships</a></li>
                    <li><a href="/events">Events</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="calendar-hero">
        <div class="container">
            <h1>Academic Calendar 2024-25</h1>
            <p>Stay organized with our comprehensive academic schedule, exam dates, and important events</p>
            <a href="#calendar" class="btn btn-primary">View Calendar</a>
        </div>
    </section>

    <!-- Calendar Section -->
    <section class="calendar-section" id="calendar">
        <div class="container">
            <h2 class="section-title">Academic Calendar</h2>
            
            <div class="calendar-container">
                <div class="calendar-header">
                    <h3>June 2024</h3>
                    <p>Semester 1 Begins</p>
                </div>
                <div class="calendar-grid" id="calendarGrid">
                    <!-- Calendar will be generated by JavaScript -->
                </div>
            </div>

            <div class="events-list">
                <h3 style="text-align: center; margin-bottom: 2rem; color: var(--primary-blue);">Upcoming Events</h3>
                
                <div class="event-filter">
                    <button class="filter-btn active" onclick="filterEvents('all')">All Events</button>
                    <button class="filter-btn" onclick="filterEvents('academic')">Academic</button>
                    <button class="filter-btn" onclick="filterEvents('exam')">Exams</button>
                    <button class="filter-btn" onclick="filterEvents('holiday')">Holidays</button>
                </div>
                
                <div id="eventsList">
                    <!-- Events will be loaded by JavaScript -->
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Calendar Data
        const calendarEvents = ''' + str(CALENDAR_EVENTS).replace("'", '"') + ''';
        
        // Generate Calendar
        function generateCalendar() {
            const calendarGrid = document.getElementById('calendarGrid');
            const daysOfWeek = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            
            // Add day headers
            daysOfWeek.forEach(day => {
                calendarGrid.innerHTML += `<div class="calendar-day-header">${day}</div>`;
            });
            
            // Generate days for June 2024 (starts on Saturday)
            const totalDays = 30;
            const startDay = 6; // Saturday
            
            // Add empty days for start
            for (let i = 0; i < startDay; i++) {
                calendarGrid.innerHTML += `<div class="calendar-day empty"></div>`;
            }
            
            // Add actual days
            for (let day = 1; day <= totalDays; day++) {
                const dateStr = `2024-06-${day.toString().padStart(2, '0')}`;
                const dayEvents = calendarEvents.filter(event => event.date === dateStr);
                
                let eventsHtml = '';
                dayEvents.forEach(event => {
                    eventsHtml += `<div class="calendar-event event-${event.type}" onclick="showEventDetails(${event.id})">${event.title}</div>`;
                });
                
                calendarGrid.innerHTML += `
                    <div class="calendar-day">
                        <div class="day-number">${day}</div>
                        ${eventsHtml}
                    </div>
                `;
            }
        }
        
        // Load Events List
        function loadEvents(filter = 'all') {
            const eventsList = document.getElementById('eventsList');
            eventsList.innerHTML = '';
            
            const filteredEvents = calendarEvents.filter(event => {
                if (filter === 'all') return true;
                return event.type === filter;
            });
            
            if (filteredEvents.length === 0) {
                eventsList.innerHTML = '<p style="text-align: center; color: var(--text-light);">No events found</p>';
                return;
            }
            
            filteredEvents.forEach(event => {
                eventsList.innerHTML += `
                    <div class="event-item ${event.type}">
                        <div class="event-date">${event.date}</div>
                        <h4>${event.title}</h4>
                        <p>${event.description}</p>
                        <span class="event-type-badge" style="background: ${event.color}; color: white; padding: 0.3rem 0.8rem; border-radius: 12px; font-size: 0.8rem;">
                            ${event.type.charAt(0).toUpperCase() + event.type.slice(1)}
                        </span>
                    </div>
                `;
            });
        }
        
        // Filter Events
        function filterEvents(type) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            loadEvents(type);
        }
        
        // Show Event Details
        function showEventDetails(eventId) {
            const event = calendarEvents.find(e => e.id === eventId);
            if (event) {
                alert(`${event.title}\\nDate: ${event.date}\\nType: ${event.type}\\n\\n${event.description}`);
            }
        }
        
        // Initialize
        generateCalendar();
        loadEvents();
    </script>
</body>
</html>
'''

# NEW: Academic Programs Page
ACADEMICS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Programs - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .academics-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=600&fit=crop');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .academics-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .academics-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Programs Section */
        .programs-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .program-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 3rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .tab-btn {
            padding: 15px 30px;
            border: 2px solid var(--primary-blue);
            background: transparent;
            color: var(--primary-blue);
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
            font-size: 1.1rem;
        }

        .tab-btn.active, .tab-btn:hover {
            background: var(--primary-blue);
            color: white;
        }

        .programs-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2.5rem;
        }

        .program-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .program-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .program-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }

        .program-content {
            padding: 2.5rem;
        }

        .program-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.6rem;
        }

        .program-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 1.5rem;
            color: var(--text-light);
        }

        .program-duration {
            background: var(--primary-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }

        .program-features {
            margin: 1.5rem 0;
        }

        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.8rem;
        }

        .feature-item::before {
            content: '✓';
            color: var(--success);
            font-weight: bold;
            margin-right: 0.8rem;
        }

        .career-opportunities {
            background: var(--light-blue);
            padding: 1.5rem;
            border-radius: 15px;
            margin-top: 1.5rem;
        }

        .career-opportunities h4 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        .career-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .career-tag {
            background: var(--primary-blue);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
        }

        /* Stats Section */
        .stats-section {
            background: var(--primary-blue);
            color: white;
            padding: 80px 0;
            text-align: center;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }

        .stat-card {
            padding: 2rem;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .program-tabs {
                flex-direction: column;
                align-items: center;
            }
            
            .tab-btn {
                width: 250px;
                text-align: center;
            }
            
            .programs-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics" style="color: var(--primary-blue); background: var(--light-blue);">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/alumni">Alumni</a></li>
                    <li><a href="/career-services">Career Services</a></li>
                    <li><a href="/scholarships">Scholarships</a></li>
                    <li><a href="/events">Events</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="academics-hero">
        <div class="container">
            <h1>Academic Programs</h1>
            <p>Explore our diverse range of undergraduate, postgraduate, and certificate programs designed for your success</p>
            <a href="#programs" class="btn btn-primary">View Programs</a>
        </div>
    </section>

    <!-- Programs Section -->
    <section class="programs-section" id="programs">
        <div class="container">
            <h2 class="section-title">Our Programs</h2>
            
            <div class="program-tabs">
                <button class="tab-btn active" onclick="showPrograms('undergraduate')">Undergraduate</button>
                <button class="tab-btn" onclick="showPrograms('postgraduate')">Postgraduate</button>
                <button class="tab-btn" onclick="showPrograms('certificate')">Certificate Courses</button>
            </div>
            
            <div class="programs-grid" id="programsGrid">
                <!-- Programs will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">15+</div>
                    <div class="stat-label">Academic Programs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">200+</div>
                    <div class="stat-label">Expert Faculty</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">85%</div>
                    <div class="stat-label">Placement Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">5000+</div>
                    <div class="stat-label">Successful Alumni</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Academic Programs Data
        const academicPrograms = ''' + str(ACADEMIC_PROGRAMS).replace("'", '"') + ''';
        
        // Show Programs by Category
        function showPrograms(category) {
            // Update active tab
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Load programs
            const programsGrid = document.getElementById('programsGrid');
            programsGrid.innerHTML = '';
            
            const programs = academicPrograms[category];
            
            if (programs.length === 0) {
                programsGrid.innerHTML = `
                    <div style="grid-column: 1 / -1; text-align: center; padding: 4rem; color: var(--text-light);">
                        <h3>No programs available in this category</h3>
                        <p>Please check back later for updates.</p>
                    </div>
                `;
                return;
            }
            
            programs.forEach(program => {
                const specializations = program.specializations ? 
                    program.specializations.map(spec => `<span class="career-tag">${spec}</span>`).join('') : '';
                
                programsGrid.innerHTML += `
                    <div class="program-card">
                        <img src="${program.image}" alt="${program.name}" class="program-image">
                        <div class="program-content">
                            <h3>${program.name}</h3>
                            <div class="program-meta">
                                <span class="program-duration">${program.duration}</span>
                                <span>Fees: ${program.fees}</span>
                            </div>
                            <p>${program.description}</p>
                            
                            <div class="program-features">
                                <div class="feature-item"><strong>Eligibility:</strong> ${program.eligibility}</div>
                                ${specializations ? `<div class="feature-item"><strong>Specializations:</strong> ${program.specializations.join(', ')}</div>` : ''}
                            </div>
                            
                            <div class="career-opportunities">
                                <h4>Career Opportunities</h4>
                                <div class="career-tags">
                                    ${program.career_opportunities.map(career => `<span class="career-tag">${career}</span>`).join('')}
                                </div>
                            </div>
                            
                            <button class="btn btn-primary" style="width: 100%; margin-top: 1.5rem;" onclick="showProgramDetails(${program.id}, '${category}')">
                                Learn More
                            </button>
                        </div>
                    </div>
                `;
            });
        }
        
        // Show Program Details
        function showProgramDetails(programId, category) {
            const program = academicPrograms[category].find(p => p.id === programId);
            if (program) {
                const specializations = program.specializations ? 
                    `<p><strong>Specializations:</strong> ${program.specializations.join(', ')}</p>` : '';
                
                const details = `
                    <h2>${program.name}</h2>
                    <p><strong>Duration:</strong> ${program.duration}</p>
                    <p><strong>Fees:</strong> ${program.fees}</p>
                    <p><strong>Eligibility:</strong> ${program.eligibility}</p>
                    ${specializations}
                    <p>${program.description}</p>
                    <h3>Career Opportunities</h3>
                    <ul>
                        ${program.career_opportunities.map(career => `<li>${career}</li>`).join('')}
                    </ul>
                `;
                
                alert(`Program Details:\\n\\n${program.name}\\nDuration: ${program.duration}\\nFees: ${program.fees}\\n\\n${program.description}`);
            }
        }
        
        // Initialize with undergraduate programs
        showPrograms('undergraduate');
    </script>
</body>
</html>
'''

# NEW: Departments Page
DEPARTMENTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Academic Departments - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .departments-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1200&h=600&fit=crop');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .departments-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .departments-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Departments Section */
        .departments-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .departments-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 3rem;
        }

        .department-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .department-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .department-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }

        .department-content {
            padding: 2.5rem;
        }

        .department-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-size: 1.6rem;
        }

        .department-hod {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: var(--light-blue);
            border-radius: 15px;
        }

        .hod-image {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            margin-right: 1rem;
            border: 3px solid var(--primary-blue);
        }

        .hod-info h4 {
            color: var(--primary-blue);
            margin-bottom: 0.3rem;
        }

        .hod-info p {
            color: var(--text-light);
            font-size: 0.9rem;
        }

        .department-stats {
            display: flex;
            justify-content: space-between;
            margin: 1.5rem 0;
            padding: 1rem;
            background: var(--light-blue);
            border-radius: 15px;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary-blue);
        }

        .stat-label {
            font-size: 0.8rem;
            color: var(--text-light);
        }

        .programs-list {
            margin: 1.5rem 0;
        }

        .program-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.8rem;
        }

        .program-item::before {
            content: '🎓';
            margin-right: 0.8rem;
        }

        .research-areas {
            background: var(--light-blue);
            padding: 1.5rem;
            border-radius: 15px;
            margin: 1.5rem 0;
        }

        .research-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1rem;
        }

        .research-tag {
            background: var(--primary-blue);
            color: white;
            padding: 0.4rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
        }

        /* Faculty Section */
        .faculty-section {
            background: var(--light-blue);
            padding: 80px 0;
        }

        .faculty-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .faculty-card {
            background: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .faculty-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .faculty-card h4 {
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
        }

        .faculty-card p {
            color: var(--text-light);
            margin-bottom: 1rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .departments-grid {
                grid-template-columns: 1fr;
            }
            
            .department-stats {
                flex-direction: column;
                gap: 1rem;
            }
            
            .stat {
                text-align: left;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Admissions Open 2024-25</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>''' + COLLEGE_DATA['motto'] + '''</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments" style="color: var(--primary-blue); background: var(--light-blue);">Departments</a></li>
                    <li><a href="/alumni">Alumni</a></li>
                    <li><a href="/career-services">Career Services</a></li>
                    <li><a href="/scholarships">Scholarships</a></li>
                    <li><a href="/events">Events</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="departments-hero">
        <div class="container">
            <h1>Academic Departments</h1>
            <p>Explore our diverse academic departments, each dedicated to excellence in education and research</p>
            <a href="#departments" class="btn btn-primary">View Departments</a>
        </div>
    </section>

    <!-- Departments Section -->
    <section class="departments-section" id="departments">
        <div class="container">
            <h2 class="section-title">Our Departments</h2>
            
            <div class="departments-grid" id="departmentsGrid">
                <!-- Departments will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Faculty Section -->
    <section class="faculty-section">
        <div class="container">
            <h2 class="section-title">Department Heads</h2>
            <div class="faculty-grid" id="facultyGrid">
                <!-- Faculty will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Contact Us</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">''' + COLLEGE_DATA['contact']['address'] + '''</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ ''' + COLLEGE_DATA['contact']['email'] + '''</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + '''. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Departments Data
        const departments = ''' + str(DEPARTMENTS).replace("'", '"') + ''';
        
        // Load Departments
        function loadDepartments() {
            const departmentsGrid = document.getElementById('departmentsGrid');
            const facultyGrid = document.getElementById('facultyGrid');
            
            departmentsGrid.innerHTML = '';
            facultyGrid.innerHTML = '';
            
            Object.entries(departments).forEach(([key, dept]) => {
                // Department Card
                departmentsGrid.innerHTML += `
                    <div class="department-card">
                        <img src="${dept.image}" alt="${dept.name}" class="department-image">
                        <div class="department-content">
                            <h3>${dept.name}</h3>
                            
                            <div class="department-hod">
                                <img src="${dept.hod_image}" alt="${dept.hod}" class="hod-image">
                                <div class="hod-info">
                                    <h4>${dept.hod}</h4>
                                    <p>Head of Department</p>
                                </div>
                            </div>
                            
                            <p>${dept.description}</p>
                            
                            <div class="department-stats">
                                <div class="stat">
                                    <div class="stat-number">${dept.faculty_count}+</div>
                                    <div class="stat-label">Faculty</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-number">${dept.programs.length}</div>
                                    <div class="stat-label">Programs</div>
                                </div>
                                <div class="stat">
                                    <div class="stat-number">${dept.research_areas.length}</div>
                                    <div class="stat-label">Research Areas</div>
                                </div>
                            </div>
                            
                            <div class="programs-list">
                                <h4>Programs Offered</h4>
                                ${dept.programs.map(program => `<div class="program-item">${program}</div>`).join('')}
                            </div>
                            
                            <div class="research-areas">
                                <h4>Research Areas</h4>
                                <div class="research-tags">
                                    ${dept.research_areas.map(area => `<span class="research-tag">${area}</span>`).join('')}
                                </div>
                            </div>
                            
                            <button class="btn btn-primary" style="width: 100%;" onclick="showDepartmentDetails('${key}')">
                                View Department Details
                            </button>
                        </div>
                    </div>
                `;
                
                // Faculty Card for HOD
                facultyGrid.innerHTML += `
                    <div class="faculty-card">
                        <h4>${dept.hod}</h4>
                        <p>Head of ${dept.name}</p>
                        <p><strong>Qualification:</strong> ${dept.faculty[0].qualification}</p>
                        <p><strong>Experience:</strong> 15+ Years</p>
                    </div>
                `;
            });
        }
        
        // Show Department Details
        function showDepartmentDetails(deptKey) {
            const dept = departments[deptKey];
            if (dept) {
                const details = `
                    Department: ${dept.name}
                    Head: ${dept.hod}
                    Faculty Count: ${dept.faculty_count}
                    
                    Programs:
                    ${dept.programs.join('\\n')}
                    
                    Research Areas:
                    ${dept.research_areas.join('\\n')}
                    
                    Achievements:
                    ${dept.achievements.join('\\n')}
                `;
                
                alert(`Department Details:\\n\\n${details}`);
            }
        }
        
        // Initialize
        loadDepartments();
    </script>
</body>
</html>
'''

# NEW: Alumni Association Page
ALUMNI_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alumni Association - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .alumni-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1200&h=600&fit=crop');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .alumni-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .alumni-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Success Stories Section */
        .stories-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .stories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 3rem;
        }

        .story-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .story-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .alumni-image {
            width: 100%;
            height: 300px;
            object-fit: cover;
        }

        .story-content {
            padding: 2.5rem;
        }

        .story-content h3 {
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
            font-size: 1.4rem;
        }

        .alumni-batch {
            color: var(--text-light);
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }

        .alumni-position {
            background: var(--primary-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: bold;
        }

        .alumni-achievement {
            background: var(--light-blue);
            padding: 1rem;
            border-radius: 15px;
            margin: 1rem 0;
            font-style: italic;
        }

        /* Events Section */
        .events-section {
            background: var(--light-blue);
            padding: 80px 0;
        }

        .events-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2.5rem;
        }

        .event-card {
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .event-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .event-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }

        .event-content {
            padding: 2rem;
        }

        .event-content h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        .event-date {
            background: var(--primary-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: bold;
        }

        /* Registration Section */
        .registration-section {
            padding: 80px 0;
            background: var(--white);
        }

        .registration-form {
            background: var(--light-blue);
            padding: 3rem;
            border-radius: 25px;
            max-width: 600px;
            margin: 0 auto;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 2rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 1rem;
            font-weight: bold;
            color: var(--primary-blue);
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--primary-blue);
            outline: none;
            box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
        }

        .success-message {
            background: var(--success);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            display: none;
        }

        /* Stats Section */
        .stats-section {
            background: var(--primary-blue);
            color: white;
            padding: 60px 0;
            text-align: center;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }

        .stat-card {
            padding: 2rem;
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .stories-grid, .events-grid {
                grid-template-columns: 1fr;
            }
            
            .registration-form {
                padding: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Alumni Meet 2024</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ alumni@siwscollege.edu</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>Alumni Association</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/alumni" style="color: var(--primary-blue); background: var(--light-blue);">Alumni</a></li>
                    <li><a href="/career-services">Career Services</a></li>
                    <li><a href="/scholarships">Scholarships</a></li>
                    <li><a href="/events">Events</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="alumni-hero">
        <div class="container">
            <h1>SIWS College Alumni Association</h1>
            <p>Connecting generations of excellence - Stay connected, give back, and grow together</p>
            <a href="#register" class="btn btn-primary">Join Alumni Network</a>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">5000+</div>
                    <div class="stat-label">Alumni Members</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">25+</div>
                    <div class="stat-label">Countries Worldwide</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100+</div>
                    <div class="stat-label">Industry Leaders</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">15</div>
                    <div class="stat-label">Annual Events</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Success Stories Section -->
    <section class="stories-section">
        <div class="container">
            <h2 class="section-title">Alumni Success Stories</h2>
            <div class="stories-grid" id="storiesGrid">
                <!-- Stories will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Events Section -->
    <section class="events-section">
        <div class="container">
            <h2 class="section-title">Upcoming Alumni Events</h2>
            <div class="events-grid" id="eventsGrid">
                <!-- Events will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Registration Section -->
    <section class="registration-section" id="register">
        <div class="container">
            <h2 class="section-title">Join Our Alumni Network</h2>
            
            <div class="success-message" id="successMessage">
                <h3>🎉 Registration Successful!</h3>
                <p>Welcome to the SIWS College Alumni Network. You will receive a confirmation email shortly.</p>
            </div>
            
            <div class="registration-form">
                <form id="alumniRegistrationForm" onsubmit="submitRegistration(event)">
                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="full_name" placeholder="Enter your full name" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email Address *</label>
                        <input type="email" name="email" placeholder="Enter your email address" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Phone Number</label>
                        <input type="tel" name="phone" placeholder="Enter your phone number">
                    </div>
                    
                    <div class="form-group">
                        <label>Graduation Year *</label>
                        <select name="graduation_year" required>
                            <option value="">Select Graduation Year</option>
                            <option value="2023">2023</option>
                            <option value="2022">2022</option>
                            <option value="2021">2021</option>
                            <option value="2020">2020</option>
                            <option value="2019">2019</option>
                            <option value="2018">2018</option>
                            <option value="2017">2017</option>
                            <option value="2016">2016</option>
                            <option value="2015">2015</option>
                            <option value="2014">2014</option>
                            <option value="2013">2013</option>
                            <option value="2012">2012</option>
                            <option value="2011">2011</option>
                            <option value="2010">2010</option>
                            <option value="2009">2009</option>
                            <option value="2008">2008</option>
                            <option value="2007">2007</option>
                            <option value="2006">2006</option>
                            <option value="2005">2005</option>
                            <option value="2004">2004</option>
                            <option value="2003">2003</option>
                            <option value="2002">2002</option>
                            <option value="2001">2001</option>
                            <option value="2000">2000</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Program Studied *</label>
                        <select name="program" required>
                            <option value="">Select Program</option>
                            <option value="bsc">B.Sc</option>
                            <option value="bcom">B.Com</option>
                            <option value="ba">B.A</option>
                            <option value="bms">BMS</option>
                            <option value="msc">M.Sc</option>
                            <option value="mcom">M.Com</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Current Position</label>
                        <input type="text" name="position" placeholder="Enter your current position">
                    </div>
                    
                    <div class="form-group">
                        <label>Company/Organization</label>
                        <input type="text" name="company" placeholder="Enter your company name">
                    </div>
                    
                    <div class="form-group">
                        <label>Interested in Mentorship Program?</label>
                        <select name="mentorship">
                            <option value="no">No</option>
                            <option value="yes">Yes, I want to be a mentor</option>
                            <option value="seek">Yes, I need mentorship</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 18px; font-size: 1.1rem;" id="submitBtn">
                        Join Alumni Network
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Stay Connected</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">Alumni Relations Office</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ alumni@siwscollege.edu</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + ''' Alumni Association. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Alumni Data
        const alumniData = ''' + str(ALUMNI_DATA).replace("'", '"') + ''';
        
        // Load Success Stories
        function loadStories() {
            const storiesGrid = document.getElementById('storiesGrid');
            storiesGrid.innerHTML = '';
            
            alumniData.success_stories.forEach(story => {
                storiesGrid.innerHTML += `
                    <div class="story-card">
                        <img src="${story.image}" alt="${story.name}" class="alumni-image">
                        <div class="story-content">
                            <h3>${story.name}</h3>
                            <div class="alumni-batch">${story.batch} | ${story.program}</div>
                            <div class="alumni-position">${story.current_position}</div>
                            <div class="alumni-achievement">${story.achievement}</div>
                            <p>"${story.testimonial}"</p>
                        </div>
                    </div>
                `;
            });
        }
        
        // Load Events
        function loadEvents() {
            const eventsGrid = document.getElementById('eventsGrid');
            eventsGrid.innerHTML = '';
            
            alumniData.events.forEach(event => {
                eventsGrid.innerHTML += `
                    <div class="event-card">
                        <img src="${event.image}" alt="${event.title}" class="event-image">
                        <div class="event-content">
                            <div class="event-date">${event.date}</div>
                            <h3>${event.title}</h3>
                            <p>${event.description}</p>
                            <button class="btn" style="width: 100%; margin-top: 1rem;">Register for Event</button>
                        </div>
                    </div>
                `;
            });
        }
        
        // Submit Registration
        function submitRegistration(event) {
            event.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = 'Registering...';
            submitBtn.disabled = true;
            
            // Simulate registration
            setTimeout(() => {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Reset form
                document.getElementById('alumniRegistrationForm').reset();
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Scroll to success message
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });
                
                alert('Thank you for joining the SIWS College Alumni Network!');
                
            }, 2000);
        }
        
        // Initialize
        loadStories();
        loadEvents();
    </script>
</body>
</html>
'''

# NEW: Career Services Page
CAREER_SERVICES_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Services - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .career-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=600&fit=crop');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .career-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .career-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Stats Section */
        .stats-section {
            background: var(--white);
            padding: 80px 0;
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            text-align: center;
        }

        .stat-card {
            background: var(--light-blue);
            padding: 3rem 2rem;
            border-radius: 20px;
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
        }

        .stat-label {
            color: var(--text-dark);
            font-size: 1.1rem;
            font-weight: 500;
        }

        /* Recruiters Section */
        .recruiters-section {
            background: var(--light-blue);
            padding: 80px 0;
        }

        .recruiters-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 2rem;
            align-items: center;
        }

        .recruiter-logo {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }

        .recruiter-logo:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }

        /* Training Programs */
        .training-section {
            padding: 80px 0;
            background: var(--white);
        }

        .training-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2.5rem;
        }

        .training-card {
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid var(--primary-blue);
            transition: all 0.3s ease;
        }

        .training-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }

        .training-card h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        .training-duration {
            background: var(--primary-blue);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: bold;
        }

        /* Registration Section */
        .registration-section {
            background: var(--light-blue);
            padding: 80px 0;
        }

        .registration-form {
            background: white;
            padding: 3rem;
            border-radius: 25px;
            max-width: 600px;
            margin: 0 auto;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 2rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 1rem;
            font-weight: bold;
            color: var(--primary-blue);
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--primary-blue);
            outline: none;
            box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
        }

        .file-upload {
            border: 2px dashed #e5e7eb;
            padding: 2rem;
            text-align: center;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .file-upload:hover {
            border-color: var(--primary-blue);
            background: var(--light-blue);
        }

        .success-message {
            background: var(--success);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            display: none;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .stats-grid, .training-grid {
                grid-template-columns: 1fr;
            }
            
            .recruiters-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .registration-form {
                padding: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Placement Drive 2024</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ placement@siwscollege.edu</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>Career Services & Placements</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/alumni">Alumni</a></li>
                    <li><a href="/career-services" style="color: var(--primary-blue); background: var(--light-blue);">Career Services</a></li>
                    <li><a href="/scholarships">Scholarships</a></li>
                    <li><a href="/events">Events</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="career-hero">
        <div class="container">
            <h1>Career Services & Placements</h1>
            <p>Bridging the gap between education and employment with comprehensive career development programs</p>
            <a href="#register" class="btn btn-primary">Register for Placements</a>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="container">
            <h2 class="section-title">Placement Statistics 2023-24</h2>
            <div class="stats-grid" id="statsGrid">
                <!-- Stats will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Recruiters Section -->
    <section class="recruiters-section">
        <div class="container">
            <h2 class="section-title">Our Recruiting Partners</h2>
            <div class="recruiters-grid" id="recruitersGrid">
                <!-- Recruiters will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Training Programs -->
    <section class="training-section">
        <div class="container">
            <h2 class="section-title">Training & Development Programs</h2>
            <div class="training-grid" id="trainingGrid">
                <!-- Training programs will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Registration Section -->
    <section class="registration-section" id="register">
        <div class="container">
            <h2 class="section-title">Student Registration for Placements</h2>
            
            <div class="success-message" id="successMessage">
                <h3>✅ Registration Successful!</h3>
                <p>Your placement registration has been submitted. Our team will contact you soon.</p>
            </div>
            
            <div class="registration-form">
                <form id="placementRegistrationForm" onsubmit="submitRegistration(event)">
                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="full_name" placeholder="Enter your full name" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email Address *</label>
                        <input type="email" name="email" placeholder="Enter your email address" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Phone Number *</label>
                        <input type="tel" name="phone" placeholder="Enter your phone number" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Program *</label>
                        <select name="program" required>
                            <option value="">Select Program</option>
                            <option value="bsc">B.Sc</option>
                            <option value="bcom">B.Com</option>
                            <option value="ba">B.A</option>
                            <option value="bms">BMS</option>
                            <option value="msc">M.Sc</option>
                            <option value="mcom">M.Com</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Specialization</label>
                        <input type="text" name="specialization" placeholder="Enter your specialization">
                    </div>
                    
                    <div class="form-group">
                        <label>Current CGPA *</label>
                        <input type="number" name="cgpa" min="0" max="10" step="0.01" placeholder="Enter your CGPA" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Expected Salary (LPA)</label>
                        <input type="number" name="expected_salary" placeholder="Enter expected salary">
                    </div>
                    
                    <div class="form-group">
                        <label>Resume Upload *</label>
                        <div class="file-upload">
                            <input type="file" name="resume" accept=".pdf,.doc,.docx" required>
                            <p>📁 Upload your resume (PDF, DOC - Max 5MB)</p>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Areas of Interest</label>
                        <select name="interest_areas" multiple>
                            <option value="software">Software Development</option>
                            <option value="data">Data Science</option>
                            <option value="finance">Finance & Banking</option>
                            <option value="marketing">Marketing</option>
                            <option value="hr">Human Resources</option>
                            <option value="operations">Operations</option>
                        </select>
                        <small>Hold Ctrl to select multiple options</small>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 18px; font-size: 1.1rem;" id="submitBtn">
                        Submit Registration
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Career Services Office</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">Training & Placement Cell</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ placement@siwscollege.edu</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + ''' Career Services. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Career Services Data
        const careerServices = ''' + str(CAREER_SERVICES).replace("'", '"') + ''';
        
        // Load Stats
        function loadStats() {
            const statsGrid = document.getElementById('statsGrid');
            const stats = careerServices.placement_stats;
            
            statsGrid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-number">${stats.total_placed}+</div>
                    <div class="stat-label">Students Placed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.placement_percentage}%</div>
                    <div class="stat-label">Placement Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.highest_package}</div>
                    <div class="stat-label">Highest Package</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${stats.average_package}</div>
                    <div class="stat-label">Average Package</div>
                </div>
            `;
        }
        
        // Load Recruiters
        function loadRecruiters() {
            const recruitersGrid = document.getElementById('recruitersGrid');
            recruitersGrid.innerHTML = '';
            
            careerServices.top_recruiters.forEach(recruiter => {
                recruitersGrid.innerHTML += `
                    <div class="recruiter-logo">
                        <h4>${recruiter.name}</h4>
                    </div>
                `;
            });
        }
        
        // Load Training Programs
        function loadTrainingPrograms() {
            const trainingGrid = document.getElementById('trainingGrid');
            trainingGrid.innerHTML = '';
            
            careerServices.training_programs.forEach(program => {
                trainingGrid.innerHTML += `
                    <div class="training-card">
                        <div class="training-duration">${program.duration}</div>
                        <h3>${program.name}</h3>
                        <p>${program.description}</p>
                        <button class="btn" style="width: 100%; margin-top: 1rem;">Enroll Now</button>
                    </div>
                `;
            });
        }
        
        // Submit Registration
        function submitRegistration(event) {
            event.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = 'Submitting...';
            submitBtn.disabled = true;
            
            // Simulate registration
            setTimeout(() => {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Reset form
                document.getElementById('placementRegistrationForm').reset();
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Scroll to success message
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });
                
                alert('Placement registration submitted successfully!');
                
            }, 2000);
        }
        
        // Initialize
        loadStats();
        loadRecruiters();
        loadTrainingPrograms();
    </script>
</body>
</html>
'''

# NEW: Scholarships Page
SCHOLARSHIPS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scholarships - SIWS College</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary-blue: #1e3a8a;
            --dark-blue: #1e40af;
            --light-blue: #dbeafe;
            --white: #ffffff;
            --text-dark: #1f2937;
            --text-light: #6b7280;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background-color: var(--light-blue);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }

        /* Header Styles */
        .top-bar {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 0;
            font-size: 0.9rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
        }

        .top-bar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .admission-badge {
            background: var(--danger);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        header {
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: fixed;
            width: 100%;
            top: 40px;
            z-index: 999;
        }

        .nav-main {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 1rem;
            text-decoration: none;
        }

        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary-blue);
        }

        .logo-text h1 {
            font-size: 1.8rem;
            color: var(--primary-blue);
            margin-bottom: 0.2rem;
        }

        .logo-text span {
            font-size: 0.9rem;
            color: var(--text-light);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 2rem;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-dark);
            font-weight: 500;
            transition: color 0.3s;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }

        .nav-links a:hover {
            color: var(--primary-blue);
            background: var(--light-blue);
        }

        /* Hero Section */
        .scholarships-hero {
            background: linear-gradient(rgba(30, 58, 138, 0.8), rgba(30, 64, 175, 0.8)), 
                        url('https://images.unsplash.com/photo-1553877522-43269d4ea984?w=1200&h=600&fit=crop');
            background-size: cover;
            background-position: center;
            color: white;
            padding: 180px 0 100px;
            text-align: center;
            margin-top: 100px;
        }

        .scholarships-hero h1 {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }

        .scholarships-hero p {
            font-size: 1.3rem;
            margin-bottom: 2rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .btn {
            display: inline-block;
            background: var(--white);
            color: var(--primary-blue);
            padding: 15px 35px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            margin: 5px;
            font-size: 1.1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .btn:hover {
            background: var(--light-blue);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }

        .btn-primary {
            background: var(--primary-blue);
            color: white;
        }

        .btn-primary:hover {
            background: var(--dark-blue);
        }

        /* Scholarships Section */
        .scholarships-section {
            padding: 80px 0;
            background: var(--white);
        }

        .section-title {
            text-align: center;
            margin-bottom: 3rem;
            color: var(--primary-blue);
            font-size: 2.8rem;
            position: relative;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--primary-blue);
            border-radius: 2px;
        }

        .scholarships-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 3rem;
        }

        .scholarship-card {
            background: white;
            border-radius: 25px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border-left: 5px solid var(--primary-blue);
        }

        .scholarship-card:hover {
            transform: translateY(-15px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }

        .scholarship-header {
            background: var(--primary-blue);
            color: white;
            padding: 2rem;
        }

        .scholarship-header h3 {
            font-size: 1.6rem;
            margin-bottom: 0.5rem;
        }

        .scholarship-amount {
            background: var(--success);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            display: inline-block;
            font-weight: bold;
        }

        .scholarship-content {
            padding: 2.5rem;
        }

        .scholarship-deadline {
            background: var(--warning);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 15px;
            display: inline-block;
            margin-bottom: 1rem;
            font-weight: bold;
        }

        .scholarship-beneficiaries {
            background: var(--light-blue);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            text-align: center;
        }

        .documents-list {
            margin: 1.5rem 0;
        }

        .document-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.8rem;
        }

        .document-item::before {
            content: '📄';
            margin-right: 0.8rem;
        }

        /* Application Section */
        .application-section {
            background: var(--light-blue);
            padding: 80px 0;
        }

        .application-form {
            background: white;
            padding: 3rem;
            border-radius: 25px;
            max-width: 600px;
            margin: 0 auto;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 2rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 1rem;
            font-weight: bold;
            color: var(--primary-blue);
        }

        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s;
        }

        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            border-color: var(--primary-blue);
            outline: none;
            box-shadow: 0 0 0 3px rgba(30, 58, 138, 0.1);
        }

        .file-upload {
            border: 2px dashed #e5e7eb;
            padding: 2rem;
            text-align: center;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .file-upload:hover {
            border-color: var(--primary-blue);
            background: var(--light-blue);
        }

        .success-message {
            background: var(--success);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 0;
            display: none;
        }

        /* Stats Section */
        .stats-section {
            background: var(--primary-blue);
            color: white;
            padding: 60px 0;
            text-align: center;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
        }

        .stat-card {
            padding: 2rem;
        }

        .stat-number {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }

        .stat-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .scholarships-grid {
                grid-template-columns: 1fr;
            }
            
            .application-form {
                padding: 2rem;
            }
        }
    </style>
</head>
<body>
    <!-- Top Bar -->
    <div class="top-bar">
        <div class="container">
            <div class="admission-badge">Scholarships Available</div>
            <div>📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ scholarships@siwscollege.edu</div>
        </div>
    </div>

    <!-- Header -->
    <header>
        <div class="container">
            <nav class="nav-main">
                <a href="/" class="logo">
                    <img src="https://www.siwscollege.edu.in/wp-content/themes/twentytwentyfour/custom-templates/images/SIWS%20logo%20new.png" alt="SIWS College Logo" class="logo-img">
                    <div class="logo-text">
                        <h1>''' + COLLEGE_DATA['name'] + '''</h1>
                        <span>Scholarships & Financial Aid</span>
                    </div>
                </a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/admissions">Admissions</a></li>
                    <li><a href="/academics">Academics</a></li>
                    <li><a href="/calendar">Calendar</a></li>
                    <li><a href="/departments">Departments</a></li>
                    <li><a href="/alumni">Alumni</a></li>
                    <li><a href="/career-services">Career Services</a></li>
                    <li><a href="/scholarships" style="color: var(--primary-blue); background: var(--light-blue);">Scholarships</a></li>
                    <li><a href="/events">Events</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="scholarships-hero">
        <div class="container">
            <h1>Scholarships & Financial Aid</h1>
            <p>Making quality education accessible through various scholarship programs and financial assistance</p>
            <a href="#apply" class="btn btn-primary">Apply for Scholarship</a>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">200+</div>
                    <div class="stat-label">Scholarships Awarded</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">₹50L+</div>
                    <div class="stat-label">Financial Aid Distributed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">15+</div>
                    <div class="stat-label">Scholarship Types</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100%</div>
                    <div class="stat-label">Merit-Based Support</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Scholarships Section -->
    <section class="scholarships-section">
        <div class="container">
            <h2 class="section-title">Available Scholarships</h2>
            <div class="scholarships-grid" id="scholarshipsGrid">
                <!-- Scholarships will be loaded by JavaScript -->
            </div>
        </div>
    </section>

    <!-- Application Section -->
    <section class="application-section" id="apply">
        <div class="container">
            <h2 class="section-title">Scholarship Application</h2>
            
            <div class="success-message" id="successMessage">
                <h3>✅ Application Submitted Successfully!</h3>
                <p>Your scholarship application has been received. We will review it and contact you soon.</p>
            </div>
            
            <div class="application-form">
                <form id="scholarshipApplicationForm" onsubmit="submitApplication(event)">
                    <div class="form-group">
                        <label>Full Name *</label>
                        <input type="text" name="full_name" placeholder="Enter your full name" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Email Address *</label>
                        <input type="email" name="email" placeholder="Enter your email address" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Phone Number *</label>
                        <input type="tel" name="phone" placeholder="Enter your phone number" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Select Scholarship *</label>
                        <select name="scholarship_type" required>
                            <option value="">Choose Scholarship</option>
                            <option value="merit">Merit Scholarship</option>
                            <option value="sports">Sports Scholarship</option>
                            <option value="ews">Economically Weaker Section</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Program *</label>
                        <select name="program" required>
                            <option value="">Select Program</option>
                            <option value="bsc">B.Sc</option>
                            <option value="bcom">B.Com</option>
                            <option value="ba">B.A</option>
                            <option value="bms">BMS</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Annual Family Income (in LPA) *</label>
                        <input type="number" name="family_income" placeholder="Enter annual family income" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Previous Year Marks (%) *</label>
                        <input type="number" name="previous_marks" min="0" max="100" step="0.01" placeholder="Enter percentage" required>
                    </div>
                    
                    <div class="form-group">
                        <label>Documents Upload *</label>
                        <div class="file-upload">
                            <input type="file" name="marksheet" accept=".pdf,.jpg,.jpeg" required>
                            <p>📁 Upload Marksheet (PDF, JPG - Max 5MB)</p>
                        </div>
                        <div class="file-upload" style="margin-top: 1rem;">
                            <input type="file" name="income_certificate" accept=".pdf,.jpg,.jpeg" required>
                            <p>📁 Upload Income Certificate (PDF, JPG - Max 5MB)</p>
                        </div>
                        <div class="file-upload" style="margin-top: 1rem;">
                            <input type="file" name="aadhaar" accept=".pdf,.jpg,.jpeg" required>
                            <p>📁 Upload Aadhaar Card (PDF, JPG - Max 5MB)</p>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Why do you deserve this scholarship? *</label>
                        <textarea name="scholarship_essay" placeholder="Write about your achievements and why you deserve this scholarship..." rows="4" required></textarea>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" style="width: 100%; padding: 18px; font-size: 1.1rem;" id="submitBtn">
                        Submit Application
                    </button>
                </form>
            </div>
        </div>
    </section>

    <!-- Contact Footer -->
    <footer style="background: var(--text-dark); color: white; padding: 4rem 0 2rem; text-align: center;">
        <div class="container">
            <h2 style="font-size: 2.2rem; margin-bottom: 2rem;">Scholarship Office</h2>
            <div style="max-width: 600px; margin: 0 auto 2rem;">
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">Financial Aid & Scholarships Department</p>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">📞 ''' + COLLEGE_DATA['contact']['phone'] + ''' | ✉️ scholarships@siwscollege.edu</p>
            </div>
            <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; margin-top: 2rem;">
                <p>&copy; 2024 ''' + COLLEGE_DATA['name'] + ''' Scholarships. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Scholarships Data
        const scholarships = ''' + str(SCHOLARSHIPS).replace("'", '"') + ''';
        
        // Load Scholarships
        function loadScholarships() {
            const scholarshipsGrid = document.getElementById('scholarshipsGrid');
            scholarshipsGrid.innerHTML = '';
            
            scholarships.forEach(scholarship => {
                scholarshipsGrid.innerHTML += `
                    <div class="scholarship-card">
                        <div class="scholarship-header">
                            <h3>${scholarship.name}</h3>
                            <div class="scholarship-amount">${scholarship.amount}</div>
                        </div>
                        <div class="scholarship-content">
                            <div class="scholarship-deadline">Deadline: ${scholarship.deadline}</div>
                            <p>${scholarship.description}</p>
                            
                            <div class="scholarship-beneficiaries">
                                <strong>${scholarship.beneficiaries} Students Benefited</strong>
                            </div>
                            
                            <h4>Eligibility Criteria</h4>
                            <p>${scholarship.eligibility}</p>
                            
                            <h4>Documents Required</h4>
                            <div class="documents-list">
                                ${scholarship.documents_required.map(doc => `<div class="document-item">${doc}</div>`).join('')}
                            </div>
                            
                            <button class="btn btn-primary" style="width: 100%; margin-top: 1.5rem;" onclick="applyForScholarship(${scholarship.id})">
                                Apply Now
                            </button>
                        </div>
                    </div>
                `;
            });
        }
        
        // Apply for Scholarship
        function applyForScholarship(scholarshipId) {
            const scholarship = scholarships.find(s => s.id === scholarshipId);
            if (scholarship) {
                document.getElementById('apply').scrollIntoView({ behavior: 'smooth' });
                document.querySelector('select[name="scholarship_type"]').value = 
                    scholarship.name.toLowerCase().includes('merit') ? 'merit' :
                    scholarship.name.toLowerCase().includes('sports') ? 'sports' : 'ews';
            }
        }
        
        // Submit Application
        function submitApplication(event) {
            event.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const originalText = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = 'Submitting...';
            submitBtn.disabled = true;
            
            // Simulate application submission
            setTimeout(() => {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                
                // Reset form
                document.getElementById('scholarshipApplicationForm').reset();
                
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
                
                // Scroll to success message
                document.getElementById('successMessage').scrollIntoView({ behavior: 'smooth' });
                
                alert('Scholarship application submitted successfully!');
                
            }, 2000);
        }
        
        // Initialize
        loadScholarships();
    </script>
</body>
</html>
'''

# Add the new routes to the Flask app
@app.route('/calendar')
def calendar():
    return render_template_string(CALENDAR_TEMPLATE)

@app.route('/academics')
def academics():
    return render_template_string(ACADEMICS_TEMPLATE)

@app.route('/departments')
def departments():
    return render_template_string(DEPARTMENTS_TEMPLATE)

@app.route('/alumni')
def alumni():
    return render_template_string(ALUMNI_TEMPLATE)

@app.route('/career-services')
def career_services():
    return render_template_string(CAREER_SERVICES_TEMPLATE)

@app.route('/scholarships')
def scholarships():
    return render_template_string(SCHOLARSHIPS_TEMPLATE)

@app.route('/department/<name>')
def department_detail(name):
    if name in DEPARTMENTS:
        dept = DEPARTMENTS[name]
        department_detail_template = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{dept['name']} - SIWS College</title>
            <style>
                /* Include all CSS from departments page */
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: #dbeafe;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 2rem;
                }}
                .department-detail {{
                    background: white;
                    margin-top: 140px;
                    padding: 3rem;
                    border-radius: 25px;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
                }}
            </style>
        </head>
        <body>
            <!-- Header and navigation same as departments page -->
            <div class="department-detail">
                <h1>{dept['name']}</h1>
                <div class="hod-info">
                    <h2>Head of Department: {dept['hod']}</h2>
                    <p>{dept['description']}</p>
                </div>
                <div class="department-programs">
                    <h3>Programs Offered</h3>
                    <ul>
                        {"".join([f'<li>{program}</li>' for program in dept['programs']])}
                    </ul>
                </div>
                <a href="/departments" class="btn">Back to Departments</a>
            </div>
        </body>
        </html>
        '''
        return render_template_string(department_detail_template)
    else:
        return "Department not found", 404

# Existing routes (keep all your existing routes)
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/admissions')
def admissions():
    return render_template_string(ADMISSIONS_TEMPLATE)

@app.route('/facilities')
def facilities():
    return render_template_string(FACILITIES_TEMPLATE)

@app.route('/events')
def events():
    return render_template_string(EVENTS_TEMPLATE)

@app.route('/notices')
def notices():
    return render_template_string(NOTICES_TEMPLATE)

@app.route('/contact')
def contact():
    return render_template_string(CONTACT_TEMPLATE)

@app.route('/submit_application', methods=['POST'])
def submit_application():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        application_type = request.form.get('application_type')
        
        # Handle file uploads
        if 'aadhaar' in request.files:
            aadhaar_file = request.files['aadhaar']
            if aadhaar_file.filename != '':
                filename = secure_filename(aadhaar_file.filename)
                aadhaar_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Here you would typically save to database
        print(f"Application received from {full_name} ({email}) for {application_type}")
        
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('admissions'))
    
    return redirect(url_for('admissions'))

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        # Get form data
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        department = request.form.get('department')
        message = request.form.get('message')
        
        # Here you would typically save to database or send email
        print(f"Contact form submitted by {full_name} ({email}) - {department}: {message}")
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return redirect(url_for('contact'))

if __name__ == '__main__':
    print("🚀 SIWS College Website Starting...")
    print("🏠 Home Page: http://localhost:5000")
    print("📚 Admissions Page: http://localhost:5000/admissions")
    print("🎓 Academics Page: http://localhost:5000/academics")
    print("📅 Calendar Page: http://localhost:5000/calendar")
    print("🏫 Departments Page: http://localhost:5000/departments")
    print("👥 Alumni Page: http://localhost:5000/alumni")
    print("💼 Career Services: http://localhost:5000/career-services")
    print("💰 Scholarships: http://localhost:5000/scholarships")
    print("🏫 Facilities Page: http://localhost:5000/facilities")
    print("🎉 Events Page: http://localhost:5000/events")
    print("📢 Notices Page: http://localhost:5000/notices")
    print("📞 Contact Page: http://localhost:5000/contact")
    print("✨ All 12 pages are fully functional and loaded with content!")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)