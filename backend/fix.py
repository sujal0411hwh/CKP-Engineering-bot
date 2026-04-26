import json

knowledge_base_data = {
  "knowledge_base": [
    {
      "question": "What is CKPCET?",
      "answer": "C. K. Pithawala College of Engineering and Technology (CKPCET) is affiliated with Gujarat Technological University (GTU), Ahmedabad. It's a self-financed engineering college that started in December 1998, managed by Navyug Vidyabhavan Trust. It offers undergraduate programs in multiple engineering disciplines with focus on academic excellence, industry exposure, and practical learning.",
      "category": "General"
    },
    {
      "question": "What are the admission requirements?",
      "answer": "For admission at CKPCET, you must have passed 12th Science with Physics and Mathematics as compulsory subjects. Minimum aggregate: 45% for open category and 40% for reserved categories (SC/ST/SEBC), as per ACPC and GTU admission rules.",
      "category": "Admissions"
    },
    {
      "question": "What is the entrance exam process?",
      "answer": "Admissions are conducted through ACPC (Admission Committee for Professional Courses). Students must appear for GUJCET (Gujarat Common Entrance Test) or JEE Main as per state admission guidelines.",
      "category": "Admissions"
    },
    {
      "question": "What is GUJCET?",
      "answer": "GUJCET is the Gujarat Common Entrance Test for engineering admissions. It tests Physics, Chemistry, and Mathematics. Registration typically opens in March-April. For current dates and registration, visit the official ACPC portal at https://acpc.gujarat.gov.in/",
      "category": "Admissions"
    },
    {
      "question": "What is the admission process?",
      "answer": "Admission process: 1) Pass 12th with required percentage 2) Appear for GUJCET/JEE Main 3) Register on ACPC portal 4) Fill choices during counseling 5) Attend document verification 6) Get seat allotment 7) Pay fees and confirm admission at CKPCET.",
      "category": "Admissions"
    },
    {
      "question": "How do I apply?",
      "answer": "Apply through the ACPC online counseling portal. Register with personal and academic details, upload required documents, and select CKPCET with your preferred branch during choice filling rounds.",
      "category": "Admissions"
    },
    {
      "question": "What is the seat allotment process?",
      "answer": "After ACPC counseling, if you're allotted a seat at CKPCET, you'll receive an allotment letter. Download it, bring required documents to college for verification, pay the fees, and confirm your admission within the deadline.",
      "category": "Admissions"
    },
    {
      "question": "When does admission start?",
      "answer": "Admission typically starts in June-July after 12th results. ACPC conducts 3-4 counseling rounds through July-August. For exact dates, check the ACPC portal. Late admissions may be available under management quota.",
      "category": "Admissions"
    },
    {
      "question": "What are the cutoff ranks?",
      "answer": "Cutoff ranks for CKPCET vary every year depending on applications, exam difficulty, and seat availability. ACPC declares cutoffs after each counseling round. Computer and IT branches generally have lower cutoffs than other branches.",
      "category": "Admissions"
    },
    {
      "question": "Can I change my branch after admission?",
      "answer": "Branch change may be possible after the first year, subject to GTU rules, academic performance, and seat availability. Contact the academic office for specific guidelines after admission.",
      "category": "Admissions"
    },
    {
      "question": "What is the fee structure?",
      "answer": "The tuition fee is approximately ₹44,000 per semester for undergraduate engineering programs. Total fees include tuition, examination, and other charges. Fees are subject to change as per Fee Regulatory Committee (FRC) guidelines.",
      "category": "Fees"
    },
    {
      "question": "How can I pay the fees?",
      "answer": "Fees can be paid online through the college payment portal at https://grayquest.com/institute/ck-pithawala or via bank transfer. Payment modes include debit/card, net banking, and UPI. Fee payment deadlines are strictly followed each semester.",
      "category": "Fees"
    },
    {
      "question": "What is the refund policy?",
      "answer": "Fee refund policy follows GTU and AICTE guidelines. If you withdraw admission, refund amount depends on timing of withdrawal. Contact the college administration office for detailed refund rules.",
      "category": "Fees"
    },
    {
      "question": "Are scholarships available?",
      "answer": "Students can apply for government scholarships for SC, ST, SEBC, EWS categories and other eligible groups. Merit-based and need-based financial assistance is available. Apply through the government scholarship portal after admission. The college assists with scholarship applications.",
      "category": "Fees"
    },
    {
      "question": "Can I get an education loan?",
      "answer": "Education loan assistance is available through partner banks. The college provides necessary documentation and recommendation letters for loan applications. Contact the admission office for bank contacts and loan process guidance.",
      "category": "Fees"
    },
    {
      "question": "Which courses are offered?",
      "answer": "CKPCET offers undergraduate engineering programs (B.E.) in: Computer Engineering, Information Technology, Mechanical Engineering, Civil Engineering, Electrical Engineering, and Electronics & Communication Engineering. All programs are AICTE approved and GTU affiliated.",
      "category": "Academics"
    },
    {
      "question": "How long is the course duration?",
      "answer": "All B.E. (Bachelor of Engineering) programs at CKPCET are 4-year undergraduate courses divided into 8 semesters, following the GTU curriculum.",
      "category": "Academics"
    },
    {
      "question": "What documents are required for admission?",
      "answer": "Required documents: 12th mark sheets (all semesters), GUJCET/JEE Main scorecard, school leaving certificate (LC), transfer certificate (TC), caste certificate (if applicable), income certificate, domicile certificate, Aadhaar card, passport size photos, and migration certificate (if from other board).",
      "category": "Admissions"
    },
    {
      "question": "Is there hostel facility?",
      "answer": "CKPCET provides separate hostel facilities for boys and girls with secure environment, mess facilities, and basic amenities. Hostels are suitable for students coming from different regions.",
      "category": "Facilities"
    },
    {
      "question": "What are the hostel fees?",
      "answer": "Hostel fee structure is separate from college tuition fees. For detailed hostel fees, room types, and facilities, check the hostel section on our website or contact the hostel warden. Fee information is available at: https://ckpcet.ac.in/resources/hostel/detail",
      "category": "Fees"
    },
    {
      "question": "What hostel facilities are available?",
      "answer": "Hostel facilities include: furnished rooms (2-3 sharing), mess with vegetarian food, 24/7 security, common rooms, hot water facility, laundry, and Wi-Fi. Strict discipline and safety rules are maintained.",
      "category": "Facilities"
    },
    {
      "question": "Is there a canteen?",
      "answer": "The campus has a vegetarian canteen providing hygienic and affordable food options including breakfast, lunch, snacks, and beverages for students and staff.",
      "category": "Facilities"
    },
    {
      "question": "Is transportation available?",
      "answer": "CKPCET offers bus transportation from major locations in Surat and nearby areas. Bus routes cover key residential areas to help students commute safely and conveniently. Contact the transport office for route details.",
      "category": "Facilities"
    },
    {
      "question": "What is the library like?",
      "answer": "The central library houses a large collection of academic books, reference materials, national/international journals, and digital resources. It provides a quiet study environment with reading halls and computer terminals for research.",
      "category": "Facilities"
    },
    {
      "question": "What lab facilities are available?",
      "answer": "CKPCET has well-equipped laboratories for all engineering branches including computer labs, mechanical workshop, civil materials testing lab, electrical machines lab, and electronics lab. Practical sessions use modern equipment as per GTU curriculum.",
      "category": "Facilities"
    },
    {
      "question": "Is Wi-Fi available?",
      "answer": "Free Wi-Fi internet connectivity is available across campus for students and faculty to support academics, research, online learning, and accessing digital resources.",
      "category": "Facilities"
    },
    {
      "question": "What are the placement statistics?",
      "answer": "CKPCET has strong placement record with 85%+ placement rate. Average package: ₹4.5 LPA. Highest package: ₹12 LPA (varies yearly). Top performers receive multiple offers from reputed companies.",
      "category": "Placements"
    },
    {
      "question": "Which companies visit for placements?",
      "answer": "Recruiting companies include: TCS, Infosys, Wipro, Tech Mahindra, L&T, Cognizant, HCL, Accenture, and various regional IT and engineering firms. The T&P cell invites 50+ companies annually.",
      "category": "Placements"
    },
    {
      "question": "What is the placement process?",
      "answer": "Students are prepared through pre-placement training including aptitude tests, technical interviews, soft skills, resume building, and mock interviews. Eligible students (minimum 60% aggregate, no backlogs) can participate in placement drives from final year.",
      "category": "Placements"
    },
    {
      "question": "Are internships available?",
      "answer": "Internships are facilitated through the T&P cell. Students can pursue summer internships (after 6th semester) and industrial training. The cell maintains connections with companies for internship opportunities.",
      "category": "Placements"
    },
    {
      "question": "How can I contact the college?",
      "answer": "For admission inquiries: BE/ME programs: +91 78628-24298, General queries: +91 63550-55839 or +91 63550-62275. Email: contact@ckpcet.ac.in. Office hours: 8:30 AM to 4:10 PM, Monday to Saturday.",
      "category": "Contact"
    },
    {
      "question": "What is the college website?",
      "answer": "For complete information, admission updates, and online forms, visit our official website: https://ckpcet.ac.in",
      "category": "Contact"
    },
    {
      "question": "Where is the college located?",
      "answer": "CKPCET is located in Surat, Gujarat. The campus is in a peaceful, green environment away from city congestion. For exact address and directions, please visit: https://ckpcet.ac.in/about/institute/reach-us",
      "category": "Contact"
    },
    {
      "question": "Can I visit the campus?",
      "answer": "Yes, prospective students and parents are welcome to visit the campus. You can contact the admission office to schedule a campus tour. Call us at +91 63550 55839 or +91 63550 62275 during working hours.",
      "category": "General"
    },
    {
      "question": "What is the college affiliation?",
      "answer": "C. K. Pithawala College of Engineering and Technology (CKPCET) is affiliated with Gujarat Technological University (GTU), Ahmedabad. All academic programs follow GTU and AICTE norms, and degrees are awarded by GTU.",
      "category": "General"
    },
    {
      "question": "Is the college accredited?",
      "answer": "CKPCET's Computer Engineering and Civil Engineering programs are accredited by the National Board of Accreditation (NBA), New Delhi.",
      "category": "General"
    },
    {
      "question": "What sports facilities are available?",
      "answer": "CKPCET encourages sports and physical activities. Facilities include cricket ground, badminton court, volleyball court, table tennis, and indoor games. Annual sports events are organized.",
      "category": "Facilities"
    },
    {
      "question": "Are there any technical clubs?",
      "answer": "CKPCET has technical clubs for Coding, Robotics, and Electronics. These clubs conduct workshops, hackathons, competitions, and project exhibitions to enhance students' technical skills beyond regular academics.",
      "category": "General"
    },
    {
      "question": "What cultural activities are available?",
      "answer": "The college actively promotes cultural activities. Students participate in dance, music, drama, arts, and literary events. Cultural festivals are held annually where students showcase their talents.",
      "category": "General"
    },
    {
      "question": "Is there a management quota?",
      "answer": "Yes, CKPCET offers limited management quota seats as per AICTE and GTU norms. These seats have different fee structures. For management quota admission inquiries, contact the college admission office directly.",
      "category": "Admissions"
    }
  ]
}

# Save to file
with open('dataset.json', 'w', encoding='utf-8') as f:
    json.dump(knowledge_base_data, f, indent=2, ensure_ascii=False)

print(f"✅ Created dataset.json with {len(knowledge_base_data['knowledge_base'])} entries!")